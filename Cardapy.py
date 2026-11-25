import math  # Usado para verificar valores numéricos especiais

# Importa as funções de persistência já definidas no módulo base_dados
from base_dados import carregar_dados, salvar_dados


def _ler_texto_obrigatorio(prompt):
    # Repete a pergunta até o usuário digitar algum texto não vazio
    while True:
        # Remove espaços extras nas pontas para evitar entradas como "   "
        valor = input(prompt).strip()
        if valor:
            return valor
        print("Erro: este campo não pode ficar vazio. Tente novamente.")


def _ler_inteiro_positivo(prompt, minimo=1):
    # Repete até receber um número inteiro válido e maior ou igual ao mínimo exigido
    while True:
        entrada = input(prompt).strip()
        try:
            # Tenta converter a entrada para inteiro; se houver letras ou símbolos, cai no except
            numero = int(entrada)
            if numero < minimo:
                print(f"Erro: informe um número inteiro maior ou igual a {minimo}.")
                continue
            return numero
        except ValueError:
            print("Erro: entrada inválida. Digite apenas números inteiros.")


def _ler_float_nao_negativo(prompt):
    # Repete até receber um valor decimal válido maior ou igual a zero (ex.: preço)
    while True:
        # Aceita tanto vírgula quanto ponto como separador decimal
        entrada = input(prompt).strip().replace(",", ".")
        try:
            valor = float(entrada)
            # Garante que o número seja finito (rejeita 'nan' e 'inf') e não seja negativo
            if math.isnan(valor) or math.isinf(valor) or valor < 0:
                print("Erro: informe um valor numérico válido maior ou igual a zero.")
                continue
            # Arredonda para 2 casas decimais para trabalhar com valores monetários
            return round(valor, 2)
        except ValueError:
            print("Erro: entrada inválida. Digite um valor numérico (ex.: 15.50).")


def _gerar_proximo_id(comandas):
    # Coleta apenas os IDs existentes que sejam números inteiros para calcular o próximo
    ids_numericos = []
    for chave in comandas:
        try:
            ids_numericos.append(int(chave))
        except ValueError:
            # Ignora chaves que não sejam numéricas (ex.: "MESA-A")
            continue

    # Pega o maior ID numérico encontrado e soma 1 (ou começa em 1 se não houver nenhum)
    proximo = max(ids_numericos, default=0) + 1

    # Garante que o ID gerado ainda não exista no dicionário de comandas
    while str(proximo) in comandas:
        proximo += 1

    return str(proximo)


def _solicitar_id_unico(comandas):
    # Solicita um ID manual ou gera um automaticamente se o campo ficar em branco
    while True:
        entrada = input("ID da comanda (deixe em branco para gerar automaticamente): ").strip()
        if not entrada:
            return _gerar_proximo_id(comandas)
        # Impede cadastrar duas comandas com o mesmo identificador
        if entrada in comandas:
            print(f"Erro: o ID '{entrada}' já está em uso. Informe outro ID.")
            continue
        return entrada


def cadastrar_comanda(comandas):
    print("\n=== Nova Comanda ===")

    # Obtém um ID único (informado pelo usuário ou gerado automaticamente)
    id_comanda = _solicitar_id_unico(comandas)

    # Lê o nome do cliente ou identificação da mesa sem permitir campo em branco
    responsavel = _ler_texto_obrigatorio("Nome do cliente ou identificação da mesa: ")

    # Lista que armazenará todos os itens adicionados a esta comanda
    itens = []

    # Loop para cadastrar um ou mais itens na comanda
    while True:
        print("\n--- Adicionar Item ---")
        nome_item = _ler_texto_obrigatorio("Descrição do item: ")
        quantidade = _ler_inteiro_positivo("Quantidade: ", minimo=1)
        preco_unitario = _ler_float_nao_negativo("Preço unitário (R$): ")

        # Calcula o subtotal do item e adiciona na lista de itens da comanda
        subtotal = round(quantidade * preco_unitario, 2)
        itens.append(
            {
                "item": nome_item,
                "quantidade": quantidade,
                "preco_unitario": preco_unitario,
                "subtotal": subtotal,
            }
        )

        # Pergunta se deseja incluir mais itens, validando a resposta
        while True:
            continuar = input("Adicionar outro item? (s/n): ").strip().lower()
            if continuar in ("s", "sim"):
                adicionar_mais = True
                break
            if continuar in ("n", "nao", "não"):
                adicionar_mais = False
                break
            print("Erro: responda apenas com 's' para sim ou 'n' para não.")

        # Encerra o loop de itens caso o usuário tenha respondido 'n'
        if not adicionar_mais:
            break

    # Soma todos os subtotais para obter o valor total da comanda
    total = round(sum(item["subtotal"] for item in itens), 2)

    # Insere a nova comanda completa na estrutura em memória usando o ID único como chave
    comandas[id_comanda] = {
        "id": id_comanda,
        "responsavel": responsavel,
        "status": "aberta",
        "itens": itens,
        "total": total,
    }

    # Persiste a estrutura atualizada no arquivo JSON via função do base_dados
    salvar_dados(comandas)

    print(f"\nComanda #{id_comanda} cadastrada e salva com sucesso! Total: R$ {total:.2f}")
    return comandas[id_comanda]


# Executa um fluxo de exemplo apenas quando este arquivo é rodado diretamente
if __name__ == "__main__":
    # Carrega os dados existentes antes de iniciar o cadastro
    dados_comandas = carregar_dados()
    cadastrar_comanda(dados_comandas)
