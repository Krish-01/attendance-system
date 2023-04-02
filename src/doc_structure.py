from datetime import datetime as dt


class DocStructure:
    @classmethod
    def teacher(cls, name: str, role: str, school_name: str, mob_num: str):
        if len(mob_num) != 10 or not mob_num.isnumeric():
            raise ValueError('Mobile Number must be of 10 digits.')

        return {
            'name': name,
            'role': role,
            'school_name': school_name,
            'mob_num': mob_num,
        }

    @classmethod
    def daily_entry(
        cls,
        datetime: dt,
        _class: int,
        teacher_id: str,
        n_boys: int,
        n_girls: int,
        school_name: str,
    ):
        return {
            'datetime': datetime,
            'class': _class,
            'teacher_id': teacher_id,
            'n_boys': n_boys,
            'n_girls': n_girls,
            'school_name': school_name
        }
