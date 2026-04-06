import os
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from contextlib import asynccontextmanager
from core.database import create_db_and_tables, db
from app.init_admin import create_admin_if_not_exists
from sqlalchemy.orm import sessionmaker

# Carrega as variáveis de ambiente presentes no .env
load_dotenv()

#Busca a chave no arquivo .env
DATABASE_URI = os.getenv('DATABASE_URI')
SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM = os.getenv('ALGORITHM')
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES'))


@asynccontextmanager
async def lifespan(app: FastAPI):    
    await create_db_and_tables()
    try:# garante que a sessão seja fechada
        SessionLocal = sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=db)
        session = SessionLocal()#A classe sessão é um generator. Sempre que quiser pegar, é realizado um processo de yield.
        create_admin_if_not_exists(session)
    finally:
        session.close()#Fecha após a conclusão do yeld
    yield

# Cria o aplicativo
app = FastAPI(lifespan=lifespan)

@app.route('/')
def root():
    return {'message':'API em execução...'}


# @app.on_event('startup')

# #Critografa. Pode ser passado mais de um. Caso algum fique obsoleto, 
# #é removido quando deprecated='auto'
# bcryp_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
# oauth2_schema = OAuth2PasswordBearer(tokenUrl='auth/login-form')

#endpoints
from routes.auth_routes import auth_router
from routes.task_routes import task_router

app.include_router(auth_router)
app.include_router(task_router)

# rodar através do comando no CMD: uvicorn main:app --reload