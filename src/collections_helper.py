from dataclasses import dataclass
from datetime import date
from datetime import datetime as dt
from pathlib import Path
from typing import Union

from bson import ObjectId
from bson.json_util import dumps, loads
from pymongo.collection import Collection

from .db_helper import AttendanceDB
from .doc_structure import DocStructure


@dataclass
class Teacher:
    _collection: Collection

    def add(
        self,
        *,
        name: str,
        role: str,
        school_name: str,
        mob_num: str,
    ):
        registered = self.registered(name, mob_num)

        if registered:
            raise ValueError(
                f'{name} is already exists.'
            )
        self._collection.insert_one(
            DocStructure.teacher(name, role, school_name, mob_num)
        )

    def registered(
        self,
        name: str,
        mob_num: str,
        store: bool = False
    ) -> tuple[bool, Union[dict, None]]:
        response = self.find(name=name, mob_num=mob_num)

        if response:
            if store:
                return True, response
            return True, None
        return False, None

    def find(
        self,
        *,
        teacher_id: ObjectId = ...,
        name: str = ...,
        role: str = ...,
        school_name: str = ...,
        mob_num: str = ...,
    ) -> Union[dict, None]:
        doc = {}

        if isinstance(teacher_id, str):
            doc['_id'] = teacher_id
        if isinstance(name, str):
            doc['name'] = name
        if isinstance(role, str):
            doc['role'] = role
        if isinstance(school_name, str):
            doc['school_name'] = school_name
        if isinstance(mob_num, str):
            doc['mob_num'] = mob_num

        if len(doc) == 0:
            raise ValueError(
                'Provide at least 1 argument.'
            )
        return self._collection.find_one(doc)


@dataclass
class DailyAttendance:
    _collection: Collection
    connection_url: str

    def __post_init__(self):
        att_db = AttendanceDB(self.connection_url)
        self.__user_collection = Teacher(att_db.TEACHERS)

    def _adding_validation(self, _class: int, datetime: dt, school_name: str):
        start, end = self._get_start_end_datetime(datetime.date(),
                                                  datetime.date())

        response = self._collection.find_one({
            'class': _class,
            'school_name': school_name,
            'datetime': {'$gte': start, '$lte': end},
        })
        if response:
            raise ValueError(
                f'Entry of class {_class} on {datetime:%d-%m-%Y} already submitted.'
            )

    def add(
        self,
        teacher_id: str,
        datetime: dt,
        _class: int,
        n_boys: int,
        n_girls: int,
        school_name: str,
    ):
        self._adding_validation(_class, datetime, school_name)
        self._collection.insert_one(
            DocStructure.daily_entry(
                datetime.replace(microsecond=0), _class, teacher_id,
                n_boys, n_girls, school_name,
            ))

    def _get_start_end_datetime(self, from_date: date, to_date: date) -> tuple[dt, dt]:
        start = dt(from_date.year, from_date.month, from_date.day)
        end = dt(to_date.year, to_date.month, to_date.day, 23, 59, 59, 999)
        return start, end

    def find(
        self,
        *,
        attendance_id: ObjectId = ...,
        datetime: tuple[date, date] = ...,
        _class: int = ...,
        teacher_name: str = ...,
        school_name: str = ...,
    ) -> list[dict]:
        doc = {}

        if isinstance(attendance_id, ObjectId):
            doc['_id'] = attendance_id
        if isinstance(datetime, tuple):
            start, end = self._get_start_end_datetime(*datetime)
            doc['datetime'] = {'$gte': start, '$lte': end}
        if isinstance(_class, int):
            doc['class'] = _class
        if isinstance(school_name, str):
            doc['school_name'] = school_name
        if isinstance(teacher_name, str):
            teacher_details = self.__user_collection.find(name=teacher_name)
            if teacher_details is not None:
                doc['teacher_id'] = teacher_details['_id']
            else:
                doc['teacher_id'] = ObjectId()

        response = list(self._collection.find(doc))
        return response

    def get_attendance_id(self, **params):
        res = self._collection.find_one(params)
        if res is None:
            raise ValueError(
                'Provided data is present in the database.'
            )
        return res['_id']

    def update(self, attendance_id: ObjectId, data: dict):
        self._collection.update_one(
            {'_id': attendance_id},
            {'$set': data},
        )
