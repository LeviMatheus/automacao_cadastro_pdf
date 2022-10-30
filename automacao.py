#atividades PDF
from atividades_pdf import ler_pdf_binario, criar_pdf, pegar_pdfs, listar_pdfs, extrair_texto, nome_pdf  
from atividades_sql import conectar_sql, criar_base, executar_comando, conectar_base#conectar ao MySql
from validar_caminho import caminho_valido
import re                                                                           #operacoes de Regex
import pandas as pd                                                                 #Pandas

print(f'\n########## Automação: Cadastro por PDF ############\n')

#caminho até a pasta dos PDFS
caminho_pdfs = 'C:/Users/Gamer - PC/Documents/Códigos/automacao_cadastro_pdf/pdfs/'
colunas = ['nome','email','celular','arquivo','conteudo']
print(f'\n# Lendo caminho: {caminho_pdfs}')
print(f'\n# Criando tabela com as colunas {colunas}')
#Criando Dataframe que vai conter as informacoes
dataframe_pdfs = pd.DataFrame([],columns=colunas)

#Validando caminho informado
caminho_valido(caminho_pdfs)
#listar as pastas presentes no caminho informado
arquivos_pdfs = pegar_pdfs(caminho_pdfs)
listar_pdfs(arquivos_pdfs)

def match_regex_after(palavra,texto):
    return str(re.search(f'(?<={palavra}\:).*',texto)[0]).strip(" ")

#Ler os pdfs encontrados
print(f'\n###### Lendo os PDFs encontrados #############')
for index, pdf in enumerate(arquivos_pdfs):
    texto_extraido = extrair_texto(pdf)
    dados_binario = ler_pdf_binario(pdf)
    #Coletar campos do texto extraido
    campo_nome = match_regex_after("Nome",texto_extraido)
    campo_email = match_regex_after("Email",texto_extraido)
    campo_celular = match_regex_after("Celular",texto_extraido)
    #adicionando novos campo a tabela
    campos = {'nome':f'{campo_nome}', 'email':f'{campo_email}', 'celular':f'{campo_celular}', 'arquivo':f'{pdf}', 'conteudo':f'{dados_binario}'}
    #Adicionando a tabela
    dataframe_pdfs = dataframe_pdfs.append(campos, ignore_index=True)

print(f'\n# Criado Dataframe com conteudo lido dos PDFs.')

#Conectando ao banco
conexao_sql = conectar_sql("localhost", "root", '1998')
criar_base(conexao_sql,'cadastro')
conexao_sql = conectar_base("localhost", "root", '1998','cadastro')
#Comando de criar a tabela de cadastro
criar_tabela_cadastro = """
CREATE TABLE cadastro (
  cadastro_id INT PRIMARY KEY AUTO_INCREMENT,
  nome VARCHAR(200) NOT NULL,
  email VARCHAR(200) NOT NULL,
  celular VARCHAR(50) NOT NULL,
  arquivo VARCHAR(100) NOT NULL,
  conteudo BLOB NOT NULL
  );
 """
#Criar tabela
executar_comando(conexao_sql,criar_tabela_cadastro)

#Printar a base de dados
#print('\n',dataframe_pdfs)

#Iterar a dataframe para preencher a base de dados cadastro
for indice, registro in dataframe_pdfs.iterrows():
    #novo registro
    inserir_novo_cadastro = f""" INSERT INTO cadastro
    VALUES ('{registro['nome']}', '{registro['email']}', '{registro['celular']}', '{registro['arquivo']}', {registro['conteudo']} ); """

    #print("########### COMANDO #############")
    #print(inserir_novo_cadastro)
    #print("########### COMANDO #############")
    #print(f'{indice}:{registro}')
    #print(f"# Comando: {inserir_novo_cadastro}")
    executar_comando(conexao_sql,inserir_novo_cadastro)
