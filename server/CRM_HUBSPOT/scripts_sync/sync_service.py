from server.db_connect.db_config import Sessionlocal
from server.models.db_model import Ticket
from server.CRM_HUBSPOT.payloads import build_ticket_payload
from server.CRM_HUBSPOT.config import create_ticket_in_crm

def sync_all_tickets_to_crm():
    print("🚀 Starting bulk CRM sync...")

    db = Sessionlocal()

    try:
        tickets = (
            db.query(Ticket)
            .filter(Ticket.hubspot_ticket_id == None)
            .all()
        )

        print(f"🔍 Found {len(tickets)} unsynced tickets")

        for ticket in tickets:
            try:
                print(f"➡️ Syncing ticket {ticket.id}")

                # payload = build_ticket_payload(ticket)
                hubspot_id = create_ticket_in_crm(ticket)

                ticket.hubspot_ticket_id = hubspot_id
                db.commit()

                print(f"✅ Ticket {ticket.id} synced (HubSpot ID: {hubspot_id})")

            except Exception as e:
                db.rollback()
                print(f"❌ Failed to sync ticket {ticket.id}: {e}")

    finally:
        db.close()

    print("🎉 CRM sync completed")
