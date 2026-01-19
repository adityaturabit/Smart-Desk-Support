import streamlit as st
from api_backen.ticket_api import get_assigned_tickets,update_ticket_status,delete_ticket,create_ticket,get_my_tickets
from api_backen.customer_api import create_customer,get_customers,delete_customer,update_customer

def render():
    st.header("🛠️ Support Agent Dashboard")

    tab1, tab2 = st.tabs(["🎫 Tickets", "👥 Customers"])


    # TICKETS
    with tab1:
        st.subheader("Create Ticket (Support)")

        cust_res = get_customers()

        if cust_res.status_code != 200:
            st.error("Unable to load customers")
        else:
            customers = cust_res.json()

            if not customers:
                st.warning("Create a customer first")
            else:
                customer_map = {
                    f"{c['name']} ({c.get('company', '-')})": c["id"]
                    for c in customers
                }

                with st.form("support_create_ticket"):
                    title = st.text_input("Title")
                    description = st.text_area("Description")
                    priority = st.selectbox(
                        "Priority",
                        ["low", "medium", "high", "planned", "investigation"]
                    )
                    customer_label = st.selectbox(
                        "Customer",
                        list(customer_map.keys())
                    )

                    if st.form_submit_button("Create Ticket"):
                        payload = {
                            "title": title,
                            "description": description,
                            "priority": priority,
                            "customer_id": customer_map[customer_label]
                        }

                        res = create_ticket(payload)

                        if res.status_code == 200:
                            st.success("Ticket created")
                            st.rerun()
                        else:
                            st.error("Ticket creation failed")
        st.subheader("Assigned Tickets")

        res = get_assigned_tickets()
        if res.status_code != 200:
            st.error("Failed to load tickets")
            return

        tickets = res.json()

        if not tickets:
            st.info("No tickets assigned")
        else:
            for t in tickets:
                with st.expander(f"ID: {t['id']} | Title: {t['title']}"):
                    st.write(f"Description: {t["description"]}")
                    st.write(f"Priority: {t['priority']}")
                    st.write(f"Status: {t['status']}")

                    # 🔁 STATUS UPDATE
                    new_status = st.selectbox(
                        "Update Status",
                        ["open", "pending", "closed"],
                        index=["open", "pending", "closed"].index(t["status"]),
                        key=f"status_{t['id']}"
                    )

                    if st.button("Update Status", key=f"btn_status_{t['id']}"):
                        update_ticket_status(t["id"], new_status)
                        st.success("Status updated")
                        st.rerun()

                    # DELETE RULE
                    if t["status"] == "closed":
                        if st.button("Delete Ticket", key=f"del_{t['id']}"):
                            delete_ticket(t["id"])
                            st.success("Ticket deleted")
                            st.rerun()
                    else:
                        reason = st.text_input(
                            "Deletion Reason",
                            key=f"reason_{t['id']}"
                        )
                        if st.button("Request Delete", key=f"req_del_{t['id']}"):
                            if not reason:
                                st.warning("Reason required")
                            else:
                                delete_ticket(t["id"], reason)
                                st.success("Delete request sent")


    # CUSTOMERS
    with tab2:
        st.subheader("Customers")

        with st.form("create_customer"):
            name = st.text_input("Name")
            email = st.text_input("Email")
            company = st.text_input("Company")

            if st.form_submit_button("Create Customer"):
                res = create_customer({
                    "name": name,
                    "email": email,
                    "company": company
                })

                if res.status_code == 200:
                    st.success("Customer created")
                    st.rerun()
                else:
                    st.error("Failed to create customer")

        st.divider()

        # 🔹 LIST + UPDATE + DELETE
        res = get_customers()

        if res.status_code != 200:
            st.error("Failed to load customers")
        else:
            customers = res.json()

            if not customers:
                st.info("No customers found")

            for c in customers:
                with st.expander(f"👤 {c['name']} ({c.get('company', '-')})"):

                    # EDIT FORM
                    new_name = st.text_input(
                        "Name",
                        value=c["name"],
                        key=f"name_{c['id']}"
                    )
                    new_email = st.text_input(
                        "Email",
                        value=c.get("email", ""),
                        key=f"email_{c['id']}"
                    )
                    new_company = st.text_input(
                        "Company",
                        value=c.get("company", ""),
                        key=f"company_{c['id']}"
                    )

                    col1, col2 = st.columns(2)

                    with col1:
                        if st.button("Update", key=f"update_{c['id']}"):
                            res = update_customer(
                                c["id"],
                                {
                                    "name": new_name,
                                    "email": new_email,
                                    "company": new_company
                                }
                            )

                            if res.status_code == 200:
                                st.success("Customer updated")
                                st.rerun()
                            else:
                                st.error("Update failed")

                    with col2:
                        if st.button("Delete", key=f"delete_{c['id']}"):
                            delete_customer(c["id"])
                            st.success("Customer deleted")
                            st.rerun()