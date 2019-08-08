def tira_paragrafo(texto):
    return texto.replace('\r\n',';')

def cria_lista(texto):
    return texto.strip().replace('\r\n',';').split(';')

def lista_para_texto(lista):
    texto = ';'.join(lista)
    return texto

def cria_lista_db(texto):
    return texto.strip().split(';')
    

def cria_texto_formulario(texto):
    return texto.strip().replace(';','\n')

def troca_por_nulo(valor):
    if valor == ' ' or '' or "" or " ":
        valor = None
    return valor
