import mysql.connector              #Conector MySql
from mysql.connector import Error   #Facilitar o gerenciador de erros

#Conectando ao banco de dados
def conectar_sql(host, nome_usuario, senha):
    print(f"\n# Conectando ao host: {host} ...")
    conexao = None
    try:
        conexao = mysql.connector.connect(
            host=host,
            user=nome_usuario,
            passwd=senha
        )
        print(f"# Conectado a {host}")
    except Error as err:
        print(f"\n!!! Erro ao tentar conectar ao MySql: '{err}'")

    return conexao

def conectar_base(host, nome_usuario, senha, db):
    print(f"\n# Conectando à base de dados: {db} ...")
    try:
        conexao = mysql.connector.connect(
            host=host,
            user=nome_usuario,
            passwd=senha,
            database=db
        )
        print(f"# Conectado à base de dados: {db}")
    except Error as err:
        print(f"\n!!! Erro ao tentar conectar à base de dados: '{db}'")

    return conexao

def criar_base(conexao, base):
    print(f'# Criando a base de dados: {base}')
    cursor = conexao.cursor()
    try:
        cursor.execute(f'CREATE DATABASE {base}')
        print(f'# Base de dados {base} criada com sucesso')
    except Error as err:
        print(f"\n!!! Error ao criar a base de dados {base}: '{err}'")

def executar_comando(conexao, comando):
    cursor = conexao.cursor()
    try:
        cursor.execute(comando)
        conexao.commit()
        print(f"Comando SQL realizado.")
    except Error as err:
        print(f"\n!!! Error no comando SQL {err}")

def executar_insert(conexao, comando, parametros):
    cursor = conexao.cursor()
    try:
        cursor.execute(comando, parametros)
        conexao.commit()
        print(f"INSERT realizado.")
    except Error as err:
        print(f"\n!!! Error no comando INSERT: {err}")