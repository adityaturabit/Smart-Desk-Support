import streamlit as st
from utils.state import init_session, is_logged_in, logout
from views import login, register
from views.employee import render as employee_view
from views.support_agent import render as support_view
from views.team_lead import render as teamlead_view

st.set_page_config(page_title="Smart Support Desk", layout="wide")

init_session()

# -------- SIDEBAR --------
if is_logged_in():
    with st.sidebar:
        st.title("Smart Support Desk")
        st.write(f"Emp ID: {st.session_state.emp_id}")
        st.write(f"👤 {st.session_state.name}")
        st.write(f"Role: {st.session_state.role}")
        st.write(f"Department: {st.session_state.dept_name}")

        if st.button("Logout"):
            logout()


# -------- ROUTING --------
if not is_logged_in():
    tab1, tab2 = st.tabs(["Login", "Register"])
    with tab1:
        login.render()
    with tab2:
        register.render()
else:
    if st.session_state.role == "employee":
        employee_view()
    elif st.session_state.role == "support":
        support_view()
    elif st.session_state.role == "team_lead":
        teamlead_view()






# import streamlit as st

# from views import login, register
# from views.employee import render as employee_render
# from views.support_agent import render as support_render
# from views.team_lead import render as teamlead_render


# # ---------- SESSION INIT ----------
# if "session_id" not in st.session_state:
#     st.session_state.session_id = None
#     st.session_state.role = None
#     st.session_state.name = None


# # ---------- SIDEBAR ----------
# def render_sidebar():
#     if not st.session_state.session_id:
#         return

#     st.sidebar.title("Smart Support Desk")
#     st.sidebar.write(f"👤 {st.session_state.name}")
#     st.sidebar.write(f"Role: {st.session_state.role}")

#     if st.sidebar.button("Logout"):
#         st.session_state.clear()
#         st.rerun()


# # ---------- LOGIN GUARD ----------
# def require_login():
#     if not st.session_state.session_id:
#         st.warning("Please login first")
#         st.stop()


# # ---------- APP ----------
# st.set_page_config(page_title="Smart Support Desk", layout="wide")

# render_sidebar()

# # 🔴 NOT LOGGED IN
# if not st.session_state.session_id:
#     tab1, tab2 = st.tabs(["Login", "Register"])

#     with tab1:
#         login.render()

#     with tab2:
#         register.render()

# # 🟢 LOGGED IN
# else:
#     require_login()

#     if st.session_state.role == "employee":
#         employee_render()

#     elif st.session_state.role == "support":
#         support_render()

#     elif st.session_state.role == "team_lead":
#         teamlead_render()









# # from pages import login, register
# # from pages.employee import render as emp_dash
# # from pages.support_agent import render as sup_dash
# # from pages.team_lead import render as tl_dash
# # import streamlit as st

# # def init_auth():
# #     if "session_id" not in st.session_state:
# #         st.session_state.session_id = None
# #         st.session_state.role = None
# #         st.session_state.name = None

# # init_auth()

# # st.set_page_config(page_title="Smart Support Desk", layout="wide")

# # def render_sidebar():
# #     if not st.session_state.session_id:
# #         return  # 🔴 NO SIDEBAR

# #     st.sidebar.title("Smart Support Desk")
# #     st.sidebar.write(f"👋 {st.session_state.name}")
# #     st.sidebar.write(f"Role: {st.session_state.role}")

# #     if st.sidebar.button("Logout"):
# #         st.session_state.clear()
# #         st.rerun()


# # def require_login():
# #     if not st.session_state.session_id:
# #         st.warning("Please login first")
# #         st.stop()  # 🔥 THIS STOPS PAGE EXECUTION


# # render_sidebar()


# # if not st.session_state.session_id:
# #     tab1, tab2 = st.tabs(["Login", "Register"])
# #     with tab1:
# #         login.render()
# #     with tab2:
# #         register.render()
# # else:
# #     # 🔐 AUTHENTICATED AREA
# #     if st.session_state.role == "employee":
# #         require_login()
# #         emp_dash.render()

# #     elif st.session_state.role == "support":
# #         require_login()
# #         sup_dash.render()

# #     elif st.session_state.role == "team_lead":
# #         require_login()
# #         tl_dash.render()






















# # import streamlit as st
# # from state import is_logged_in, logout

# # st.set_page_config(page_title="Smart Support Desk", layout="wide")

# # # 🔐 NOT LOGGED IN → ONLY LOGIN / REGISTER
# # if not is_logged_in():
# #     st.title("Smart Support Desk")

# #     tab1, tab2 = st.tabs(["Login", "Register"])

# #     with tab1:
# #         from pages import login
# #         login.render()

# #     with tab2:
# #         from pages import register
# #         register.render()

# #     st.stop()  # ⛔ VERY IMPORTANT

# # # ✅ LOGGED IN → ROLE-BASED APP
# # role = st.session_state["role"]

# # with st.sidebar:
# #     st.write(f"👋 {st.session_state['name']}")
# #     st.write(f"🔑 Role: {role}")

# #     if st.button("Logout"):
# #         logout()
# #         st.rerun()

# # # ROLE ROUTING
# # if role == "employee":
# #     from pages import employee
# #     employee.render()

# # elif role == "support":
# #     from pages import support_agent
# #     support_agent.render()

# # elif role == "team_lead":
# #     from pages import team_lead
# #     team_lead.render()
