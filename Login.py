from time import sleep

import streamlit as st

from src import AttendanceDB, Teacher, utils

# Page config
st.set_page_config('Login', '💬', 'wide')

connection_url = st.secrets['MONGODB_STR']
db = st.cache_resource(AttendanceDB)(connection_url)
teachers = Teacher(db.TEACHERS)

message_area = st.empty()

# Check whether the user is logged in or not.
try:
    login_data = utils.get_login_data(st.session_state)
    if login_data:
        st.write(f'#### :red[Teacher Name:] {login_data["name"]}')
        st.write(f'#### :red[Role:] {login_data["role"]}')
        st.write(f'#### :red[School Name:] {login_data["school_name"]}')

        # Profile Updating
        if st.button('**Update Profile**', use_container_width=True):
            st.success(
                'Profile updating is now available. **Go to Update Page.**',
            )

        # User logout
        if st.button('**Logout**', use_container_width=True):
            utils.logout(st.session_state)
            st.balloons()
            st.experimental_rerun()

except KeyError:
    with st.form('login-form'):
        teacher_name = st.text_input('Teacher Name').strip()
        mob_num = st.text_input('Mobile Number', type='password')
        st.markdown('[Register Yourself](/Register)')

        if st.form_submit_button():
            registered, response = teachers.registered(teacher_name,
                                                       str(mob_num), True)
            if registered and isinstance(response, dict):
                message_area.success(f'**{teacher_name}** is logged in.')

                # Save teacher details in streamlit's session_state
                st.session_state.update(response)

                with st.spinner(f"Loading **{teacher_name}'s** data..."):
                    sleep(2)
                    st.balloons()
                st.experimental_rerun()
            else:
                message_area.error(f'**{teacher_name}** is not registered.')
                message_area.error(f'Wrong Name / Mobile Number.')
