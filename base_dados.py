import json

#Variável que contém o arquivo responsável por salvar os dados das comandas
ARQUIVO = "comandas.json"

#Função responsável por carregar os dados do salvos no arquivo .json
def carregar_dados():
    try:
        with open(ARQUIVO, "r", encoding="utf-8") as arquivo:
            return json.load(arquivo)

    except FileNotFoundError:
        #Caso ainda não exista um arquivo ainda, a função retorna um dicionário vazio
        return{}


#Função responsável por salvar os dados da comanda no arquivo .json
def salvar_dados(comandas):
    with open(ARQUIVO, "w", encoding="utf-8") as arquivo:
        json.dump(comandas, arquivo, indent=4, ensure_ascii=False)