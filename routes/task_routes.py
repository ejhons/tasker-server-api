from fastapi import APIRouter, Depends, HTTPException
from core.dependencies import get_sessao, verificar_token
from sqlalchemy.orm import Session
from app.schemas import TarefaSchema, ItemTarefaSchema, ResponseTarefaSchema
from app.models import Tarefa, Usuario, ItemTarefa
from typing import List

# argumentos: prefixo padrão e tags
# Define uma lista de dependências. Quando passada no router, todas as rotas em nível abaixo precisarão dessa dependência
# A dependência gerada nesse caso, entretanto, não pode ser usado como parâmetro dentro do endpoint
task_router = APIRouter(
    prefix='/tarefas', tags=['tarefas'], dependencies=[Depends(verificar_token)])

# endpoint:dominio/tarefas/lista
# decorator: linha de código antes da função que atribui uma funcionalidade à função designada
@task_router.get('/lista')  # lista de pedidos retornados pela função
async def listar_tarefas(session: Session = Depends(get_sessao), usuario: Usuario = Depends(verificar_token)):  # função assíncrona para poder ser usada no app
    '''
    Essa é a rota padrão de acesso aos pedidos. Todas as rotas precisam de autenticação.
    '''
    resultado = session.query(Tarefa).filter((Tarefa.criador==usuario.id)).all()
    if resultado is None:
        resultado = [] 

    return {
        "mensagem": "Você acessou à rota de Tarefas.",
        'tarefas':resultado
            }  # Sempre retornará um json que estabelece a comunicação (envio ou recebimento)

# Visualizar um pedido
@task_router.get('/tarefa/{id_tarefa}', response_model=ResponseTarefaSchema)
async def visualizar_tarefa(
    id_tarefa: int,
    session: Session = Depends(get_sessao),
    usuario: Usuario = Depends(verificar_token)):
    # Garantir que o usuário tem permissão
    tarefa = session.query(Tarefa).filter(Tarefa.id == id_tarefa).first()
    # Verifica se o pedido existe
    if not tarefa:
        raise HTTPException(
            status_code=400, detail='Tarefa não encontrada!')
    # Somente usuários admin ou o usuário que fez o pedido podem adicionar item ao pedido
    if (not usuario.admin) and (usuario.id != tarefa.criador):
        raise HTTPException(
            status_code=401, detail='Você não tem permissão para fazer essa operação.')

    return tarefa


@task_router.post('/tarefa')
async def criar_tarefa(
    tarefa_schema: TarefaSchema, 
    session: Session = Depends(get_sessao), 
    usuario: Usuario = Depends(verificar_token)):
    try:
        nova_tarefa = Tarefa(
            usuario=usuario.id, 
            descricao=tarefa_schema.descricao)#, 
            #responsavel=tarefa_schema.id_responsavel)
        session.add(nova_tarefa)
        session.commit()
        return {
            'mensagem': f'Tarefa criada com sucesso. ID da tarefa: {nova_tarefa.id}',
            'tarefa':nova_tarefa
            }
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=f'Operação não realizada: {str(e)}')



# Finalizar um pedido
@task_router.post('/tarefa/mudar_estado/{id_tarefa}')
async def mudar_estado(
    id_tarefa: int, 
    session: Session = Depends(get_sessao), 
    usuario: Usuario = Depends(verificar_token)):
    tarefa = session.query(Tarefa).filter(Tarefa.id == id_tarefa).first()
    # Verifica se o pedido existe
    if not tarefa:
        raise HTTPException(status_code=400, detail='Tarefa não encontrado!')
    # Somente usuários admin ou o usuário que fez o pedido podem mudar o estado
    if (not usuario.admin) and (usuario.id != tarefa.criador):
        raise HTTPException(
            status_code=401, detail='Você não tem permissão para fazer essa operação.')
    # Faz o cancelamento alterando o status do pedido
    tarefa.status = 'CONCLUÍDO' if tarefa.status == 'PENDENTE' else 'PENDENTE'
    session.commit()  # Não precisa ser adicionada a sessão, pois ela já está presente. Apaga o conteúdo da variável pedido
    return {
        # Obriga o sistema a carregar as informações do pedido após o comit
        'messagem': f'Tarefa {tarefa.id} com estado alterado para {tarefa.status}',
        'pedido': tarefa  # Exibe campos como atributos do objeto;
    }

@task_router.post('/tarefa/arquivar/{id_tarefa}')
# Use colchetes para passar algo dentro da rota.
# Nesse caso, o parâmetro deve ser passado como argumento da função.
async def arquivar_pedido(
    id_tarefa: int, 
    session: Session = Depends(get_sessao), 
    usuario: Usuario = Depends(verificar_token)):
    tarefa = session.query(Tarefa).filter(Tarefa.id == id_tarefa).first()
    # Verifica se o pedido existe
    if not tarefa:
        raise HTTPException(status_code=400, detail='Tarefa não encontrada!')
    # Somente usuários admin ou o usuário que fez o pedido podem cancelar o pedido
    if (not usuario.admin) and (usuario.id != tarefa.criador):
        raise HTTPException(
            status_code=401, detail='Você não tem permissão para fazer essa operação.')
    # Faz o cancelamento alterando o status do pedido
    tarefa.status = 'ARQUIVADO' if tarefa.status != 'ARQUIVADO' else 'PENDENTE'
    session.commit()  # Não precisa ser adicionada a sessão, pois ela já está presente. Apaga o conteúdo da variável pedido
    return {
        # Obriga o sistema a carregar as informações do pedido após o comit
        'messagem': f'Tarefa {tarefa.id} arquivada com sucesso',
        'tarefa': tarefa  # Exibe campos como atributos do objeto;
    }


@task_router.get('/admin/todas_tarefas')
async def admin_listar_tarefas(session: Session = Depends(get_sessao), usuario: Usuario = Depends(verificar_token)):
    '''
    Lista todos os pedidos presentes no banco de dados
    '''
    if not usuario.admin:
        raise HTTPException(
            status_code=400, detail='Você não tem permissão para fazer essa operação.')
    # Usar paginação para evitar carregamento lento em sistemas maiores
    tarefas = session.query(Tarefa).all()
    return {
        'tarefas': tarefas
    }


@task_router.post('/tarefa/{id_tarefa}/adicionar-item')
async def adicionar_item_tarefa(
    id_tarefa: int, 
    item_tarefa_schema: ItemTarefaSchema,
    session: Session = Depends(get_sessao),
    usuario: Usuario = Depends(verificar_token)):
    # Garantir que o usuário tem permissão
    tarefa = session.query(Tarefa).filter(Tarefa.id == id_tarefa).first()
    # Verifica se o pedido existe
    if not tarefa:
        raise HTTPException(status_code=400, detail='Tarefa não encontrada!')
    # Somente usuários admin ou o usuário que fez o pedido podem adicionar item ao pedido
    if (not usuario.admin) and (usuario.id != tarefa.criador):# or usuario.id != tarefa.responsavel):
        raise HTTPException(
            status_code=401, detail='Você não tem permissão para fazer essa operação.')
    item_tarefa = ItemTarefa(
        id_tarefa,
        item_tarefa_schema.descricao,
        item_tarefa_schema.status
    )
    # Adiciona item ao pedido
    session.add(item_tarefa)
    # Recalcula o preço do pedido
    tarefa.atualiza_status()
    session.commit()
    return {
        'mensagem': 'Item criado com sucesso',
        'item_id': item_tarefa.id,
        'status_tarefa': tarefa.status
    }

@task_router.post('/tarefa/toogle/{id_item_tarefa}')
async def toogle_item_tarefa(
    id_item_tarefa: int, 
    session: Session = Depends(get_sessao), 
    usuario: Usuario = Depends(verificar_token)):
    # Garantir que o usuário tem permissão
    item_tarefa = session.query(ItemTarefa).filter(
        ItemTarefa.id == id_item_tarefa).first()
    # Verifica se o pedido existe
    if not item_tarefa:
        raise HTTPException(
            status_code=400, detail='Item não encontrado!')
    # Localiza a tarefa principal
    tarefa = session.query(Tarefa).filter(
        Tarefa.id == item_tarefa.tarefa).first()
    # Somente usuários admin ou o usuário que fez o pedido podem adicionar item ao pedido
    if (not usuario.admin) and (usuario.id != tarefa.criador):
        raise HTTPException(
            status_code=401, detail='Você não tem permissão para fazer essa operação.')
    # Marca/Desmarca item
    item_tarefa.toogle()
    # Atualiza o status da Tarefa com base em seus itens
    tarefa.atualiza_status()
    session.commit()
    # Lembre do lazy loading
    return {
        'mensagem': f'Item atualizado com sucesso para {item_tarefa.status}',
        'quantidade_itens_tarefa': len(tarefa.itens),
        'tarefa': tarefa
    }

@task_router.post('/tarefa/remover-item/{id_item_tarefa}')
async def remover_item_pedido(
    id_item_tarefa: int, 
    session: Session = Depends(get_sessao), 
    usuario: Usuario = Depends(verificar_token)):
    # Garantir que o usuário tem permissão
    item_tarefa = session.query(ItemTarefa).filter(
        ItemTarefa.id == id_item_tarefa).first()
    # Verifica se o pedido existe
    if not item_tarefa:
        raise HTTPException(
            status_code=400, detail='Item não encontrado!')
    # Localiza a tarefa principal
    tarefa = session.query(Tarefa).filter(
        Tarefa.id == item_tarefa.tarefa).first()
    # Somente usuários admin ou o usuário que fez o pedido podem adicionar item ao pedido
    if (not usuario.admin) and (usuario.id != tarefa.usuario):
        raise HTTPException(
            status_code=401, detail='Você não tem permissão para fazer essa operação.')

    # Remove item ao pedido
    session.delete(item_tarefa)
    # Recalcula o preço do pedido
    tarefa.atualiza_status()
    session.commit()
    # Lembre do lazy loading
    return {
        'mensagem': 'Item removido com sucesso',
        'quantidade_itens_tarefa': len(tarefa.itens),
        'tarefa': tarefa
    }


# Todos os pedidos de um usuário
# Dessa forma, admins não podem ver os pedidos de outros usuários
# Graças ao typing, podemos retornar uma lista de pedidos no formato de ResponseTarefaSchema
# /{id_usuario}')
@task_router.post('/listar/tarefas-usuario', response_model=List[ResponseTarefaSchema])
async def listar_tarefas_usuario(
    session: Session = Depends(get_sessao), 
    usuario: Usuario = Depends(verificar_token)):
    '''
    Lista todos os pedidos presentes no banco de dados
    '''
    tarefas = session.query(Tarefa).filter(Tarefa.criador == usuario.id).all()
    return tarefas  # usa o Schema de resposta para retornar as informações


'''
@task_router.post()
@task_router.patch()
@task_router.delete()
'''
