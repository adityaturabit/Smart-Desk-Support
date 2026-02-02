
PRIORITY_MAP = {
    "low": "LOW",
    "medium": "MEDIUM",
    "high": "HIGH"
    }
STATUS_TO_STAGE = {
"open": "1",
"pending": "2",
"closed": "3"
}

def build_ticket_payload(ticket) -> dict:
    propertie = {
            "subject":ticket.title,
            "content": ticket.description,
            "hs_ticket_priority" : PRIORITY_MAP[ticket.priority.lower()],
            "hs_pipeline_stage" : "1",
            "hs_pipeline":"0",
            # "hs_created_by_user_id" : str(ticket["created_by_user_id"]),
            # "createdate": ticket["created_at"],
            # "hs_lastmodifieddate": ticket["updated_at"],
            "internal_ticket_id": str(ticket.id)
    }
    properties = { k:v for k,v in propertie.items() if v is not None}
    return properties