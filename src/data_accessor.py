
from dataclasses import dataclass
from json import loads

from bson.json_util import dumps
from pandas import DataFrame


@dataclass
class DataAccessor:
    data: list[dict]

    def __post_init__(self):
        self.df = DataFrame(loads(dumps(self.data)))

    def get_df(self):
        df = self.df
        df['_id'] = df['_id'].str.get('$oid')    # type: ignore
        df['teacher_id'] = df['teacher_id'].str.get('$oid')    # type: ignore
        df['datetime'] = (df['datetime']
                          .str.get('$date')    # type: ignore
                          .astype('datetime64')    # type: ignore
                          )
        df['date'] = df['datetime'].dt.date
        df['time'] = df['datetime'].dt.time

        return df
