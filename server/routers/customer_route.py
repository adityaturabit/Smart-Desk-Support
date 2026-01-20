from fastapi import APIRouter, Depends,HTTPException, Header, status
from sqlalchemy.orm import Session
from server.db_connect.db_config import engine,Base
from server.dependencies import get_db, get_current_user
from server.models.db_model import Customer, User
from server.schemas.customer_schema import CustomerCreate, CustomerResponse
from typing import List

router = APIRouter(prefix="/customers", tags=["Customers"])

@router.post("/",response_model=CustomerResponse)
def create_customer(customer: CustomerCreate,
                     db:Session = Depends(get_db),
                     current_user: User = Depends(get_current_user)):
    
    # user =  db.query(User).filter(User.emp_id == x_emp_id).first()
    try:
        if not current_user:
            print("User not Found")
            raise HTTPException(status_code=404, detail="User not Found")
        
        if current_user.role != "support":
            raise HTTPException(status_code=403, detail="Only For Support Agents")

        new_customer = Customer(
            name = customer.name,
            email = customer.email,
            company = customer.company,
            created_by_agent_id = current_user.id,
            created_by_agent_name = current_user.name
        )

        db.add(new_customer)
        db.commit()
        # db.flush()
        return new_customer
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.get("/",response_model=list[CustomerResponse])
def get_customers(db:Session=Depends(get_db),current_user : User = Depends(get_current_user)):
    try:
        if current_user.role == "employee":
            raise HTTPException(status_code=403,detail="Only for the Authorized members")

        if current_user.role == "support":
            return db.query(Customer).filter(
                Customer.created_by_agent_id == current_user.id
            ).all()

        if current_user.role == "team_lead":
            return db.query(Customer).all()

        raise HTTPException(status_code=403, detail="Unauthorized")
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


#customer can be updated by thos agent only who created them in the first place
@router.put("/{customer_id}",response_model=CustomerResponse)
def update_customer(customer_id: int, customer : CustomerCreate, db:Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    try:
        if current_user.role != "support":
            raise HTTPException(status_code=404,detail=["Only support agent can"])
        
        existing = db.query(Customer).filter(Customer.id == customer_id).first()

        if not existing:
            raise HTTPException(status_code=404,detail=["Customer not found"])
        
        if existing.created_by_agent_id != current_user.id:
            raise HTTPException(status_code=403,detail=["Not your Customer"])
        
        existing.name = customer.name
        existing.email = customer.email
        existing.company = customer.company

        db.commit()
        db.flush()

        return existing
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )



#customer can be deleted by those agent who created in the first place
@router.delete("/{customer_id}")
def delete_customer( customer_id : int, db:Session = Depends(get_db), current_user : User = Depends(get_current_user)):
    try:
        if current_user.role != "support":
            raise HTTPException(status_code=403,detail=["Only support agents are allowed"])
        
        customer = db.query(Customer).filter(Customer.id == customer_id).first()

        if not customer:
            raise HTTPException(status_code=404,detail=["Customer not found"])
        
        if customer.created_by_agent_id != current_user.id:
            raise HTTPException(status_code=404,detail=["Not you customer to deal with"])
        
        db.delete(customer)
        db.commit()
        db.flush()

        return {"message": f"Customer {customer.name} is deleted successfully by agent {current_user.name}"}
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )