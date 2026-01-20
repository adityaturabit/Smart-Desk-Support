from server.db_connect.db_config import Sessionlocal
from fastapi import Header , Depends, HTTPException,status
from sqlalchemy.orm import Session
from server.models.db_model import User, Customer
from server.db_connect.redis_conn.redis_client import redis_client
#fastapi dependencies allows us to inject a database session per request
 
def get_db():
    db = Sessionlocal()
    try:
        yield db
    finally:
        db.close()


#------------to get USERS
def get_current_user(x_session_id : str = Header(...,alias="X-SESSION-ID"),
    db : Session = Depends(get_db)
    ) -> User:

    try:
        user_id = redis_client.get(f"session:{x_session_id}")
        # print("SESSION HEADER RECEIVED:", x_session_id)

        # value = redis_client.get(f"session:{x_session_id}")
        # print("SESSION VALUE IN REDIS:", value)

        if not user_id:
            raise HTTPException(status_code=401,detail="Session expired or Invalid")
        
        user = db.query(User).filter(User.id == int(user_id)).first()
        

        if not user:
            raise HTTPException(status_code=401, detail="User not found")
        return user
    except HTTPException as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail=str(e))


#--------------to get Customers which can be accessed by agents and team lead only

# def get_current_customers(
#         current_user : User = Depends(get_current_user),
#         db: Session = Depends(get_db)
# ) -> List[Customer]:
    
#     if current_user.role == "employee":
#         raise HTTPException(status_code=401,detail="Only for the Authorized members")
    
#     if current_user.role == "support":
#         return (
#             db.query(Customer).filter(Customer.created_by_agent_id == current_user.id).all()
#         )
    
#     #for team lead
#     return db.query(Customer).all()