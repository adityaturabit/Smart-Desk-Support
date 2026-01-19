import requests
import streamlit as st

BASE_URL = "http://127.0.0.1:8000"

def headers():
    return {"X-SESSION-ID": st.session_state.session_id}

def create_customer(data):
    return requests.post(
        f"{BASE_URL}/customers/",
        json=data,
        headers=headers()
    )

def get_customers():
    return requests.get(
        f"{BASE_URL}/customers/",
        headers=headers()
    )

def update_customer(customer_id, data):
    return requests.put(
        f"{BASE_URL}/customers/{customer_id}",
        json=data,
        headers=headers()
    )

def delete_customer(customer_id):
    return requests.delete(
        f"{BASE_URL}/customers/{customer_id}",
        headers=headers()
    )

def get_support_agents():
    return requests.get(
        f"{BASE_URL}/users/support",
        headers=headers()
    )
