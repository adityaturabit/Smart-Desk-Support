from pydantic import BaseModel

class LoginReq(BaseModel):
    emp_id : str
    email_id : str
    password : str