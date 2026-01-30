import requests

BASE_URL = "http://127.0.0.1:8000"

def login(emp_id: str, email: str,password:str):
    payload = {
        "emp_id": emp_id,
        "email_id": email,
        "password": password
    }
    res = requests.post(f"{BASE_URL}/login", json=payload)
    return res


def register(payload: dict):
    return requests.post(f"{BASE_URL}/register", json=payload)
