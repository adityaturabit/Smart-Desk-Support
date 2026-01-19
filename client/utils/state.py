import streamlit as st

def init_session():
    defaults = {
        "session_id": None,
        "role": None,
        "name": None,
        "emp_id": None,
        "dept_id": None,
        "dept_name": None,
    }

    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v


def is_logged_in():
    return st.session_state.session_id is not None


def logout():
    st.session_state.clear()
    st.rerun()
