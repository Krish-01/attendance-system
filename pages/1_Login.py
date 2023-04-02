from time import sleep

import streamlit as st

from src import AttendanceDB, Teacher

# Page config
st.set_page_config('Login', '💬', 'wide')

connection_url = st.secrets['MONGODB_STR']
db = st.cache_resource(AttendanceDB)(connection_url)
teachers = Teacher(db.TEACHERS)

message_area = st.empty()

# Check whether the user is logged in or not.
try:
    login_data = teachers.get_logged_in_data()
    if login_data:
        st.write(f'#### :red[Teacher Name:] {login_data["name"]}')
        st.write(f'#### :red[Role:] {login_data["role"]}')
        st.write(f'#### :red[School Name:] {login_data["school_name"]}')
        st.write(f'#### :red[Mobile Number:] {login_data["mob_num"]}')

        # Profile Updating
        if st.button('**Update Profile**', use_container_width=True):
            st.error('Profile updating is not available.')

        # User logout
        if st.button('**Logout**', use_container_width=True):
            teachers.logout()
            st.balloons()
            st.experimental_rerun()

except FileNotFoundError:
    with st.form('login-form'):
        teacher_name = st.text_input('Teacher Name').strip()
        mob_num = int(st.number_input('Mobile Number',
                                      max_value=9_999_999_999, format='%d'))
        st.markdown('[Register Yourself](/Register)')

        if st.form_submit_button():
            register = teachers.registered(teacher_name, str(mob_num), True)
            if register:
                message_area.success(f'**{teacher_name}** is logged in.')
                with st.spinner(f"Loading **{teacher_name}'s** data..."):
                    sleep(3)
                    st.balloons()
                st.experimental_rerun()
            else:
                message_area.error(f'**{teacher_name}** is not registered.')
                message_area.error(f'Wrong Name / Mobile Number.')
