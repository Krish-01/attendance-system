import streamlit as st

from src import AttendanceDB, Teacher

# Page config
st.set_page_config('Teacher Registration', '🔖', 'wide', 'expanded')

connection_url = st.secrets['MONGODB_STR']
db = st.cache_resource(AttendanceDB)(connection_url)
teacher = Teacher(db.TEACHERS)

message_area = st.empty()

with st.form('registration-form', True):
    teacher_id = st.text_input('Teacher Name').strip()
    role = st.text_input("Teacher's Role").strip()
    school_name = st.text_input('School Name').strip()
    mob_num = int(st.number_input('Mobile Number',
                  max_value=9_999_999_999, format='%d'))
    st.markdown('[Already Registered](/Login)')

    if st.form_submit_button():
        try:
            teacher.add(
                name=teacher_id,
                role=role,
                school_name=school_name,
                mob_num=str(mob_num),
            )
            message_area.success(f'**{teacher_id!r}** is registered now.')
            st.balloons()
        except ValueError as e:
            message_area.error(f'**{e}** Please go to login page.')
