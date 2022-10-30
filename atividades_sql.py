import mysql.connector              #Conector MySql
from mysql.connector import Error   #Facilitar o gerenciador de erros

pwd = '1998'

#Conectando ao banco de dados
def conectar_sql(host, nome_usuario, senha):
    print(f"\n# Conectando ao host: {host} ...")
    conexao = None
    try:
        conexao = mysql.connector.connect(
            host=host,
            user=nome_usuario,
            passwd=pwd
        )
        print(f"# Conectado a {host}")
    except Error as err:
        print(f"\n!!! Erro ao tentar conectar ao MySql: '{err}'")

    return conexao

def criar_base(conexao, base):
    print(f'# Criando a base de dados: {base}')
    cursor = conexao.cursor()
    try:
        cursor.execute(f'CREATE DATABASE {base}')
        print(f'# Base de dados {base} criada com sucesso')
    except Error as err:
        print(f"\n!!! Error ao criar a base de dados {base}: '{err}'")