from datetime import datetime as dt
from typing import Union

import streamlit as st
from pandas import DataFrame

from src import AttendanceDB, DailyAttendance, Teacher
from src.data_accessor import DataAccessor

# Page config
st.set_page_config('Entry Data', '🗂️', 'wide')

connection_url = st.secrets['MONGODB_STR']
db = st.cache_resource(AttendanceDB)(connection_url)
teachers = Teacher(db.TEACHERS)
daily_entry = st.cache_resource(DailyAttendance)(
    db.DAILY_ENTRY, connection_url)


def get_df(**kwargs) -> Union[DataFrame, None]:
    if kwargs['_class'] == 'All Classes':
        del kwargs['_class']
    if not kwargs['teacher_name']:
        del kwargs['teacher_name']

    response = daily_entry.find(**kwargs)
    if response:
        df = DataAccessor(response)
        return df.get_df()


with st.sidebar:
    options = [
        'school_name',
    ]
    show_df_cols = st.multiselect('Select table columns to show', options)

message_area = st.empty()

# Check whether the user is logged in or not.
try:
    login_data = teachers.get_logged_in_data()
except FileNotFoundError:
    message_area.error('Please Login First.')
    st.stop()

df = None
with st.form('entry-data'):
    st.write('Pass data in any filed to get data.')
    teacher_name = st.text_input('Teacher Name')
    school_name = st.text_input('School Name', login_data['school_name'],
                                disabled=True)
    _class = st.selectbox('Class', ['All Classes'] + list(range(1, 13)))

    col1, col2 = st.columns(2)
    from_date = col1.date_input('From Date', dt.now())
    to_date = col2.date_input('To Date', dt.now())

    form_submit_btn = st.form_submit_button()
    if form_submit_btn:
        kwargs = {
            'school_name': school_name,
            'datetime': (from_date, to_date),
            '_class': _class,
            'teacher_name': teacher_name,
        }
        df = get_df(**kwargs)


if isinstance(df, DataFrame) and not df.empty:
    df = df[['class', 'n_boys', 'n_girls', 'datetime'] + show_df_cols]
    df.rename(columns={
        'class': 'Class',
        'n_boys': 'No. of Boys',
        'n_girls': 'No. of Girls',
        'datetime': 'Entry Date & Time',
        'school_name': 'School Name',
    }, inplace=True)

    st.markdown('---')
    st.download_button('**Download Table**', df.to_csv(index=False),
                       'entry_data.csv', 'csv',
                       use_container_width=True)
    st.table(df)
    st.stop()

if form_submit_btn:
    st.error('No data for this query!')
