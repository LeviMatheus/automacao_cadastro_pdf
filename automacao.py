#atividades PDF
from atividades_pdf import ler_pdf_binario, criar_pdf, pegar_pdfs, listar_pdfs, extrair_texto      
from atividades_sql import conectar_sql, criar_base                                          #conectar ao MySql
from validar_caminho import caminho_valido
import re                                                                           #operacoes de Regex
import pandas as pd                                                                 #Pandas

print(f'\n########## Automação: Cadastro por PDF ############')

#caminho até a pasta dos PDFS
caminho_pdfs = 'C:/Users/Gamer - PC/Documents/Códigos/alimentar base por pdf/pdfs/'
colunas = ['nome','email','celular','arquivo','conteudo']
print(f'# Lendo caminho: {caminho_pdfs}')
print(f'# Criando tabela com as colunas {colunas}')
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
    campos = {'nome':campo_nome, 'email':campo_email, 'celular':campo_celular,'arquivo':pdf, 'conteudo':dados_binario}
    #Adicionando a tabela
    dataframe_pdfs = dataframe_pdfs.append(campos, ignore_index=True)

print(f'\n# Criado Dataframe com conteudo lido dos PDFs.')


#Conectando ao banco
conexao_sql = conectar_sql("localhost", "root", 'senha')
criar_base(conexao_sql,'cadastro')

