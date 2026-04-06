# Pydantic: força o tipo dos dados garantindo velocidade e integridade.
from pydantic import BaseModel
from typing import Optional, List

# Padrões de envio de informação


class UsuarioSchema(BaseModel):
    nome: str
    email: str
    senha: str
    ativo: Optional[bool]
    admin: Optional[bool]

    class Config:
        # Faz com o objeto seja interpretado como uma classe graças ao sqlalchemy
        from_attributes = True

class LoginSchema(BaseModel):
    email: str
    senha: str

    class Config:
        from_attributes = True

class TarefaSchema(BaseModel):
    # id_usuario: int
    descricao: str
    # id_responsavel: int = None

    class Config:
        # Faz com o objeto seja interpretado como uma classe graças ao sqlalchemy
        from_attributes = True


class ItemTarefaSchema(BaseModel):
    descricao: str
    status: bool = False

    class Config:
        from_attributes = True


class ResponseTarefaSchema(BaseModel):
    id: int
    status: str
    descricao: str
    itens: List[ItemTarefaSchema]

    class Config:
        from_attributes = True
