from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
# from passlib.context import CryptContext
# from main import bcryp_context


#Critografa. Pode ser passado mais de um. Caso algum fique obsoleto, 
#é removido quando deprecated='auto'
bcryp_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
oauth2_schema = OAuth2PasswordBearer(tokenUrl='auth/login-form')

def get_password_hash(password: str) -> str:
    return bcryp_context.hash(password)

def verify_password(plain_password:str, hashed_password:str) -> bool:
    return bcryp_context.verify(plain_password, hashed_password)