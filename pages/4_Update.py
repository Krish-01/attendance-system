from time import sleep
from src import AttendanceDB, Teacher, utils, DocStructure

import streamlit as st

# Page config
st.set_page_config('Update Page', '🔖', 'wide')

connection_url = st.secrets['MONGODB_STR']
db = st.cache_resource(AttendanceDB)(connection_url)
teachers = Teacher(db.TEACHERS)

message_area = st.empty()

try:
    login_data = utils.get_login_data(st.session_state)
except KeyError:
    message_area.error('Please Login First.')
    st.stop()

with st.sidebar:
    radio = st.radio('Update:', ['Profile', 'Attendance Data'])

if radio == 'Profile':
    with st.form('update-teacher-profile'):
        st.subheader('👨‍🏫 Update user profile')

        teacher_name = st.text_input('Teacher Name',
                                     login_data['name']).strip()
        role = st.text_input("Teacher's Role",
                             login_data['role']).strip()
        school_name = st.text_input('School Name',
                                    login_data['school_name']).strip()
        mob_num = st.number_input('Mobile Number', value=int(login_data['mob_num']),
                                  max_value=9_999_999_999, format='%d')

        if st.form_submit_button():
            try:
                doc = DocStructure.teacher(
                    teacher_name, role, school_name, str(mob_num)
                )
            except ValueError as e:
                message_area.error(e)
                st.stop()
            doc.update({'_id': login_data['_id']})
            teachers.update(doc)

            with st.spinner(f'Updating profile...'):
                sleep(2)
                st.balloons()
            utils.logout(st.session_state)
            st.experimental_rerun()

elif radio == 'Attendance Data':
    message_area.error('This feature is not available.')
