import requests
import streamlit as st

BASE_URL = "http://127.0.0.1:8000"

def headers():
    return {
        "X-SESSION-ID": st.session_state.session_id
    }

def create_ticket(data):
    return requests.post(
        f"{BASE_URL}/tickets",
        json=data,
        headers=headers()
    )

def get_my_tickets():
    return requests.get(
        f"{BASE_URL}/tickets/",
        headers=headers()
    )

# 🔹 Support: get assigned tickets
def get_assigned_tickets():
    return requests.get(
        f"{BASE_URL}/tickets/",
        headers=headers()
    )

# 🔹 Update ticket status
def update_ticket_status(ticket_id, status):
    return requests.patch(
        f"{BASE_URL}/tickets/{ticket_id}/status",
        json={"status": status},
        headers=headers()
    )

# 🔹 Delete ticket (with optional reason)
def delete_ticket(ticket_id, reason=None):
    payload = {}
    if reason:
        payload["reason"] = reason

    return requests.delete(
        f"{BASE_URL}/tickets/{ticket_id}",
        json=payload,
        headers=headers()
    )

def get_all_tickets():
    return requests.get(
        f"{BASE_URL}/tickets",
        headers=headers()
    )


def assign_ticket(ticket_id, agent_id):
    return requests.patch(
        f"{BASE_URL}/tickets/{ticket_id}/assign",
        json={"agent_id": agent_id},
        headers=headers()
    )


def get_weekly_analytics():
    return requests.get(
        f"{BASE_URL}/analytics/weekly",
        headers=headers()
    )


def get_teamlead_tickets():
    return requests.get(
        f"{BASE_URL}/analytics/team-lead/summary",
        headers=headers()
    )
