from pydantic import BaseModel
from typing import List, Dict

class EmployeeTicketSummary(BaseModel):
    total_tickets: int
    tickets: List[dict]


class SupportCustomerTicketCount(BaseModel):
    customer_id: int
    customer_name: str
    ticket_count: int


class SupportTicketSummary(BaseModel):
    total_tickets: int
    tickets_by_customer: List[SupportCustomerTicketCount]


class TeamLeadTicketSummary(BaseModel):
    total_tickets: int
    tickets: List[dict]
