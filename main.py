from fastapi import FastAPI
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from dotenv import load_dotenv
import os

# Carrega as variáveis de ambiente presentes no .env
load_dotenv()
#Busca a chave no arquivo .env
SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM = os.getenv('ALGORITHM')
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES'))

# Cria o 
app = FastAPI()

#Critografa. Pode ser passado mais de um. Caso algum fique obsoleto, 
#é removido quando deprecated='auto'
bcryp_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
oauth2_schema = OAuth2PasswordBearer(tokenUrl='auth/login-form')

# rodar através do comando no CMD: uvicorn main::app --reload
#endpoints
from auth_routes import auth_router
from order_routes import order_router


app.include_router(auth_router)
app.include_router(order_router)