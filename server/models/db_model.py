from sqlalchemy import Column,String,Integer, FLOAT,Enum,ForeignKey, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from server.db_connect.db_config import Base

class Dept(Base):
    __tablename__ = "depts"
    dept_id = Column(Integer, autoincrement=True,primary_key=True)
    dept_name = Column(String(30),nullable=False)
    dept_code = Column(String(10),unique=True, nullable=False)
    users = relationship("User",back_populates="department")

# USER MODEL FOR LOGIN & LOGOUT
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(30),nullable=False)
    emp_id = Column(String(10),unique=True,nullable=False, index=True)
    email_id = Column(String(20), unique=True,nullable=False)
    dept_id = Column(Integer,ForeignKey("depts.dept_id"))
    role = Column(Enum("employee","support","team_lead",name="user_roles"),nullable=False)
    department = relationship("Dept", back_populates="users")
    password_hash = Column(String(255),nullable=False)

# CUSTOMER MODEL AFTER A AGENT LOGS IN
class Customer(Base):
    __tablename__ = "customers"
    id = Column(Integer,autoincrement=True,primary_key=True, index=True)
    name = Column(String(30),nullable=False)
    email = Column(String(50),nullable=True)
    company = Column(String(50),nullable=True)
    created_by_agent_id = Column(Integer,ForeignKey("users.id"),nullable=False)
    created_by_agent_name = Column(String(50),nullable=False)


# ----- TICKET MODEL

class Ticket(Base):
    __tablename__ = "tickets"
    id = Column(Integer, autoincrement=True,primary_key=True)
    title =Column(String(250),nullable=False)
    description = Column(String(500),nullable=False)
    priority = Column(Enum("low","medium","high","planned","investigation",name="Ticket Priority"),default="medium",nullable=False)
    status = Column(Enum("open","pending","closed",name="Ticket Status"),default="open",nullable=False)
    created_by_user_id = Column(Integer,ForeignKey("users.id"),nullable=False)
    assigned_agent = Column(Integer,ForeignKey("users.id"),nullable=True)
    customer_id = Column(Integer,ForeignKey("customers.id"),nullable=True)
    created_at = Column(DateTime(timezone=True),server_default=func.now())
    updated_at = Column(DateTime(timezone=True),onupdate=func.now())
    deletion_reason = Column(String(500), nullable=True)
    hubspot_ticket_id = Column(String(50), nullable=True)
