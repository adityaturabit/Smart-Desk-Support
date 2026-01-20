import streamlit as st
from api_backen.ticket_api import get_teamlead_tickets,assign_ticket,get_weekly_analytics,delete_ticket,update_ticket_status
from utils.state import is_logged_in
from api_backen.customer_api import get_support_agents


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

# def render_all_tickets():
#     res = get_teamlead_tickets()
    
#     if res.status_code != 200:
#         st.error("Failed to load tickets")
#         st.write(res.text)
#         return

#     tickets = normalize_tickets(res.json())

#     if not tickets:
#         st.info("No tickets found")
#         return

#     for t in tickets:
#         with st.expander(f"🎫 {t['title']} [{t['status']}]"):
#             st.write("Priority:", t["priority"])
#             st.write("Assigned Agent:", t.get("assigned_agent"))
#             st.write("Created By:", t.get("created_by_user_id"))
#             st.write("Customer:", t.get("customer_id"))

#         if t["status"] == "closed":
#             if st.button(f"🗑 Delete Ticket {t['id']}", key=f"del_{t['id']}"):
#                 res = delete_ticket(t["id"])
#                 if res.status_code == 200:
#                     st.success("Deleted")
#                     st.rerun()
#                 else:
#                     st.error(res.text)

def render_all_tickets():
    res = get_teamlead_tickets()

    if res.status_code != 200:
        st.error(res.text)
        return

    data = res.json()["tickets"]

    for t in data:
        with st.expander(f"🎫 {t['title']} [{t['status']}]"):
            st.write("Priority:", t["priority"])
            st.write("Assigned Agent:", t["assigned_agent"])
            st.write("Customer:", t["customer_id"])

            new_status = st.selectbox(
                "Change Status",
                ["open", "pending", "closed"],
                index=["open","pending","closed"].index(t["status"]),
                key=f"status_{t['id']}"
            )

            if st.button("Update Status", key=f"btn_{t['id']}"):
                update_ticket_status(t["id"], new_status)
                if res.status_code == 200:
                    st.success("Status updated")
                    st.rerun()
                else:
                    st.error(res.text)

            if t["status"] == "closed":
                if st.button("🗑 Delete", key=f"del_{t['id']}"):
                    delete_ticket(t["id"], reason="Deleted by Team Lead")
                    st.rerun()


# def render_assignment():
#     st.subheader("Assign / Reassign Ticket")

#     agents_res = get_support_agents()
#     if agents_res.status_code != 200:
#         st.error("Failed to load support agents")
#         return
#     agents = agents_res.json()

#     tickets_res = get_teamlead_tickets()
#     if tickets_res.status_code != 200:
#         st.error("Failed to load tickets")
#         st.write(tickets_res.text)
#         return

#     tickets = normalize_tickets(tickets_res.json())
#     tickets = [t for t in tickets if t["status"] == "open"]

#     if not tickets:
#         st.info("No OPEN tickets available for assignment")
#         return

#     ticket_map = {
#         f"{t['title']} (ID {t['id']})": t["id"]
#         for t in tickets
#     }

#     agent_map = {
#         f"{a['name']} (ID {a['id']})": a["id"]
#         for a in agents
#     }

#     with st.form("assign_ticket_form"):
#         ticket_label = st.selectbox("Ticket", list(ticket_map.keys()))
#         agent_label = st.selectbox("Support Agent", list(agent_map.keys()))

#         if st.form_submit_button("Assign"):
#             res = assign_ticket(
#                 ticket_map[ticket_label],
#                 agent_map[agent_label]
#             )

#             if res.status_code == 200:
#                 st.success("Ticket assigned")
#                 st.rerun()
#             else:
#                 st.error(res.text)

def render_assignment():
    st.subheader("🔁 Assign / Reassign Ticket")

    # ---------- Load Support Agents ----------
    agents_res = get_support_agents()
    if agents_res.status_code != 200:
        st.error("Failed to load support agents")
        st.write(agents_res.text)
        return

    agents = agents_res.json()
    if not agents:
        st.info("No support agents available")
        return

    # ---------- Load Tickets ----------
    tickets_res = get_teamlead_tickets()
    if tickets_res.status_code != 200:
        st.error("Failed to load tickets")
        st.write(tickets_res.text)
        return

    # Normalize tickets (handles dict/list response)
    tickets = normalize_tickets(tickets_res.json())

    # 🔴 IMPORTANT: Only OPEN tickets can be assigned
    tickets = [t for t in tickets if t["status"] == "open"]

    if not tickets:
        st.info("No OPEN tickets available for assignment")
        return

    # ---------- Dropdown Maps ----------
    ticket_map = {
        f"{t['title']} (ID {t['id']})": t["id"]
        for t in tickets
    }

    agent_map = {
        f"{a['name']} (ID {a['id']})": a["id"]
        for a in agents
    }

    # ---------- Assign Form ----------
    with st.form("assign_ticket_form"):
        ticket_label = st.selectbox(
            "🎫 Select Ticket",
            list(ticket_map.keys())
        )

        agent_label = st.selectbox(
            "👤 Assign to Support Agent",
            list(agent_map.keys())
        )

        submitted = st.form_submit_button("✅ Assign Ticket")

        if submitted:
            res = assign_ticket(
                ticket_id=ticket_map[ticket_label],
                agent_id=agent_map[agent_label]
            )

            if res.status_code == 200:
                st.success("Ticket assigned successfully")
                st.rerun()
            else:
                st.error("Assignment failed")
                st.write(res.text)


def render_weekly_analytics():
    st.subheader("Weekly Agent Stats")

    res = get_weekly_analytics()

    if res.status_code != 200:
        st.error("Failed to load analytics")
        return

    data = res.json()

    st.dataframe(data)



