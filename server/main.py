from fastapi import FastAPI, HTTPException, Depends, Header
from server.db_connect.db_config import Base,engine
from sqlalchemy.orm import Session
from server.models.db_model import Dept,User
from server.schemas.user_schema import UserResponse, UserCreate
from server.schemas.auth_schema import LoginReq
from server.dependencies import get_db
from server.routers import customer_route,ticket_route, analytics_route
import uuid
from server.db_connect.redis_conn.redis_client import redis_client
from server.routers import user_route
from fastapi.middleware.cors import CORSMiddleware



app = FastAPI(title="Smart Support Desk",tags=["WOW"])

app.add_middleware(CORSMiddleware,allow_origins = ["*"],allow_methods = ["*"])

@app.on_event("startup")
def start_up():
    # Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind = engine)


@app.get("/")
def landing_page():
    return "LANDING PAGE"

#for the registration of the employee,support,team_lead of the company
@app.post("/register",response_model=UserResponse)
def register(user: UserCreate, db:Session = Depends(get_db)):
    existing = db.query(User).filter(User.emp_id == user.emp_id).first()

    if existing:
        return HTTPException(status_code=400,detail="User already exists")
    
    dept = db.query(Dept).filter(Dept.dept_id == user.dept_id).first()

    if not dept:
        raise HTTPException(status_code = 404,detail = ["Department not found"])

    new_user = User(
        emp_id = user.emp_id,
        name = user.name,
        email_id = user.email_id,
        role = user.role,
        dept_id = user.dept_id
    )
    # use = db.query(User).first()
    # print(use.department.dept_name)

    # dep = db.query(Dept).first()
    # print([u.name for u in dep.users])

    db.add(new_user)
    db.commit()
    db.flush()
    return new_user


# >>>>>>>>>>>>>>>> LOGIN
@app.post("/login")
def login(payload: LoginReq,db: Session = Depends(get_db)):
    
    existing_user1 = db.query(User).filter(User.emp_id == payload.emp_id).first()
    existing_user = db.query(User).filter(User.email_id == payload.email_id).first()

    if not existing_user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    if not existing_user1:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    session_id = str(uuid.uuid4())

    redis_client.setex(
        f"session:{session_id}",
        3600, # it means 1 hour
        existing_user.id
    )
    print("SESSION STORED:", f"session:{session_id}")
    
    return {
        "session_id":session_id,
        "role" : existing_user.role,
        "name": existing_user.name,
        "emp_id": existing_user.emp_id,
        "dept_name": existing_user.department.dept_name if existing_user.department else None
    }


app.include_router(customer_route.router)
app.include_router(ticket_route.router)
app.include_router(analytics_route.router)
app.include_router(user_route.router)

#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>LOGOUT
@app.post("/logout")
def logout(x_session_id: str = Header(..., alias="X-SESSION-ID")):
    redis_client.delete(f"session:{x_session_id}")
    return {"message": "Logged out successfully"}




# @app.post("/test-user",response_model=UserResponse)
# def test_user(user: UserCreate):
#     fake_user = {
#         "id":1,
#         "emp_id": user.emp_id,
#         "email_id": user.email_id,
#         "role":user.role
#     }
#     return fake_user