from pydantic import BaseModel,EmailStr


class CustomerBase(BaseModel):
    name : str
    email : EmailStr | None = None
    company : str | None=None

class CustomerCreate(CustomerBase):
    pass 

class CustomerResponse(CustomerBase):
    id : int
    created_by_agent_id : int

    class Config:
        from_attributes = True