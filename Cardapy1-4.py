# Cardapy 1.4 - Fechamento, Alteração, Exclusão e Menu Interativo (Matheus)


from base_dados import carregar_dados, salvar_dados
from visao import listar_registros, consultar_registro, _mostrar_comanda, _pegar

# Reaproveita o cadastro e as validações prontas, sem alterar as mesmas.
from cardapy import (
    cadastrar_comanda,
    _ler_texto_obrigatorio,
    _ler_inteiro_positivo,
    _ler_float_nao_negativo,
)


def _confirmar(prompt):
    # Pergunta s/n; qualquer resposta diferente de "s"/"sim" conta como não
    return input(f"{prompt} (s/n): ").strip().lower() in ("s", "sim")


def calcular_total(comanda):
    # Soma quantidade e preço de todos os itens
    return round(sum(
        _pegar(item, "quantidade", padrao=0) * _pegar(item, "preco_unitario", "preco", padrao=0)
        for item in comanda.get("itens", [])
    ), 2)


def _selecionar_comanda(comandas, acao):
    # Pede o ID ou o nome do cliente e devolve o ID da comanda 
    busca = input(f"ID ou nome do cliente da comanda que deseja {acao}: ").strip()

    # ID exato tem prioridade
    if busca in comandas:
        return busca

    achadas = [
        id_comanda for id_comanda, comanda in comandas.items()
        if busca and busca.lower() in str(_pegar(comanda, "responsavel", "cliente", padrao="")).lower()
    ]

    if not achadas:
        print(f"Nenhuma comanda encontrada para '{busca}'.")
        return None
    if len(achadas) > 1:
        print(f"Várias comandas encontradas: {', '.join('#' + i for i in achadas)}. Informe o ID exato.")
        return None
    return achadas[0]


def _ler_item():
    nome = _ler_texto_obrigatorio("Descrição do item: ")
    quantidade = _ler_inteiro_positivo("Quantidade: ")
    preco = _ler_float_nao_negativo("Preço unitário (R$): ")
    return {"item": nome, "quantidade": quantidade, "preco_unitario": preco,
            "subtotal": round(quantidade * preco, 2)}


def _ler_posicao(itens):
    # Mostra os itens numerados, e devolve o índice escolhido
    for numero, item in enumerate(itens, start=1):
        print(f"  {numero}. {_pegar(item, 'item', 'produto', padrao='?')} | {_pegar(item, 'quantidade', padrao=0)}x")
    while True:
        numero = _ler_inteiro_positivo("Número do item: ")
        if numero <= len(itens):
            return numero - 1
        print(f"Erro: escolha um número entre 1 e {len(itens)}.")


def fechar_comanda(comandas):
    print("\n=== Fechar Comanda ===")
    id_comanda = _selecionar_comanda(comandas, "fechar")
    if id_comanda is None:
        return

    comanda = comandas[id_comanda]
    if comanda.get("status") == "fechada":
        print(f"A comanda #{id_comanda} já está fechada.")
        return
    if not comanda.get("itens"):
        print("Erro: a comanda não possui itens, não é possível fechar.")
        return

    # Este segmento Calcula o valor final com base nos itens e mostra a comanda . 
    total = calcular_total(comanda)
    _mostrar_comanda(id_comanda, comanda)
    print(f"Valor final a pagar: R$ {total:.2f}")

    if _confirmar("Confirmar o fechamento?"):
        comanda["status"] = "fechada"
        comanda["total"] = total
        salvar_dados(comandas)
        print(f"Comanda #{id_comanda} fechada com sucesso!")
    else:
        print("Fechamento cancelado.")


def alterar_comanda(comandas):
    print("\n=== Alterar Comanda ===")
    id_comanda = _selecionar_comanda(comandas, "alterar")
    if id_comanda is None:
        return

    comanda = comandas[id_comanda]
    if comanda.get("status") == "fechada":
        print(f"Erro: a comanda #{id_comanda} já está fechada e não pode ser alterada.")
        return

    itens = comanda.setdefault("itens", [])

    # Repete até o usuário escolher voltar.
    while True:
        _mostrar_comanda(id_comanda, comanda)
        opcao = input("1-Cliente/mesa  2-Adicionar item  3-Alterar item  4-Remover item  0-Voltar: ").strip()

        if opcao == "0":
            return
        elif opcao == "1":
            # Mantém o nome do campo que a comanda já usa (cliente ou responsavel)
            chave = "cliente" if "cliente" in comanda else "responsavel"
            comanda[chave] = _ler_texto_obrigatorio("Novo nome do cliente ou mesa: ")
        elif opcao == "2":
            itens.append(_ler_item())
        elif opcao in ("3", "4") and itens:
            posicao = _ler_posicao(itens)
            if opcao == "3":
                itens[posicao] = _ler_item()
            elif len(itens) > 1:
                itens.pop(posicao)
            else:
                print("Erro: a comanda precisa de ao menos 1 item. Use a opção Excluir.")
                continue
        else:
            print("Erro: opção inválida.")
            continue

        # Recalcula o total e salva após a alteração
        comanda["total"] = calcular_total(comanda)
        salvar_dados(comandas)
        print("Comanda atualizada e salva com sucesso!")


def excluir_comanda(comandas):
    print("\n=== Excluir Comanda ===")
    id_comanda = _selecionar_comanda(comandas, "excluir")
    if id_comanda is None:
        return

    _mostrar_comanda(id_comanda, comandas[id_comanda])
    if _confirmar(f"Excluir a comanda #{id_comanda}?"):
        del comandas[id_comanda]
        salvar_dados(comandas)
        print(f"Comanda #{id_comanda} excluída com sucesso!")
    else:
        print("Exclusão cancelada.")


def menu_principal():
    # Carrega os dados salvos
    comandas = carregar_dados()

    # Cada opção do menu chama uma função dos participantes
    opcoes = {
        "1": cadastrar_comanda,
        "2": listar_registros,
        "3": consultar_registro,
        "4": alterar_comanda,
        "5": excluir_comanda,
        "6": fechar_comanda,
    }

    while True:
        print("\n===== CARDAPY - COMANDAS =====")
        print("1 - Cadastrar   2 - Listar   3 - Consultar")
        print("4 - Alterar     5 - Excluir  6 - Fechar     0 - Sair")

        try:
            opcao = input("Escolha uma opção: ").strip()
        except (EOFError, KeyboardInterrupt):
            # Evita quebrar o sistema com Ctrl+C / Ctrl+D
            opcao = "0"

        if opcao == "0":
            print("\nEncerrando o sistema. Até logo!")
            break
        elif opcao in opcoes:
            opcoes[opcao](comandas)
        else:
            print("Erro: opção inválida. Digite um número de 0 a 6.")


# Executa o menu apenas quando este arquivo é rodado diretamente
if __name__ == "__main__":
    menu_principal()
