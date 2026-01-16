from sqlalchemy.orm import Session
from server.models.db_model import User
from server.db_connect.redis_conn.redis_client import redis_client

def assign_next_agent(db:Session) -> int | None:
    agents = (
        db.query(User).filter(User.role == "support").order_by(User.id).all()
    )

    if not agents:
        return None
    
    last_id = redis_client.get("round_robin:last_agent_id")
    agent_ids = [a.id for a in agents]

    if not last_id or int(last_id) not in agent_ids:
        next_agent = agents[0]
    else:
        idx = agent_ids.index(int(last_id))
        next_agent = agents[(idx + 1)%len(agents)]

    redis_client.set("round_robin:last_agent_id", next_agent.id)
    return next_agent.id