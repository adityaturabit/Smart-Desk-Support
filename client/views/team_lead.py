import streamlit as st
import pandas as pd
import altair as alt

from utils.state import is_logged_in
from api_backen.ticket_api import (
    get_teamlead_tickets,
    assign_ticket,
    update_ticket_status,
    delete_ticket,
    get_weekly_analytics,
)
from api_backen.customer_api import get_support_agents, get_customers
import streamlit as st
from api_backen.auth_api import register
from api_backen.ticket_api import get_my_tickets


# ---------- CONSTANTS ----------
PRIORITY_ORDER = {
    "high": 1,
    "medium": 2,
    "low": 3,
    "planned": 4,
    "investigation": 5,
}

STATUS_BADGE = {
    "open": "🔵 OPEN",
    "pending": "🟠 PENDING",
    "closed": "⚫ CLOSED",
}


# ---------- ENTRY ----------
def render():
    if not is_logged_in() or st.session_state.role != "team_lead":
        st.error("Unauthorized")
        return

    st.title("📊 Team Lead Dashboard")

    tickets = get_teamlead_tickets().json().get("tickets", [])
    agents = get_support_agents().json()
    customers = get_customers().json()
    analytics = get_weekly_analytics().json()

    res = get_my_tickets()
    tickets = res.json() if res.status_code == 200 else []
    # st.divider()
    # -------- KPIs --------
    col1, col2, col3,col4 = st.columns(4)
    col1.metric("Open", len([t for t in tickets if t["status"] == "open"]))
    col2.metric("Pending", len([t for t in tickets if t["status"] == "pending"]))
    col3.metric("Closed", len([t for t in tickets if t["status"] == "closed"]))
    col4.metric("Total", len([t for t in tickets ]))

    
    tabs = st.tabs([
        "📋 Tickets",
        "🔁 Assign Tickets",
        "📈 Weekly Analytics",
        "Agents",
        "👥 Customers",
    ])


    # ================= TAB 1: TICKETS =================
    with tabs[0]:
        active = [t for t in tickets if t["status"] != "closed"]
        closed = [t for t in tickets if t["status"] == "closed"]

        st.subheader("🟢 Open / Pending Tickets")
        
        show_ticket_table(active, "active")

        st.subheader("⚫ Closed Tickets")
        show_ticket_table(closed, "closed")

        if st.session_state.get("selected_ticket"):
            show_ticket_detail(st.session_state.selected_ticket)
        

    # ================= TAB 2: ASSIGN =================
    with tabs[1]:
        st.subheader("🔁 Assign / Reassign Ticket")

        open_tickets = [t for t in tickets if t["status"] == "open"]
        if not open_tickets:
            st.info("No OPEN tickets available")
        else:
            ticket_map = {f"{t['title']} (ID {t['id']})": t["id"] for t in open_tickets}
            agent_map = {f"{a['name']} (ID {a['id']})": a["id"] for a in agents}

            with st.form("assign_form"):
                ticket_label = st.selectbox("Ticket", ticket_map.keys())
                agent_label = st.selectbox("Support Agent", agent_map.keys())

                if st.form_submit_button("Assign Ticket"):
                    assign_ticket(ticket_map[ticket_label], agent_map[agent_label])
                    st.success("Ticket assigned")
                    st.rerun()

    # ================= TAB 3: ANALYTICS =================
    with tabs[2]:
        st.subheader("📈 Weekly Agent Performance")

        if not analytics:
            st.info("No analytics data")
        else:
            df = pd.DataFrame(analytics)
            df["date"] = pd.to_datetime(df["date"])

            agent_filter = st.selectbox(
                "Filter by Agent",
                ["All"] + sorted(df["agent_name"].unique().tolist())
            )

            if agent_filter != "All":
                df = df[df["agent_name"] == agent_filter]

            st.dataframe(
                df[["date", "agent_name", "opened", "pending", "closed"]],
                use_container_width=True,
            )

            chart_df = df.melt(
                id_vars=["date", "agent_name"],
                value_vars=["opened", "pending", "closed"],
                var_name="status",
                value_name="count",
            )

            chart = (
                alt.Chart(chart_df)
                .mark_bar()
                .encode(
                    x="date:T",
                    y="count:Q",
                    color="status:N",
                    tooltip=["agent_name", "status", "count"],
                )
                .properties(height=400)
            )

            st.altair_chart(chart, use_container_width=True)

    
    with tabs[3]:
        st.header("👥 Support Agents")
        st.subheader("📝 Register")

        emp_id = st.text_input("Employee ID", key="reg_emp")
        name = st.text_input("Name", key="reg_name")
        email = st.text_input("Email", key="reg_email")
        dept_id = st.number_input("Department ID",key="dept_id",min_value=1,max_value=10,step=1)
        role = st.selectbox("Role", ["support", "team_lead"])
        password = st.text_input("Password", key="reg_password")

        if st.button("Register"):
            payload = {
                "emp_id": emp_id,
                "name": name,
                "email_id": email,
                "role": role,
                "dept_id" : dept_id,
                "password": password
            }

            res = register(payload)

            if res.status_code == 200:
                st.success("Registered successfully")
            else:
                st.error("Registration failed")
        
        if not agents:
            st.caption("No support agents found")
        else:
            
            df = pd.DataFrame(agents)
            # Replace 'new_name' with your desired column names
            # Select only the columns you want and rename them simultaneously
            df_display = df[["id", "emp_id", "name", "dept_name"]].rename(columns={
                "id": "Agent Id",
                "emp_id": "Employee ID",
                "name": "Full Name",
                "dept_name": "Department Name"
            })

            st.dataframe(df_display, use_container_width=True)


            # st.dataframe(
            #     df[["id","emp_id", "name", "dept_name"]],
            #     use_container_width=True,
            # )

        
        
        # else:
        #     for a in agents:
        #         st.markdown(
        #             f"**{a['name']}**  \n"
        #             f"ID: {a['emp_id']}  \n"
        #             f"Dept: {a.get('dept_name', '-')}"
        #         )


    # ================= TAB 4: CUSTOMERS =================
    with tabs[4]:
        st.subheader("👥 Customers Created by Support Agents")
        
        if not customers:
            st.info("No customers found")
        else:
            df = pd.DataFrame(customers)
            
            st.dataframe(
                df[["id", "name", "email", "company", "created_by_agent_id"]],
                use_container_width=True,
            )


# ---------- TICKET TABLE ----------
def show_ticket_table(tickets, key_prefix):
    if not tickets:
        st.info("No tickets available")
        return

    df = pd.DataFrame(tickets)
    df["priority_rank"] = df["priority"].map(PRIORITY_ORDER)
    df = df.sort_values("priority_rank")

    st.dataframe(
        df[["id", "title", "priority", "status"]],
        use_container_width=True,
        hide_index=True,
    )

    selected_id = st.selectbox(
        "Select Ticket ID to view details",
        options=[None] + df["id"].tolist(),
        key=f"select_{key_prefix}",
    )

    if selected_id is not None:
        st.session_state.selected_ticket = next(
            (t for t in tickets if t["id"] == selected_id),
            None
        )
    # else:
    #     st.session_state.selected_ticket = None
        



# ---------- TICKET DETAIL ----------
def show_ticket_detail(t):
    st.divider()
    st.subheader("📄 Ticket Details")

    if not t:
        return

    st.markdown(f"🎫 {t['title']}")
    st.caption(f"Ticket ID: {t['id']}")

    col1, col2 = st.columns(2)
    col1.write(f"**Priority:** {t['priority']}")
    col1.write(f"**Status:** {STATUS_BADGE[t['status']]}")
    col2.write(f"**Customer ID:** {t.get('customer_id')}")
    col2.write(f"**Assigned Agent:** {t.get('assigned_agent')}")

    st.markdown("**Description**")
    st.info(t.get("description", "No description"))

    # ---- Update Status ----
    if t["status"] != "closed":
        new_status = st.selectbox(
            "Update Status",
            ["open", "pending", "closed"],
            index=["open", "pending", "closed"].index(t["status"]),
        )

        if st.button("Save Status"):
            update_ticket_status(t["id"], new_status)
            del st.session_state.selected_ticket
            st.success("Status updated")
            st.rerun()

    # ---- Delete Ticket ----
    st.markdown("### 🗑 Delete Ticket")
    reason = st.text_area("Deletion reason (required)")

    if st.button("Delete Ticket"):
        if not reason.strip():
            st.error("Reason required")
        else:
            delete_ticket(t["id"], reason=reason)
            del st.session_state.selected_ticket
            st.success("Ticket deleted")
            st.rerun()

    if st.button("❌ Close Details"):
        st.session_state.selected_ticket = None
        st.session_state.open_ticket_select = None
        st.session_state.closed_ticket_select = None
        st.rerun()