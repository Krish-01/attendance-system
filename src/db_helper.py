import pymongo
from pymongo.collection import Collection
from pymongo.database import Database


class AttendanceDB:
    def __init__(self, connection_url: str) -> None:
        self.CLIENT = pymongo.MongoClient(connection_url)
        self.ATTENDANCE_DB: Database = self.CLIENT['attendance']
        self.TEACHERS: Collection = self.ATTENDANCE_DB['teachers']
        self.DAILY_ENTRY: Collection = self.ATTENDANCE_DB['daily_entry']
