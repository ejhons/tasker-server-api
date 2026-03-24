'''
Docstring for auth_routes
Rotas referentes às rotas relacionadas à autenticação.
'''
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from models import Usuario
from dependencies import get_sessao, verificar_token
from main import bcryp_context
from schemas import UsuarioSchema, LoginSchema
from sqlalchemy.orm import Session
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone
from main import SECRET_KEY, ACCESS_TOKEN_EXPIRE_MINUTES, ALGORITHM

#argumentos: prefixo padrão e tags
auth_router = APIRouter(prefix='/auth', tags=['auth'])

# Gera token de acesso (curta duração)
def criar_token(id_usuario, duracao_token=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)):
    #Define data de expiração do token
    data_expiracao = datetime.now(timezone.utc) + duracao_token
    dict_info = {
        'sub':str(id_usuario), #parâmetro do proprietário do token que precisa necessariamente ser uma string
        'exp':data_expiracao,
        }
    #gera o token jwt codificado
    encoded_jwt = jwt.encode(dict_info, SECRET_KEY, ALGORITHM)
    return encoded_jwt

#Verifica se as informações de usuário e senha correspondem ao cadastrado no banco de dados. Em caso afirmativo, retorna o usuário.
def autenticar_usuario(email, senha, session):
    usuario = session.query(Usuario).filter(Usuario.email==email).first()
    if not usuario:
        return False
    elif not bcryp_context.verify(senha, usuario.senha):
        return False
    
    return usuario


@auth_router.get('/')
async def home():
    '''
    Essa é a rota principal de autenticação.
    '''
    return {'mensagem':'Você acessou à rota de autenticação',
            'autenticado':False}

@auth_router.post('/criar_conta')
async def criar_conta(usuario_schema:UsuarioSchema, session : Session = Depends(get_sessao)):#usuario:Usuario):   
    #verifica se já existe um usuário
    usuario = session.query(Usuario).filter(Usuario.email==usuario_schema.email).first()
    if usuario:
        #Já existe usuário com esse email
        raise HTTPException(status_code=400, detail="Já existe um usuário cadastrado com esse e-mail!")
    else:
        senha_criptografada = bcryp_context.hash(usuario_schema.senha)
        novo_usuario = Usuario(
            nome=usuario_schema.nome,
            email=usuario_schema.email,
            senha=senha_criptografada,
            ativo=usuario_schema.ativo,
            admin=usuario_schema.admin)
        session.add(novo_usuario)
        session.commit()
        return {"mensagem":f"Usuário cadastrado com sucesso: {usuario_schema.email}"}

# Uso de tokens para acesso ao endpoint
#login -> email e senha -> token JWT (Json Web token) dasdi98420dsioew0923dada
# Cada rota recebe o token para validar autenticação
@auth_router.post('/login')
async def login(login_schema:LoginSchema, session:Session = Depends(get_sessao)):
    #Verifica se existe usuário
    usuario = autenticar_usuario(login_schema.email, login_schema.senha, session)#session.query(Usuario).filter(Usuario.email==login_schema.email).first()
    #Caso o usuário não seja encontrado, lança um erro.
    if not usuario:
        raise HTTPException(status_code=400, detail='Usuário não encontrado ou credenciais erradas.')
    else:
        access_token = criar_token(usuario.id)
        refresh_token = criar_token(usuario.id, timedelta(days=7)) #token para permitir atualização do token de autenticação
        #JWT Bearer. Dentro do headers, é ncessário mandar 
        #header = {'Access-Token':'Bearer Token'}
        return {
            'access_token':access_token,
            'refresh-token':refresh_token,
            'token-type':'Bearer'
            }
# Para poder utilizar o botão de authorize dentro da documentação do FastAPI
@auth_router.post('/login-form')
async def login_form(dados_formulario: OAuth2PasswordRequestForm = Depends(), session:Session = Depends(get_sessao)):
    #Verifica se existe usuário
    usuario = autenticar_usuario(dados_formulario.username, dados_formulario.password, session)#session.query(Usuario).filter(Usuario.email==login_schema.email).first()
    #Caso o usuário não seja encontrado, lança um erro.
    if not usuario:
        raise HTTPException(status_code=400, detail='Usuário não encontrado ou credenciais erradas.')
    else:
        access_token = criar_token(usuario.id)
        return {
            'access_token':access_token,
            'token-type':'Bearer'
            }


@auth_router.get('/refresh')
async def use_refresh_token(usuario: Usuario = Depends(verificar_token)):
    '''Verifica o token passado se ainda é válido. Em caso afirmativo, retorna um novo token de acesso'''
    #usuario = verificar_token(token, session)
    access_token = criar_token(usuario.id)
    return {
        'access_token':access_token,
        'token-type':'Bearer'
        }
