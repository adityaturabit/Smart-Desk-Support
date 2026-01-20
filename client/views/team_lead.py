import streamlit as st
from api_backen.ticket_api import get_teamlead_tickets,assign_ticket,get_weekly_analytics,delete_ticket,update_ticket_status
from utils.state import is_logged_in
from api_backen.customer_api import get_support_agents,get_customers
import pandas as pd
import altair as alt
import pandas as pd



def status_badge(status):
    colors = {
        "open": "🔵 OPEN", 
        "pending": "🟠 PENDING",
        "closed": "⚫ CLOSED"
    }
    return colors.get(status, status)


def render_kpis(tickets):
    open_t = len([t for t in tickets if t["status"] == "open"])
    pending_t = len([t for t in tickets if t["status"] == "pending"])
    closed_t = len([t for t in tickets if t["status"] == "closed"])

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Total Tickets", len(tickets))
    c2.metric("Open", open_t)
    c3.metric("Pending", pending_t)
    c4.metric("Closed", closed_t)


# def render_active_tickets(tickets):
#     st.subheader("📋 Active Tickets")

#     active = [t for t in tickets if t["status"] != "closed"]

#     if not active:
#         st.success("🎉 No active tickets")
#         return

#     for t in active:
#         with st.container(border=True):
#             st.markdown(f"### 🎫 {t['title']}")
#             st.markdown(status_badge(t["status"]))

#             col1, col2 = st.columns(2)
#             col1.write(f"**Priority:** {t['priority']}")
#             col2.write(f"**Customer ID:** {t['customer_id']}")

#             new_status = st.selectbox(
#                 "Change Status",
#                 ["open", "pending", "closed"],
#                 index=["open","pending","closed"].index(t["status"]),
#                 key=f"status_{t['id']}"
#             )

#             if st.button("✅ Update Status", key=f"upd_{t['id']}"):
#                 res = update_ticket_status(t["id"], new_status)
#                 if res.status_code == 200:
#                     st.success("Updated")
#                     st.rerun()
#                 else:
#                     st.error(res.text)



def render_active_tickets(tickets):
    st.subheader("📋 Active Tickets")

    active = [t for t in tickets if t["status"] != "closed"]

    if not active:
        st.success("🎉 No active tickets")
        return

    df = pd.DataFrame(active)
    
    # Priority sorting
    df["priority_rank"] = df["priority"].map(PRIORITY_ORDER)
    df = df.sort_values("priority_rank")

    df = df[[
        "id",
        "title",
        "description",
        "priority",
        "status",
        "assigned_agent",
        "customer_id",
        "created_at"
    ]]

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )

    for t in active:
        with st.container(border=True):
            st.markdown(f"### 🎫 {t['title']}")
            st.caption(f"Ticket ID: {t['id']}")

            st.markdown(f"**Description:** {t.get('description', '-')}")
            st.markdown(f"**Priority:** `{t['priority']}`")
            st.markdown(f"**Customer ID:** `{t['customer_id']}`")
            st.markdown(f"**Assigned Agent:** `{t['assigned_agent']}`")

            st.markdown(f"**Status:** {status_badge(t['status'])}")

            new_status = st.selectbox(
                "Change Status",
                ["open", "pending", "closed"],
                index=["open","pending","closed"].index(t["status"]),
                key=f"status_{t['id']}"
            )

            if st.button("✅ Update Status", key=f"upd_{t['id']}"):
                update_ticket_status(t["id"], new_status)
                st.rerun()


# def render_closed_tickets(tickets):
#     st.subheader("🗃 Closed Tickets (Read-Only)")

#     closed = [t for t in tickets if t["status"] == "closed"]

#     if not closed:
#         st.info("No closed tickets yet")
#         return

#     for t in closed:
#         with st.expander(f"⚫ {t['title']} (ID {t['id']})"):
#             st.write("Priority:", t["priority"])
#             st.write("Assigned Agent:", t["assigned_agent"])
#             st.write("Customer:", t["customer_id"])

#             if st.button("🗑 Permanently Delete", key=f"del_{t['id']}"):
#                 res = delete_ticket(t["id"], reason="Deleted by Team Lead")
#                 if res.status_code == 200:
#                     st.success("Deleted")
#                     st.rerun()
#                 else:
#                     st.error(res.text)


# def render_closed_tickets(tickets):
#     st.subheader("🗃 Closed Tickets")

#     closed = [t for t in tickets if t["status"] == "closed"]

#     if not closed:
#         st.info("No closed tickets yet")
#         return

#     for t in closed:
#         with st.expander(f"⚫ {t['title']} (ID {t['id']})"):
#             st.write("Description:", t.get("description", "-"))
#             st.write("Priority:", t["priority"])
#             st.write("Assigned Agent:", t["assigned_agent"])
#             st.write("Customer:", t["customer_id"])

#             if st.button("🗑 Permanently Delete", key=f"del_{t['id']}"):
#                 delete_ticket(t["id"], reason="Deleted by Team Lead")
#                 st.rerun()

PRIORITY_ORDER = {
    "high": 1,
    "medium": 2,
    "low": 3,
    "planned": 4,
    "investigation": 5
}


def render_closed_tickets(tickets):
    st.subheader("⚫ Closed Tickets")

    closed = [
        t for t in tickets
        if t["status"] == "closed"
    ]

    if not closed:
        st.info("No closed tickets yet")
        return

    df = pd.DataFrame(closed)
    
    df["priority_rank"] = df["priority"].map(PRIORITY_ORDER)
    df = df.sort_values("priority_rank")

    df = df[[
        "id",
        "title",
        "description",
        "priority",
        "assigned_agent",
        "customer_id",
        "created_at"
    ]]

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )



def normalize_tickets(data):
    """
    Ensures tickets is always a list of ticket dicts
    """
    if isinstance(data, list):
        return data

    if isinstance(data, dict) and "tickets" in data:
        return data["tickets"]

    return []


def render():
    if not is_logged_in() or st.session_state.role != "team_lead":
        st.error("Unauthorized")
        return

    st.title("📊 Team Lead Dashboard")

    tabs = st.tabs([
    "📋 All Tickets",
    "🔁 Assign / Reassign",
    "📈 Weekly Analytics"
    ])

    with tabs[0]:
        render_all_tickets()

    with tabs[1]:
        render_assignment()

    with tabs[2]:
        render_weekly_analytics()


def render_all_tickets():
    res = get_teamlead_tickets()

    if res.status_code != 200:
        st.error("Failed to load tickets")
        st.write(res.text)
        return

    tickets = res.json()["tickets"]

    active = [t for t in tickets if t["status"] != "closed"]
    closed = [t for t in tickets if t["status"] == "closed"]

    render_ticket_table(active, "🟢 Active Tickets")
    render_ticket_table(closed, "⚫ Closed Tickets")

    if "selected_ticket" in st.session_state:
        render_ticket_detail()
        render_status_update(st.session_state.selected_ticket)
        render_delete_ticket(st.session_state.selected_ticket)

    # render_kpis(tickets)
    # st.divider()
    # render_active_tickets(tickets)
    # st.divider()
    # render_closed_tickets(tickets)
    # render_active_tickets(tickets)
    # st.divider()

    # render_closed_tickets(tickets)
    # st.divider()

    render_tickets_per_customer(tickets, top_n=5)
    st.divider()

    render_customers_overview()


# def render_assignment():
#     st.subheader("🔁 Assign / Reassign Ticket")

#     # ---------- Load Support Agents ----------
#     agents_res = get_support_agents()
#     if agents_res.status_code != 200:
#         st.error("Failed to load support agents")
#         st.write(agents_res.text)
#         return

#     agents = agents_res.json()
#     if not agents:
#         st.info("No support agents available")
#         return

#     # ---------- Load Tickets ----------
#     tickets_res = get_teamlead_tickets()
#     if tickets_res.status_code != 200:
#         st.error("Failed to load tickets")
#         st.write(tickets_res.text)
#         return

#     # Normalize tickets (handles dict/list response)
#     tickets = normalize_tickets(tickets_res.json())

#     # 🔴 IMPORTANT: Only OPEN tickets can be assigned
#     tickets = [t for t in tickets if t["status"] == "open"]

#     if not tickets:
#         st.info("No OPEN tickets available for assignment")
#         return

#     # ---------- Dropdown Maps ----------
#     ticket_map = {
#         f"{t['title']} (ID {t['id']})": t["id"]
#         for t in tickets
#     }

#     agent_map = {
#         f"{a['name']} (ID {a['id']})": a["id"]
#         for a in agents
#     }

#     # ---------- Assign Form ----------
#     with st.form("assign_ticket_form"):
#         ticket_label = st.selectbox(
#             "🎫 Select Ticket",
#             list(ticket_map.keys())
#         )

#         agent_label = st.selectbox(
#             "👤 Assign to Support Agent",
#             list(agent_map.keys())
#         )

#         submitted = st.form_submit_button("✅ Assign Ticket")

#         if submitted:
#             res = assign_ticket(
#                 ticket_id=ticket_map[ticket_label],
#                 agent_id=agent_map[agent_label]
#             )

#             if res.status_code == 200:
#                 st.success("Ticket assigned successfully")
#                 st.rerun()
#             else:
#                 st.error("Assignment failed")
#                 st.write(res.text)


def render_assignment():
    st.subheader("🔁 Assign / Reassign Ticket")

    agents = get_support_agents().json()
    tickets = normalize_tickets(get_teamlead_tickets().json())

    open_tickets = [t for t in tickets if t["status"] == "open"]

    if not open_tickets:
        st.info("No OPEN tickets available for assignment")
        return

    ticket_map = {f"{t['title']} (ID {t['id']})": t["id"] for t in open_tickets}
    agent_map = {f"{a['name']} (ID {a['id']})": a["id"] for a in agents}

    with st.form("assign_form"):
        st.selectbox("🎫 Ticket", ticket_map.keys(), key="assign_ticket")
        st.selectbox("👤 Support Agent", agent_map.keys(), key="assign_agent")

        if st.form_submit_button("✅ Assign Ticket"):
            assign_ticket(
                ticket_map[st.session_state.assign_ticket],
                agent_map[st.session_state.assign_agent]
            )
            st.success("Ticket assigned successfully")
            st.rerun() 


def render_stacked_chart(df):
    st.markdown("### 📊 Ticket Status Distribution")

    chart_data = df.melt(
        id_vars=["date", "agent_name"],
        value_vars=["opened", "pending", "closed"],
        var_name="status",
        value_name="count"
    )

    chart = (
        alt.Chart(chart_data)
        .mark_bar()
        .encode(
            x=alt.X("date:T", title="Date"),
            y=alt.Y("count:Q", title="Tickets"),
            color=alt.Color(
                "status:N",
                scale=alt.Scale(
                    domain=["opened", "pending", "closed"],
                    range=["#1f77b4", "#ff7f0e", "#2ca02c"]
                ),
                title="Status"
            ),
            tooltip=[
                "agent_name",
                "status",
                "count",
                alt.Tooltip("date:T", title="Date")
            ]
        )
        .properties(height=400)
    )

    st.altair_chart(chart, use_container_width=True)


def render_weekly_analytics():
    st.subheader("📈 Weekly Agent Performance")

    res = get_weekly_analytics()

    if res.status_code != 200:
        st.error("Failed to load analytics")
        st.write(res.text)
        return

    data = res.json()

    if not data:
        st.info("No analytics data available")
        return

    # ---------- Convert to DataFrame ----------
    df = pd.DataFrame(data)
    df["date"] = pd.to_datetime(df["date"])

    # ---------- Agent Filter ----------
    agent_options = ["All Agents"] + sorted(df["agent_name"].unique().tolist())

    selected_agent = st.selectbox(
        "👤 Filter by Support Agent",
        agent_options
    )

    if selected_agent != "All Agents":
        df = df[df["agent_name"] == selected_agent]

    # ---------- Show Table ----------
    st.markdown("### 📋 Weekly Breakdown")
    st.dataframe(
        df[["date", "agent_name", "opened", "pending", "closed"]],
        use_container_width=True
    )

    # ---------- Stacked Bar Chart ----------
    render_stacked_chart(df)


def render_tickets_per_customer(tickets, top_n=5):
    st.subheader(f"🏢 Top {top_n} Customers by Ticket Volume")

    df = pd.DataFrame(tickets)

    if df["customer_id"].isnull().all():
        st.info("No customer-linked tickets")
        return

    customer_counts = (
        df.groupby("customer_id")
          .size()
          .reset_index(name="tickets")
          .sort_values("tickets", ascending=False)
          .head(top_n)
    )

    st.dataframe(customer_counts, use_container_width=True)


def render_customers_overview():
    st.subheader("👥 Customers (All Support-Created)")

    res = get_customers()

    if res.status_code != 200:
        st.error("Failed to load customers")
        return

    customers = res.json()

    if not customers:
        st.info("No customers found")
        return

    df = pd.DataFrame(customers)

    df = df[[
        "id",
        "name",
        "email",
        "company",
        "created_by_agent_id"
    ]]

    st.dataframe(df, use_container_width=True)


def render_ticket_table(tickets, title):
    st.subheader(title)

    if not tickets:
        st.info("No tickets found")
        return

    for t in tickets:
        col1, col2, col3, col4 = st.columns([4, 2, 2, 1])

        col1.write(f"🎫 **{t['title']}**")
        col2.write(t["priority"].upper())
        col3.write(t["status"].upper())

        if col4.button("View", key=f"view_{t['id']}"):
            st.session_state.selected_ticket = t


def render_ticket_detail():
    ticket = st.session_state.get("selected_ticket")
    if not ticket:
        return

    st.divider()
    st.subheader("📄 Ticket Details")

    st.markdown(f"### 🎫 {ticket['title']}")
    st.write("**Description:**")
    st.info(ticket["description"])

    col1, col2, col3 = st.columns(3)
    col1.write(f"**Status:** {ticket['status']}")
    col2.write(f"**Priority:** {ticket['priority']}")
    col3.write(f"**Customer ID:** {ticket['customer_id']}")

    st.write(f"**Assigned Agent:** {ticket['assigned_agent']}")
    st.write(f"**Created At:** {ticket['created_at']}")


def render_status_update(ticket):
    if ticket["status"] == "closed":
        return

    new_status = st.selectbox(
        "Update Status",
        ["open", "pending", "closed"],
        index=["open", "pending", "closed"].index(ticket["status"])
    )

    if st.button("✅ Update Status"):
        res = update_ticket_status(ticket["id"], new_status)
        if res.status_code == 200:
            st.success("Status updated")
            st.session_state.selected_ticket = None
            st.rerun()
        else:
            st.error(res.text)


def render_delete_ticket(ticket):
    st.divider()
    st.subheader("🗑 Delete Ticket")

    reason = st.text_area(
        "Deletion Reason (Required)",
        placeholder="Explain why this ticket is being deleted..."
    )

    if st.button("❌ Delete Ticket"):
        if not reason.strip():
            st.error("Deletion reason is mandatory")
            return

        res = delete_ticket(ticket["id"], reason=reason)

        if res.status_code == 200:
            st.success("Ticket deleted")
            st.session_state.selected_ticket = None
            st.rerun()
        else:
            st.error(res.text)
