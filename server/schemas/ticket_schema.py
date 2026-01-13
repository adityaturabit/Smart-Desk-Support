from pydantic import BaseModel
from typing import Optional
from enum import Enum
from datetime import datetime

class TicketPriority(str,Enum):
    low = "low"
    medium = "medium"
    high = "high"
    planned = "planned"
    investigation = "investigation"

class TicketStatus(str,Enum):
    open = "open"
    pending = "pending"
    closed = "closed"

class TicketBase(BaseModel):
    title : str
    description : str
    priority : TicketPriority = TicketPriority.medium

class CreateTicket(TicketBase):
    customer_id : Optional[int] = None

class UpdateTicket(BaseModel):
    status : TicketStatus

class TicketResponse(TicketBase):
    id : int
    status : TicketStatus
    created_by_user_id : int
    assigned_agent : Optional[int]
    customer_id : Optional[int]
    created_at : datetime

    class Config:
        from_attributes = True

class TicketDeleteRequest(BaseModel):
    reason: Optional[str] = None


class AssignTicketRequest(BaseModel):
    agent_id: int
