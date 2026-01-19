import streamlit as st
from api_backen.ticket_api import get_all_tickets,assign_ticket,get_weekly_analytics,delete_ticket
from utils.state import is_logged_in
from api_backen.customer_api import get_support_agents



def render_all_tickets():
    res = get_all_tickets()

    if res.status_code != 200:
        st.error("Failed to load tickets")
        return

    tickets = res.json()

    if not tickets:
        st.info("No tickets found")
        return

    for t in tickets:
        with st.expander(f"🎫 {t['title']} [{t['status']}]"):
            st.write("Priority:", t["priority"])
            st.write("Assigned Agent:", t["assigned_agent"])
            st.write("Created By:", t["created_by_user_id"])
            st.write("Customer:", t["customer_id"])
        if t["status"] == "closed":
            if st.button(f"🗑 Delete Ticket {t['id']}"):
                res = delete_ticket(t["id"])
                if res.status_code == 200:
                    st.success("Deleted")
                    st.rerun()
                else:
                    st.error("Delete failed")


def render_assignment():
    st.subheader("Assign / Reassign Ticket")
    agents_res = get_support_agents()

    if agents_res.status_code != 200:
        st.error("Failed to load support agents")
        return

    agents = agents_res.json()
    tickets = get_all_tickets().json()
    # agents = get_support_agents().json()

    ticket_map = {
        f"{t['title']} (ID {t['id']})": t["id"]
        for t in tickets
    }

    agent_map = {
        f"{a['name']} (ID {a['id']})": a["id"]
        for a in agents
    }

    with st.form("assign_ticket_form"):
        ticket_label = st.selectbox("Ticket", ticket_map.keys())
        agent_label = st.selectbox("Support Agent", agent_map.keys())

        if st.form_submit_button("Assign"):
            res = assign_ticket(
                ticket_map[ticket_label],
                agent_map[agent_label]
            )

            if res.status_code == 200:
                st.success("Ticket assigned")
                st.rerun()
            else:
                st.error("Assignment failed")

def render_weekly_analytics():
    st.subheader("Weekly Agent Stats")

    res = get_weekly_analytics()

    if res.status_code != 200:
        st.error("Failed to load analytics")
        return

    data = res.json()

    st.dataframe(data)


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
