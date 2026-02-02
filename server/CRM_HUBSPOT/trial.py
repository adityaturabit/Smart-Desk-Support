from server.db_connect.db_config import Sessionlocal
from server.models.db_model import Ticket 
from server.CRM_HUBSPOT.config import Hubspotsync
from server.CRM_HUBSPOT.payloads import build_ticket_payload
import os

async def sync_ticket_to_crm(ticket_id: int):
    print(f"[CRM SYNC] Starting sync for ticket {ticket_id}")
    db = Sessionlocal()

    try:

        ticket = db.get(Ticket, ticket_id)
        
        if ticket is None:
            print(f"Ticket {ticket_id} not found. Skipping CRM sync.")
            return

        if ticket.hubspot_ticket_id:
            print(f"Ticket {ticket_id} already synced.")
            return
        
        payload = build_ticket_payload(ticket)
        
        HUBSPOT_TOKEN = os.getenv("HUBSPOT_TOKEN")

        hubspot = Hubspotsync(HUBSPOT_TOKEN)
        print("HUBSPOT PAYLOAD:", payload)
        hubspott_id = await hubspot.create_ticket_in_crm(payload)
        

        ticket.hubspot_ticket_id = hubspott_id
        db.commit()

        print(f"Ticket {ticket_id} synced to CRM.")

    except Exception as e:
        db.rollback()
        print("CRM sync failed:", e)

    finally:
        db.close()








# from server.db_connect.db_config import Sessionlocal
# from server.models.db_model import Ticket
# # from sqlalchemy.orm import Session
# from server.CRM_HUBSPOT.config import create_ticket_in_crm

# def sync_ticket_to_crm(ticket_id : int):
#     db = Sessionlocal()

#     try:
#         ticket = db.get(Ticket,ticket_id)

#         if ticket.hubspot_ticket_id:
#             return
        
#         crm_id = create_ticket_in_crm({
#             "id": ticket.id,
#             "title": ticket.title,
#             "description": ticket.description,
#             "priority": ticket.priority,
#         })

#         ticket.hubspot_ticket_id = crm_id
#         db.commit()

#     except Exception as e:
#         db.rollback()
#         print("CRM sync failed:", e)

#     finally:
#         db.close()