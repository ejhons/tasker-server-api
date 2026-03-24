
from fastapi import APIRouter

#argumentos: prefixo padrão e tags
tasks_router = APIRouter(prefix='/tasks', tags=['tasks'])