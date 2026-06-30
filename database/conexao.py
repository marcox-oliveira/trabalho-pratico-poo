import psycopg2
from psycopg2 import OperationalError
def obter_conexao():
    try:
        conexao = psycopg2.connect(
            host="localhost",
            database="musicstream",
            user="postgres",
            password="SUA SENHA",
            port=5432
        )
        return conexao
    except OperationalError as e:
        raise ConnectionError(f"Erro ao conectar ao banco de dados: {e}")

def fechar_conexao(conexao):
    if conexao and not conexao.closed:
        conexao.close()
