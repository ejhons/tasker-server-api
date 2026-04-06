
from fastapi import Depends, HTTPException
from core.database import db
from app.models import Usuario
from sqlalchemy.orm import sessionmaker, Session
from jose import jwt, JWTError
from main import SECRET_KEY, ALGORITHM
from core.security import oauth2_schema
# from main import oauth2_schema, SECRET_KEY, ALGORITHM

def get_sessao():
    '''
    Cria a sessão no banco de dados e garante que ela seja fechada após o uso.
    '''
    try:# garante que a sessão seja fechada
        Session = sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=db)
        session = Session()#A classe sessão é um generator. Sempre que quiser pegar, é realizado um processo de yield.
        yield session#Retorna um valor mas neão encerra a execução da função
    finally:
        session.close()#Fecha após a conclusão do yeld


def verificar_token (token: str = Depends(oauth2_schema), session:Session = Depends(get_sessao)) -> Usuario:
    # Decodifica e retorna um dicionário com as informações do usuário. Caso não consiga verificar, lança um erro.
    try:
        #verifica se o token é válido
        dict_info = jwt.decode(token, SECRET_KEY, ALGORITHM)# Decodifica se o token ainda estiver válido
        id_usuario = int(dict_info.get('sub')) #Não retorna erro se não encontrar parêmtro
    except JWTError as error:
        print(error)
        raise HTTPException(status_code=401, detail='Acesso negado.')

    #Extrai o id do usuário
    usuario = session.query(Usuario).filter(Usuario.id==id_usuario).first()
    #Lança exceção caso o usuário não seja encontrado
    if not usuario:
        raise HTTPException(status_code=401, detail='Acesso Inválido.')
    # Retorna o usuário encontrado
    return usuario

