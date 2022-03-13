from passlib.context import CryptContext

# Telling passlib the default hashing algorithm -> bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash(password: str):
    return pwd_context.hash(password)