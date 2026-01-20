from pydantic import BaseModel, EmailStr
from enum import Enum


class UserRole(str,Enum):
    employee = "employee"
    support = "support"
    team_lead = "team_lead"

class UserBase(BaseModel):
    emp_id: str
    name : str
    email_id: EmailStr
    role : UserRole
    dept_id : int
    

class UserCreate(UserBase):
    # email : str
    # emp_id : str
    # role : str
    pass 

class UserResponse(UserBase):
    id : int
    # name : str
    # emp_id : str
    # role : Enum
    
    class Config:
        orm_mode = True
