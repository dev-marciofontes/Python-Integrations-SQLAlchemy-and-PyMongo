from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    create_engine,
    inspect,
    select,
    Numeric
)
from sqlalchemy.orm import (
    declarative_base,
    relationship,
    Session
)

Base = declarative_base()


class Cliente(Base):
    """Classe que representa a tabela Cliente."""

    __tablename__ = "cliente"

    id = Column(Integer, primary_key=True)
    nome = Column(String)
    cpf = Column(String)
    endereco = Column(String)

    def __repr__(self):
        return f"Cliente(id={self.id}, nome={self.nome}, cpf={self.cpf}, endereco={self.endereco})"


class Conta(Base):
    """Classe que representa a tabela Conta."""

    __tablename__ = "conta"

    id = Column(Integer, primary_key=True)
    tipo = Column(String)
    agencia = Column(String)
    num = Column(Integer)
    saldo = Column(Numeric(10, 2))
    id_cliente = Column(Integer, ForeignKey("cliente.id"))
    cliente = relationship("Cliente", back_populates="contas")

    def __repr__(self):
        return f"Conta(id={self.id}, tipo={self.tipo}, agencia={self.agencia}, num={self.num}, saldo={self.saldo}, " \
               f"id_cliente={self.id_cliente})"


Cliente.contas = relationship("Conta", order_by=Conta.id, back_populates="cliente")

# conexão com o banco de dados
engine = create_engine("sqlite:///banco.db")

# Criando as tabelas no banco de dados
Base.metadata.create_all(engine)


def recuperar_todos_os_clientes(session):
    """
    Recupera todos os clientes da tabela Cliente e os imprime.

    Args:
        session: A sessão do SQLAlchemy para interagir com o banco de dados.
    """
    stmt_cliente = select(Cliente)
    print("\nRecuperando clientes...")
    for cliente in session.scalars(stmt_cliente):
        print(cliente)


def recuperar_todas_as_contas(session):
    """
    Recupera todas as contas da tabela Conta e as imprime.

    Args:
        session: A sessão do SQLAlchemy para interagir com o banco de dados.
    """
    stmt_conta = select(Conta)
    print("\nRecuperando contas...")
    for conta in session.scalars(stmt_conta):
        print(conta)


def buscar_cliente_por_nome(nome, session):
    """
    Busca um cliente pelo nome na tabela Cliente e o imprime.

    Args:
        nome: O nome do cliente a ser buscado.
        session: A sessão do SQLAlchemy para interagir com o banco de dados.
    """
    stmt_cliente = select(Cliente).where(Cliente.nome == nome)
    print(f"\nBuscando cliente por nome: {nome}")
    for cliente in session.scalars(stmt_cliente):
        print(cliente)


def buscar_conta_por_numero_agencia(numero, session):
    """
    Busca uma conta pelo número de agência na tabela Conta e a imprime.

    Args:
        numero: O número da agência da conta a ser buscada.
        session: A sessão do SQLAlchemy para interagir com o banco de dados.
    """
    stmt_conta = select(Conta).where(Conta.num == numero)
    print(f"\nBuscando conta por número de agência: {numero}")
    for conta in session.scalars(stmt_conta):
        print(conta)


# Investigando o esquema do banco de dados
inspector = inspect(engine)
print(inspector.has_table("cliente"))
print(inspector.has_table("conta"))
print(inspector.get_table_names())
print(inspector.default_schema_name)

# Criando registros de exemplo
clientes = [
    Cliente(nome="João", cpf="123456789", endereco="Rua A"),
    Cliente(nome="Maria", cpf="987654321", endereco="Rua B"),
    Cliente(nome="Pedro", cpf="456789123", endereco="Rua C"),
    Cliente(nome="Ana", cpf="321654987", endereco="Rua D")
]

contas = [
    Conta(tipo="Corrente", agencia="Agência 1", num=1, saldo=1000.0, cliente=clientes[0]),
    Conta(tipo="Poupança", agencia="Agência 2", num=2, saldo=2000.0, cliente=clientes[0]),
    Conta(tipo="Corrente", agencia="Agência 3", num=3, saldo=3000.0, cliente=clientes[1])
]

# Criando uma sessão para interagir com o banco de dados
with Session(engine) as session:
    session.add_all(clientes + contas)
    session.commit()

    recuperar_todos_os_clientes(session)
    print("---------------------------------------------------------")
    recuperar_todas_as_contas(session)
    print("---------------------------------------------------------")
    buscar_cliente_por_nome("João", session)
    print("---------------------------------------------------------")
    buscar_conta_por_numero_agencia(2, session)
