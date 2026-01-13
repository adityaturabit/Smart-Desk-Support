from pydantic import BaseModel
from datetime import date

class AgentDailyStatus(BaseModel):
    agent_id : int
    agent_name : str
    date : date
    opened : int
    pending: int
    closed: int
