from datetime import datetime as dt

import streamlit as st

from src import AttendanceDB, DailyAttendance, Teacher, utils

# Page config
st.set_page_config('Daily Entry Form', '🗒️', 'wide')

st.title('Daily Attendance Entry')


# Database and collections
connection_url = st.secrets['MONGODB_STR']
db = st.cache_resource(AttendanceDB)(connection_url)
teachers = Teacher(db.TEACHERS)
daily_entry = st.cache_resource(DailyAttendance)(
    db.DAILY_ENTRY, connection_url)

# --- Empty area for messages --- #
message_area = st.empty()

# Check whether the user is logged in or not.
try:
    login_data = utils.get_login_data(st.session_state)
except KeyError:
    message_area.error('Please Login First.')
    st.stop()


with st.form('daily_entry_form', True):
    col1, col2 = st.columns(2)
    col1.text_input('Teacher Name', login_data['name'],
                    disabled=True)
    col2.date_input('Today Date', dt.now(), disabled=True)
    school_name = st.text_input('School Name', login_data['school_name'],
                                disabled=True)
    _class: int = st.selectbox('Class', range(1, 13))    # type: ignore
    n_boys = int(st.number_input('No. of present boys',
                                 min_value=0, format='%d'))
    n_girls = int(st.number_input('No. of present girls',
                                  min_value=0, format='%d'))

    # Get teacher_id from login data
    teacher_id = login_data['_id']
    datetime = dt.now()

    if st.form_submit_button('Add Entry'):
        try:
            daily_entry.add(teacher_id, datetime, _class,
                            n_boys, n_girls, school_name)
            message_area.success(
                f'Entry of class {_class} on {datetime:%d-%m-%Y} submitted.'
            )
        except ValueError as e:
            message_area.error(e)
