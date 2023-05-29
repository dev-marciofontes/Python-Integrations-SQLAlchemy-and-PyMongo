from pymongo import MongoClient


def conectar_mongodb(uri):
    """
    Conecta ao MongoDB usando a URI fornecida.

    Args:
        uri (str): URI de conexão ao MongoDB.

    Returns:
        MongoClient: Objeto de conexão ao MongoDB.
    """
    client = MongoClient(uri)
    return client


def obter_banco(client, nome_banco):
    """
    Obtém um banco de dados a partir do objeto de conexão ao MongoDB.

    Args:
        client (MongoClient): Objeto de conexão ao MongoDB.
        nome_banco (str): Nome do banco de dados.

    Returns:
        Database: Objeto do banco de dados.
    """
    return client[nome_banco]


def obter_colecao(banco, nome_colecao):
    """
    Obtém uma coleção a partir do objeto do banco de dados.

    Args:
        banco (Database): Objeto do banco de dados.
        nome_colecao (str): Nome da coleção.

    Returns:
        Collection: Objeto da coleção.
    """
    return banco[nome_colecao]


def inserir_documentos(colecao, documentos):
    """
    Insere documentos na coleção do MongoDB.

    Args:
        colecao (Collection): Objeto da coleção.
        documentos (list): Lista de documentos a serem inseridos.

    Returns:
        InsertManyResult: Objeto com informações do resultado da inserção.
    """
    result = colecao.insert_many(documentos)
    print(f"{result.inserted_ids} documentos inseridos com sucesso!")
    return result


def recuperar_informacoes(colecao, chave, valor):
    """
    Recupera informações da coleção do MongoDB com base em pares de chave e valor.

    Args:
        colecao (Collection): Objeto da coleção.
        chave (str): Chave para filtrar os documentos.
        valor (str): Valor correspondente à chave.

    Returns:
        Cursor: Cursor para iterar sobre os documentos encontrados.
    """
    query = {chave: valor}
    resultados = colecao.find(query)
    return resultados


def excluir_documentos(colecao, chave=None, valor=None):
    """
    Exclui documentos da coleção do MongoDB com base em pares de chave e valor.

    Se nenhum par de chave e valor for fornecido, a coleção inteira será excluída.

    Args:
        colecao (Collection): Objeto da coleção.
        chave (str): Chave para filtrar os documentos (opcional).
        valor (str): Valor correspondente à chave (opcional).
    """
    query = {}
    if chave and valor:
        query = {chave: valor}
    colecao.delete_many(query)
    print("Documentos excluídos com sucesso!")


def excluir_item(colecao, chave, valor):
    """
    Exclui um único item da coleção com base em um critério específico.

    Args:
        colecao (Collection): Objeto da coleção.
        chave (str): Chave para filtrar o item a ser excluído.
        valor (str): Valor correspondente à chave.

    Returns:
        DeleteResult: Objeto com informações do resultado da exclusão.
    """
    query = {chave: valor}
    result = colecao.delete_one(query)
    print(f"{result.deleted_count} documento excluído com sucesso!")
    return result


# Código de conexão com o MongoDB
uri = "mongodb+srv://pymongo:<suasenha>@<seucluster>.<iddocluster>.mongodb.net/?retryWrites=true&w=majority"

# Conecte ao MongoDB
client = conectar_mongodb(uri)

# Acesse o banco de dados
banco = obter_banco(client, "Banco")

# Defina a coleção "bank" para armazenar os documentos de clientes
colecao_bank = obter_colecao(banco, "bank")

# Definição dos documentos de clientes e contas
documentos = [
    {
        "nome": "Naruto Uzumaki",
        "cpf": "12345678901",
        "endereco": "Konoha Street",
        "conta": {
            "id": "1",
            "tipo": "Conta Corrente",
            "agencia": "Hidden Leaf Bank",
            "num": 1,
            "saldo": 1000.0
        }
    },
    {
        "nome": "Luffy Monkey D.",
        "cpf": "98765432109",
        "endereco": "One Piece Avenue",
        "conta": {
            "id": "2",
            "tipo": "Poupança",
            "agencia": "Sunny Bank",
            "num": 2,
            "saldo": 500.0
        }
    },
    {
        "nome": "Cloud Strife",
        "cpf": "45678912305",
        "endereco": "Final Fantasy Boulevard",
        "conta": {
            "id": "3",
            "tipo": "Investimento",
            "agencia": "Mako Bank",
            "num": 3,
            "saldo": 2000.0
        }
    },
    {
        "nome": "Zelda",
        "cpf": "78912345607",
        "endereco": "Hyrule Lane",
        "conta": {
            "id": "4",
            "tipo": "Conta Corrente",
            "agencia": "Castle Bank",
            "num": 4,
            "saldo": 1500.0
        }
    },
    {
        "nome": "Kirby",
        "cpf": "65478932105",
        "endereco": "Dream Land Street",
        "conta": {
            "id": "5",
            "tipo": "Poupança",
            "agencia": "Popopo Bank",
            "num": 5,
            "saldo": 200.0
        }
    },
    {
        "nome": "Sonic the Hedgehog",
        "cpf": "32165498708",
        "endereco": "Green Hill Road",
        "conta": {
            "id": "6",
            "tipo": "Investimento",
            "agencia": "Ring Bank",
            "num": 6,
            "saldo": 3000.0
        }
    }
]

# Insere os documentos na coleção "bank"
inserir_documentos(colecao_bank, documentos)

# Exemplo de recuperação de informações pelo nome do cliente
resultados_nome = recuperar_informacoes(colecao_bank, "nome", "Naruto Uzumaki")
for resultado in resultados_nome:
    print(resultado)

# Exemplo de recuperação de informações pelo tipo de conta
resultados_conta = recuperar_informacoes(colecao_bank, "conta.tipo", "Poupança")
for resultado in resultados_conta:
    print(resultado)

print("---------------------------------------------------------")
# Recupera todas as contas da coleção "bank"
resultados_contas = colecao_bank.find()
for resultado in resultados_contas:
    print(resultado)
print("---------------------------------------------------------")

# Exclui apenas o item com nome "Luffy Monkey D."
excluir_item(colecao_bank, "nome", "Luffy Monkey D.")

# Exclui todos os documentos da coleção "bank"
excluir_documentos(colecao_bank)
