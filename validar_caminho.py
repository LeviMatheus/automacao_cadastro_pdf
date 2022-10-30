import os #operacoes do sistema

def caminho_valido(caminho):
    #validar caminho
    if not os.path.exists(caminho):
        os.makedirs(caminho)
        return True
    elif not os.path.isdir(caminho):
        raise IOError(f'{caminho}')