import os
import sys
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
#from main import DATABASE_URI

# Cria a conexão do banco de dados no local informado. Após o deploy da aplicação, o endereço fornecido deve corresponder àquele disponibilizador pelo provedor.
db = create_engine(url='sqlite:///./data/banco.db')#DATABASE_URI)

# Cria a base do banco de dados
Base = declarative_base()

async def create_db_and_tables():
	'''
	Cria tabelas do banco de dados
	'''
	Base.metadata.create_all(bind=db)
