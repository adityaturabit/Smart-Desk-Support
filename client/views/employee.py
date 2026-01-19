import streamlit as st
import pandas as pd
from api_backen.ticket_api import create_ticket, get_my_tickets
from utils.state import logout

def render():
    st.title("🎫 Employee Dashboard")

    # -------- LOGOUT BUTTON --------
    # if st.button("Logout"):
    #     logout()

    # st.divider()

    # -------- LOAD TICKETS --------
    res = get_my_tickets()
    tickets = res.json() if res.status_code == 200 else []

    # -------- KPIs --------
    col1, col2, col3 = st.columns(3)
    col1.metric("Open", len([t for t in tickets if t["status"] == "open"]))
    col2.metric("Pending", len([t for t in tickets if t["status"] == "pending"]))
    col3.metric("Closed", len([t for t in tickets if t["status"] == "closed"]))

    st.divider()

    # -------- CREATE TICKET --------
    st.subheader("Create Ticket")

    with st.form("employee_create_ticket"):
        title = st.text_input("Title", key="emp_title")
        description = st.text_area("Description", key="emp_desc")
        priority = st.selectbox(
            "Priority",
            ["low", "medium", "high"],
            key="emp_priority"
        )
        submitted = st.form_submit_button("Create Ticket")

        if submitted:
            payload = {
                "title": title,
                "description": description,
                "priority": priority
            }

            r = create_ticket(payload)
            if r.status_code == 200:
                st.success("Ticket created successfully")
                st.rerun()
            else:
                st.error(r.json().get("detail", "Error creating ticket"))

    st.divider()

    # -------- MY TICKETS TABLE --------
    st.subheader("My Tickets")

    if tickets:
        df = pd.DataFrame(tickets)
        if "updated_at" not in df.columns:
            df["updated_at"] = None
        df = df[["id", "title", "priority", "status", "created_at","updated_at"]]
        st.dataframe(df, use_container_width=True)
    else:
        st.info("No tickets created yet.")
