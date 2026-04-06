# TASKER - Simple Task Manager
## Description
Gerenciador simples de tarefas capaz de cadastrar usuários e oprações de
CRUD de geração de tarefas.

## 🚀 Funcionalidades
- CRUD de tarefas
- Cadastro de usuários (administradores e clientes)
- Operações de Finalização ou Arquivamento de tarefas

## Arquitetura
- Separação de Responsabilidades
- Service layer
- Autenticação em JWT Tokes

# Tecnologias
- Python
- FastAPI
- SQLAlchemy
- SQLite

## Como rodar
```bash
pip install -r requirements.txt
uvicorn main:app --reload
```

## Como rodar em porta específica
```bash
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port $PORT
```

## Domínio
- produtividade e gerenciamento



