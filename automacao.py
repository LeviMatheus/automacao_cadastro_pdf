#atividades PDF
from regex import Regex
from atividades_pdf import ler_pdf_binario, criar_pdf, pegar_pdfs, listar_pdfs, extrair_texto, nome_pdf  
from atividades_sql import conectar_sql, criar_base, executar_comando, conectar_base, executar_insert#conectar ao MySql
from validar_caminho import caminho_valido
import re                                                                           #operacoes de Regex
import pandas as pd                                                                 #Pandas
import shutil

print(f'/n########## Automação: Cadastro por PDF ############/n')

#caminho até a pasta dos PDFS
caminho_pdfs_novos = 'C:/Users/Gamer - PC/Documents/Códigos/automacao_cadastro_pdf/pdfs/'
caminho_pdfs_adicionados = 'C:/Users/Gamer - PC/Documents/Códigos/automacao_cadastro_pdf/pdfs/Adicionados/'
nome_base = 'cadastro'
nome_tabela = 'cadastro'
servidor = 'localhost'
usuario = 'root'
senha = '1998'
colunas = ('nome','email','celular','arquivo','conteudo')
dados_binario = ''
print(f'/n# Lendo caminho: {caminho_pdfs_novos}')

#Validando caminho informado
caminho_valido(caminho_pdfs_novos)
#listar as pastas presentes no caminho informado
arquivos_pdfs = pegar_pdfs(caminho_pdfs_novos)
listar_pdfs(arquivos_pdfs)

#Funcao para encontrar campos
def match_regex_after(palavra,texto):
    return str(re.search(f'(?<={palavra}\:).*',texto)[0]).strip(" ")

#Conectando ao banco
conexao_sql = conectar_sql(f'{servidor}', f'{usuario}', f'{senha}')
criar_base(conexao_sql,f'{nome_base}')
conexao_sql = conectar_base(f'{servidor}', f'{usuario}', f'{senha}',f'{nome_base}')
#Comando de criar a tabela de cadastro
criar_tabela_cadastro = f"""
CREATE TABLE {nome_tabela} (
  cadastro_id INT PRIMARY KEY AUTO_INCREMENT,
  nome VARCHAR(200) NOT NULL,
  email VARCHAR(200) NOT NULL,
  celular VARCHAR(50) NOT NULL,
  arquivo VARCHAR(100) NOT NULL,
  conteudo LONGBLOB NOT NULL
  );
 """
#Criar tabela
executar_comando(conexao_sql,criar_tabela_cadastro)

#Ler os pdfs encontrados
print(f'/n###### Lendo os PDFs encontrados #############')
for index, pdf in enumerate(arquivos_pdfs):
    texto_extraido = extrair_texto(pdf)
    dados_binario = ler_pdf_binario(pdf)
    #Coletar campos do texto extraido
    print(f"# Coletando informações dos PDFs")
    try:
        campo_nome = match_regex_after("Nome",texto_extraido)
        campo_email = match_regex_after("Email",texto_extraido)
        campo_celular = match_regex_after("Celular",texto_extraido)
    except Exception as err:
        print(f"/n!!! Erro ao aplicar Expressões regulares no conteúdo lido do pdf. Erro: {err}")
    #adicionando novos campo a tabela
    print(f"Inserindo dados do PDF na tabela: {nome_tabela}")
    inserir_novo_cadastro = f"""INSERT INTO {nome_tabela} (nome,email,celular,arquivo,conteudo) VALUES (%s,%s,%s,%s,%s)"""
    parametros = (campo_nome,campo_email,campo_celular,pdf,dados_binario)
    executar_insert(conexao_sql,inserir_novo_cadastro,parametros)
    #Mover pdf para pasta de feitos
    print(f"Movendo PDF para a pasta de Adicionados\n")
    shutil.move(pdf, caminho_pdfs_adicionados)