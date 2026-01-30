import streamlit as st
from api_backen.auth_api import login
from utils.state import init_session

def render():
    init_session()
    st.header("🔐 Login")

    emp_id = st.text_input("Employee ID", key="login_emp")
    email = st.text_input("Email", key="login_email")
    password = st.text_input("Password", type="password")

    if st.button("Login"):

        if not emp_id or not email or not password:
            st.warning("Please fill all fields")
            return
        
        res = login(emp_id,email, password)

        if res.status_code == 200:
            data = res.json()
            st.session_state.session_id = data["session_id"]
            st.session_state.role = data["role"]
            st.session_state.name = data["name"]
            st.session_state.emp_id = data.get("emp_id")
            st.session_state.dept_name = data.get("dept_name")
            st.success("Login successful")
            st.rerun()
        else:
            st.error("Invalid credentials")
