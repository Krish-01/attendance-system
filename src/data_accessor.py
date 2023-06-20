
from dataclasses import dataclass
from json import loads

import pandas as pd
from bson.json_util import dumps


@dataclass
class DataAccessor:
    data: list[dict]

    def __post_init__(self):
        self.df = pd.DataFrame(loads(dumps(self.data)))

    def get_df(self, teacher_details: bool = False):
        df = self.df.copy()

        df['entry_id'] = df['_id'].str.get('$oid')    # type: ignore
        df['teacher_id'] = df['teacher_id'].str.get('$oid')    # type: ignore
        df['datetime'] = pd.to_datetime(df['datetime']
                                        .str.get('$date'))    # type: ignore
        df['date'] = df['datetime'].dt.date
        df['time'] = df['datetime'].dt.time

        df = df.drop(columns=['_id', 'datetime'])

        if teacher_details:
            new_df = df.merge(self.__teacher_details_df(), 'inner',
                              left_on='teacher_id', right_on='_id')
            new_df = new_df.drop(columns=['teacher_details', '_id'])
            return new_df
        return df

    def __teacher_details_df(self) -> pd.DataFrame:
        df = pd.json_normalize(self.data, 'teacher_details').drop_duplicates()

        df['_id'] = df['_id'].astype(str)

        df = df.drop(columns=['mob_num'])
        return df
