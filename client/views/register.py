import streamlit as st
from api_backen.auth_api import register

def render():
    st.header("📝 Register")

    emp_id = st.text_input("Employee ID", key="reg_emp")
    name = st.text_input("Name", key="reg_name")
    email = st.text_input("Email", key="reg_email")
    dept_id = st.number_input("Department ID",key="dept_id",min_value=1,max_value=10,step=1)
    role = st.selectbox("Role", ["employee", "support", "team_lead"])

    if st.button("Register"):
        payload = {
            "emp_id": emp_id,
            "name": name,
            "email_id": email,
            "role": role,
            "dept_id" : dept_id
        }

        res = register(payload)

        if res.status_code == 200:
            st.success("Registered successfully")
        else:
            st.error("Registration failed")









# import streamlit as st
# from api_backen.auth_api import register

# def render():
#     st.subheader("📝 Register")

#     name = st.text_input("Name", key="reg_name")
#     emp_id = st.text_input("Employee ID", key="reg_emp_id")
#     email = st.text_input("Email", key="reg_email")
#     dept_id = st.number_input("Department ID",key="dept_id",min_value=1,max_value=10,step=1)
#     role = st.selectbox(
#         "Role",
#         ["employee", "support", "team_lead"],
#         key="reg_role"
#     )
    

#     if st.button("Register", key="reg_btn"):
#         payload = {
#             "name": name,
#             "emp_id": emp_id,
#             "email_id": email,
#             "role": role,
#             "dept_id" : dept_id
#         }

#         res = register(payload)

#         if res.status_code == 200:
#             st.success("User registered successfully")
#         else:
#             st.error("Registration failed")
