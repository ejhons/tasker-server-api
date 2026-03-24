#Pydantic: força o tipo dos dados garantindo velocidade e integridade.
from pydantic import BaseModel
from typing import Optional, List

# Padrões de envio de informação
class UsuarioSchema(BaseModel):
    nome:str
    email:str
    senha:str
    ativo:Optional[bool]
    admin:Optional[bool]

    class Config:
        from_attributes = True #Faz com o objeto seja interpretado como uma classe graças ao sqlalchemy

class PedidoSchema(BaseModel):
    id_usuario:int
    
    class Config:
        from_attributes = True #Faz com o objeto seja interpretado como uma classe graças ao sqlalchemy

class LoginSchema(BaseModel):
    email:str
    senha:str
    class Config:
        from_attributes = True

class ItemPedidoSchema(BaseModel):    
    quantidade:int
    sabor:str
    tamanho:str
    borda:bool
    preco_unitario:float
    class Config:
        from_attributes = True

# Padrão de resposta do servidor
class ResponsePedidoSchema(BaseModel):
    id: int
    status: str
    preco: float
    itens: List[ItemPedidoSchema]
    class Config:
        from_attributes = True

