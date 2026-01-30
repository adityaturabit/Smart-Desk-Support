from passlib.context import CryptContext
import hashlib

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)
def _prehash_password(password: str) -> str:
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def hash_password(plain_password:str)-> str:
    return pwd_context.hash(_prehash_password(plain_password))

def verify_password(plain_password:str,hash_password:str)-> bool:
    return pwd_context.verify(_prehash_password(plain_password),hash_password)