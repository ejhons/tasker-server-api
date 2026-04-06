from sqlalchemy import create_engine, Column, String, Integer, Boolean, Float, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy_utils.types import ChoiceType
from core.database import Base

# Subclasse que herda Base. Por padrão, o nome da tabela será o nome da classe com 's' no final com todas as letras minúsculas.
class Usuario(Base):
    # Mas o nome da tabela pode ser definido por:
    __tablename__ = 'usuarios'
    # Cada campo será uma coluna do banco de dados
    id = Column('id', Integer, primary_key=True,
                autoincrement=True)  # Chave primária
    nome = Column('usuario', String)
    email = Column('email', String, nullable=False)  # Campo não pode ser vazio
    senha = Column('senha', String)
    ativo = Column('ativo', Boolean)
    # Campo que será definido como padrão fornecido.
    admin = Column('admin', Boolean, default=False)

    # Quando o usuário for criado por código python, a função __init será chamada.
    def __init__(self, nome, email, senha, ativo=True, admin=False):
        self.nome = nome
        self.email = email
        self.senha = senha
        self.ativo = ativo
        self.admin = admin

# Executa a criação dos metados do seu banco (cria efetivamente o banco de dados)

# migrar banco de dados
# criar migração: alembic revision --autogenerate -m 'Adicionando campo de itens a Pedido'
# Executa a migração: alembic upgrade head

# Item da Tarefa
class Tarefa(Base):
    __tablename__ = 'tarefas'
    STATUS_PEDIDOS = (
        # (Chave, valor) chave não pode ter caracteres especiais, enquanto valor sim.
        ('PENDENTE', 'PENDENTE'),
        ('CONCLUIDO', 'CONCLUIDO'),
        ('ARQUIVADO', 'ARQUIVADO'),
    )

    id = Column('id', Integer, primary_key=True, autoincrement=True)
    # pendente, cancelado, finalizado. O choiceType permite manter a integridade do banco
    descricao = Column('descricao', String, default='Nova Tarefa')
    status = Column('status', String, default='PENDENTE')
    # Chave estrangeira para se comunicar com a tabela de usuários. Deve ser fornecido o campo da tabela que deseja se conectar da forma tabela.campo
    criador = Column('criador', ForeignKey('usuarios.id'))
    # responsavel = Column('reponsavel', ForeignKey('usuarios.id'))
    # Sempre que eu tiver tabelas relacionadas por um campo e eu preciso acessar todos
    # os dados que estão realcionados a um objeto na tabela original, é conveniente usar uma Relationship.
    # cascade='all, delete' -> caso delete um itemPedido a ação é cascateada para Pedido, apagando-os.
    itens = relationship('ItemTarefa', cascade='all, delete')

    def __init__(self, usuario, descricao, status='PENDENTE'):#, responsavel=None):
        self.criador = usuario
        self.descricao = descricao
        self.status = status
        # self.responsavel = responsavel

    def atualiza_status(self):
        if self.status == 'ARQUIVADO':
            return
        if all([item.status for item in self.itens]):
            self.status = 'CONCLUÍDO'
        else:
            self.status = 'PENDENTE'


# Itens dos Pedidos
class ItemTarefa(Base):
    __tablename__ = 'itens_tarefa'

    id = Column('id', Integer, primary_key=True, autoincrement=True)
    descricao = Column('descricao', String)
    status = Column('concluido', Boolean, default=False)
    tarefa = Column('tarefa', ForeignKey('tarefas.id'))

    def __init__(self, tarefa, descricao='', status=False, ):
        self.descricao = descricao
        self.status = status
        self.tarefa = tarefa

    def toogle(self):
        self.status = not self.status
