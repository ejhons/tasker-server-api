from sqlalchemy import create_engine, Column, String, Integer, Boolean, Float, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy_utils.types import ChoiceType


# Cria a conexão do banco de dados no local informado. Após o deploy da aplicação, o endereço fornecido deve corresponder àquele disponibilizador pelo provedor.
db = create_engine('sqlite:///banco.db')
#db = create_engine('sqlite:///database/banco.db')
# Cria a base do banco de dados
Base = declarative_base()


# Cria as classes que serão as tabelas do banco de dados
# Usuário: administradores e clientes


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


# Pedido
class Pedido(Base):
    __tablename__ = 'pedidos'
    STATUS_PEDIDOS = (
        # (Chave, valor) chave não pode ter caracteres especiais, enquanto valor sim.
        ('PENDENTE', 'PENDENTE'),
        ('CANCELADO', 'CANCELADO'),
        ('FINALIZADO', 'FINALIZADO'),
    )

    id = Column('id', Integer, primary_key=True, autoincrement=True)
    # pendente, cancelado, finalizado. O choiceType permite manter a integridade do banco
    status = Column('status', String, default='PENDENTE')
    # status = Column('status', ChoiceType(STATUS_PEDIDOS), default='PENDENTE')
    # Chave estrangeira para se comunicar com a tabela de usuários. Deve ser fornecido o campo da tabela que deseja se conectar da forma tabela.campo
    usuario = Column('usuario', ForeignKey('usuarios.id'))
    preco = Column('preco', Float)
    # Sempre que eu tiver tabelas relacionadas por um campo e eu preciso acessar todos os dados que estão realcionados a um objeto na tabela original, é conveniente usar uma Relationship.
    # cascade='all, delete' -> caso delete um itemPedido a ação é cascateada para Pedido, apagando-os.
    itens = relationship('ItemPedido', cascade='all, delete')

    def __init__(self, usuario, status='PENDENTE', preco=0.0):
        self.usuario = usuario
        self.preco = preco
        self.status = status
    
    def calcular_preco(self):
        # Calcula e atualiza o preço do pedido
        self.preco = sum([item.preco_unitario * item.quantidade for item in self.itens])

# Itens dos Pedidos
class ItemPedido(Base):
    __tablename__ = 'itens_pedido'
    TAMANHOS = (
        ('P', 'PEQUENA'),
        ('M', 'MÉDIA'),
        ('G', 'GRANDE')
    )

    id = Column('id', Integer, primary_key=True, autoincrement=True)
    quantidade = Column('quantidade', Integer)
    sabor = Column('sabor', String)
    tamanho = Column('tamanho', String)#ChoiceType(TAMANHOS))
    borda = Column('borda', Boolean)
    preco_unitario = Column('preco_unitario', Float)
    pedido = Column('pedido', ForeignKey('pedidos.id'))

    def __init__(self, quantidade, sabor, tamanho, borda, preco_unitario, pedido):
        self.quantidade = quantidade
        self.sabor = sabor
        self.tamanho = tamanho
        self.borda = borda
        self.preco_unitario = preco_unitario
        self.pedido = pedido

# Executa a criação dos metados do seu banco (cria efetivamente o banco de dados)

# migrar banco de dados
# criar migração: alembic revision --autogenerate -m 'Adicionando campo de itens a Pedido'
# Executa a migração: alembic upgrade head
