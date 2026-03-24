
from fastapi import APIRouter, Depends, HTTPException
from dependencies import get_sessao, verificar_token
from sqlalchemy.orm import Session
from schemas import PedidoSchema,ItemPedidoSchema, ResponsePedidoSchema
from models import Pedido, Usuario, ItemPedido
from typing import List

#argumentos: prefixo padrão e tags
#Define uma lista de dependências. Quando passada no router, todas as rotas em nível abaixo precisarão essa dependência
# A dependência gerada nesse caso não pode ser usado como parâmetro dentro do endpoint
order_router = APIRouter(prefix='/pedidos', tags=['pedidos'], dependencies=[Depends(verificar_token)])

#endpoint:dominio/pedidos/lista
#decorator: linha de código antes da função que atribui uma funcionalidade à função designada
@order_router.get('/')#lista de pedidos retornados pela função
async def pedidos():#função assíncrona para poder ser usada no app
    '''
    Essa é a rota padrão de acesso aos pedidos. Todas as rotas precisam de autenticação.
    '''
    return {"mensagem":"Você acessou à rota de pedidos."}#Sempre retornará um json que estabelece a comunicação (envio ou recebimento)

@order_router.post('/pedido')
async def criar_pedido(pedido_schema:PedidoSchema, session:Session = Depends(get_sessao)):
    novo_pedido = Pedido(usuario=pedido_schema.id_usuario)
    session.add(novo_pedido)
    session.commit()
    return {'mensagem':f'Pedido criado com sucesso. ID do pedido: {novo_pedido.id}'}

@order_router.post('/pedido/cancelar/{id_pedido}')
# Use colchetes para passar algo dentro da rota.
# Nesse caso, o parâmetro deve ser passado como argumento da função.
async def cancelar_pedido(id_pedido:int, session:Session = Depends(get_sessao), usuario:Usuario = Depends(verificar_token)):
    pedido = session.query(Pedido).filter(Pedido.id==id_pedido).first()
    #Verifica se o pedido existe
    if not pedido:
        raise HTTPException(status_code=400, detail='Pedido não encontrado!')
    #Somente usuários admin ou o usuário que fez o pedido podem cancelar o pedido
    if not usuario.admin and usuario.id != pedido.usuario:
        raise HTTPException(status_code=401, detail='Você não tem permissão para fazer essa operação.')
    # Faz o cancelamento alterando o status do pedido
    pedido.status = 'CANCELADO'
    session.commit()# Não precisa ser adicionada a sessão, pois ela já está presente. Apaga o conteúdo da variável pedido
    return {
        'messagem':f'Pedido nº {pedido.id} cancelado com sucesso',#Obriga o sistema a carregar as informações do pedido após o comit
        'pedido': pedido #Exibe campos como atributos do objeto;
    }


@order_router.get('/listar')
async def listar_pedidos(session:Session = Depends(get_sessao), usuario:Usuario = Depends(verificar_token)):
    '''
    Lista todos os pedidos presentes no banco de dados
    '''
    if not usuario.admin:
        raise HTTPException(status_code=400, detail='Você não tem permissão para fazer essa operação.')
    else:
        pedidos = session.query(Pedido).all()#Usar paginação para evitar carregamento lento em sistemas maiores
        return {
            'pedidos':pedidos
        }

@order_router.post('/pedido/adicionar-item/{id_pedido}')
async def adicionar_item_pedido(id_pedido:int, item_pedido_schema:ItemPedidoSchema, session:Session = Depends(get_sessao), usuario:Usuario = Depends(verificar_token)):
    # Garantir que o usuário tem permissão
    pedido = session.query(Pedido).filter(Pedido.id==id_pedido).first()    
    # Verifica se o pedido existe
    if not pedido:
        raise HTTPException(status_code=400, detail='Pedido não encontrado!')
    #Somente usuários admin ou o usuário que fez o pedido podem adicionar item ao pedido
    if not usuario.admin and usuario.id != pedido.usuario:
        raise HTTPException(status_code=401, detail='Você não tem permissão para fazer essa operação.')
    item_pedido = ItemPedido(item_pedido_schema.quantidade, item_pedido_schema.sabor, item_pedido_schema.tamanho, 
                             item_pedido_schema.borda, item_pedido_schema.preco_unitario, id_pedido)
    # Adiciona item ao pedido
    session.add(item_pedido)
    # Recalcula o preço do pedido
    pedido.calcular_preco()
    session.commit()
    return {
        'mensagem': 'Item criado com sucesso',
        'item_id': item_pedido.id,
        'preco_pedido': pedido.preco
    }


@order_router.post('/pedido/remover-item/{id_item_pedido}')
async def remover_item_pedido(id_item_pedido:int, session:Session = Depends(get_sessao), usuario:Usuario = Depends(verificar_token)):
    # Garantir que o usuário tem permissão
    item_pedido = session.query(ItemPedido).filter(ItemPedido.id==id_item_pedido).first()
    # Verifica se o pedido existe
    if not item_pedido:
        raise HTTPException(status_code=400, detail='Item no pedido não encontrado!')
    #Somente usuários admin ou o usuário que fez o pedido podem adicionar item ao pedido
    if not usuario.admin and usuario.id != pedido.usuario:
        raise HTTPException(status_code=401, detail='Você não tem permissão para fazer essa operação.')
    
    pedido = session.query(Pedido).filter(Pedido.id==item_pedido.pedido).first()
    # Remove item ao pedido
    session.delete(item_pedido)
    # Recalcula o preço do pedido
    pedido.calcular_preco()
    session.commit()
    # Lembre do lazy loading
    return {
        'mensagem': 'Item removido com sucesso',
        'quantidade_itens_pedido': len(pedido.itens),
        'pedido': pedido
    }

# Finalizar um pedido
@order_router.post('/pedido/finalizar/{id_pedido}')
async def finalizar_pedido(id_pedido:int, session:Session = Depends(get_sessao), usuario:Usuario = Depends(verificar_token)):
    pedido = session.query(Pedido).filter(Pedido.id==id_pedido).first()
    #Verifica se o pedido existe
    if not pedido:
        raise HTTPException(status_code=400, detail='Pedido não encontrado!')
    #Somente usuários admin ou o usuário que fez o pedido podem cancelar o pedido
    if not usuario.admin and usuario.id != pedido.usuario:
        raise HTTPException(status_code=401, detail='Você não tem permissão para fazer essa operação.')
    # Faz o cancelamento alterando o status do pedido
    pedido.status = 'FINALIZADO'
    session.commit()# Não precisa ser adicionada a sessão, pois ela já está presente. Apaga o conteúdo da variável pedido
    return {
        'messagem':f'Pedido nº {pedido.id} finalizado com sucesso',#Obriga o sistema a carregar as informações do pedido após o comit
        'pedido': pedido #Exibe campos como atributos do objeto;
    }

# Visualizar um pedido
@order_router.post('/pedido/{id_pedido}', response_model=ResponsePedidoSchema)
async def visualizar_pedido(id_pedido:int, session:Session = Depends(get_sessao), usuario:Usuario = Depends(verificar_token)):
    # Garantir que o usuário tem permissão
    pedido = session.query(Pedido).filter(Pedido.id==id_pedido).first()
    # Verifica se o pedido existe
    if not pedido:
        raise HTTPException(status_code=400, detail='Item no pedido não encontrado!')
    #Somente usuários admin ou o usuário que fez o pedido podem adicionar item ao pedido
    if not usuario.admin and usuario.id != pedido.usuario:
        raise HTTPException(status_code=401, detail='Você não tem permissão para fazer essa operação.')
    
    session.commit()
    # Lembre do lazy loading
    # return {
    #     'quantidade_itens_pedido': len(pedido.itens),
    #     'pedido': pedido
    # }
    return pedido


# Todos os pedidos de um usuário
# Dessa forma, admins não podem ver os pedidos de outros usuários
# Graças ao typing, podemos retornar uma lista de pedidos no formato de ResponsePedidoSchema
@order_router.post('/listar/pedidos-usuario', response_model=List[ResponsePedidoSchema])#/{id_usuario}')
async def listar_pedidos(session:Session = Depends(get_sessao), usuario:Usuario = Depends(verificar_token)):
    '''
    Lista todos os pedidos presentes no banco de dados
    '''
    pedidos = session.query(Pedido).filter(Pedido.usuario==usuario.id).all()
    return pedidos #usa o Schema de resposta para retornar as informações


'''
@order_router.post()
@order_router.patch()
@order_router.delete()
'''