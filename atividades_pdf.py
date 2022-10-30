import base64
import os
import PyPDF2 as leitor             #leitor PDF

def ler_pdf_binario(caminho):
    #ler
    with open(caminho, 'rb') as arquivo:
        blob = base64.b64encode(arquivo.read())
    return blob

def criar_pdf(nome_extensao,blob):
    #criar pdf
    blob = base64.b64decode(blob)
    arquivo = open(nome_extensao,'wb')
    arquivo.write(blob)
    arquivo.close()

def pegar_pdfs(caminho):
    caminhos = [os.path.join(caminho, nome) for nome in os.listdir(caminho)]
    #pegar os arquivos destas pastas
    print(f'# Coletando arquivos do diretório: {caminhos}')
    arquivos = [arq for arq in caminhos if os.path.isfile(arq)]
    #pegar somente os pdfs
    print(f'# Filtrando somente os PDFs')
    arquivos_pdfs = [arq for arq in arquivos if arq.lower().endswith(".pdf")]
    return arquivos_pdfs

def listar_pdfs(arquivos_pdfs):
    #Listar os pdfs encontrados
    print(f'\n############ PDFS encontrados ##############')
    for index, pdf in enumerate(arquivos_pdfs):
        print(f'PDF {index}: {pdf}')

def extrair_texto(pdf):
    print(f'# Lendo: {pdf}')
    #abrir arquivo
    try:
        #lendo arquivo
        dados_pdf = leitor.PdfFileReader(pdf, strict=False)
        for pagina in range(dados_pdf.numPages):
            #coletando conteudo da pagina atual
            temp_conteudo = dados_pdf.getPage(pagina)
            #extraindo texto do conteudo
            texto_extraido = temp_conteudo.extract_text()
            #print conteudo
            #print(f'\n Conteudo: {texto_extraido}')
            #concatenando conteudo
            texto_extraido += texto_extraido
    except:
        raise IOError(f'Erro ao tentar ler PDF {os.getcwd(pdf)}')

    return texto_extraido