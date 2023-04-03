from typing import MutableMapping

data_keys = ['_id', 'name', 'role', 'school_name', 'mob_num']


def get_login_data(session_state: MutableMapping):
    if len(session_state.keys()) < len(data_keys):
        raise KeyError('Require login details.')

    login_data = {key: val for key, val in session_state.items()
                  if key in data_keys}
    return login_data


def logout(session_state: MutableMapping):
    for i in data_keys:
        del session_state[i]
