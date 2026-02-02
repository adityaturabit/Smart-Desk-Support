import os
from dotenv import load_dotenv
import requests
from server.CRM_HUBSPOT.payloads import build_ticket_payload
import httpx

load_dotenv()

HUBSPOT_TOKEN = os.getenv("HUBSPOT_TOKEN")
BASE_URL = "https://api.hubapi.com"

headers ={
    "Authorization": f"Bearer {HUBSPOT_TOKEN}",
    "Content-Type" : "application/json"
}
class Hubspotsync:
    def __init__(self, token) :
        self.headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type" : "application/json"
          }

    async def create_ticket_in_crm(self,payload : dict)-> str:
        async with httpx.AsyncClient(timeout=10) as client:
             response = await client.post(
                  f"{BASE_URL}/crm/v3/objects/tickets",
                  headers= self.headers,
                  json= {"properties":payload})

        if response.status_code >= 429:
            print(response.text)
            raise Exception("Hubspot rate limit exceeded")
        
        response.raise_for_status()
        return response.json()["id"]

# response =  requests.get(f"{BASE_URL}/crm/v3/objects/tickets",headers=headers)

def create_ticket_in_crm(ticket):
    url = f"{BASE_URL}/crm/v3/objects/tickets"


    payload =  build_ticket_payload(ticket)

    response = requests.post(url,headers=headers,json={"properties":payload})
    hubspot_id = response.json().get("id")
    if not hubspot_id:
        raise Exception(f"HubSpot did not return an ID: {response.text}")
    if response.status_code >= 400:
            print("HubSpot error:", response.status_code)
            print(response.text)

    return response.json()["id"]