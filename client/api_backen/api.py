import requests
import streamlit as st

BASE_URL = "http://127.0.0.1:8000"

def post(endpoint, payload):
    headers = {}
    if "session_id" in st.session_state:
        headers["X-SESSION-ID"] = st.session_state["session_id"]

    return requests.post(
        f"{BASE_URL}{endpoint}",
        json=payload,
        headers=headers
    )
