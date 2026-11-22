from base_dados import carregar_dados


def _pegar(dicionario, *chaves, padrao=None):
    # Procura o primeiro nome de campo que existir (aceita os dois formatos do projeto)
    for chave in chaves:
        if chave in dicionario:
            return dicionario[chave]
    return padrao


def _mostrar_comanda(id_comanda, comanda):
    # Mostra uma comanda formatada na tela
    cliente = _pegar(comanda, "responsavel", "cliente", padrao="Não informado")
    status = comanda.get("status", "aberta")

    print("-" * 40)
    print(f"Comanda #{id_comanda}")
    print(f"Cliente/Mesa: {cliente}")
    print(f"Status: {status}")
    print("Itens:")

    total = 0
    for item in comanda.get("itens", []):
        nome = _pegar(item, "item", "produto", padrao="?")
        qtd = _pegar(item, "quantidade", padrao=0)
        preco = _pegar(item, "preco_unitario", "preco", padrao=0)
        subtotal = _pegar(item, "subtotal", padrao=qtd * preco)
        total += subtotal
        print(f"  - {nome} | {qtd}x R$ {preco:.2f} = R$ {subtotal:.2f}")

    # Usa o total salvo na comanda; se não existir, usa a soma calculada
    total = comanda.get("total", total)
    print(f"Total: R$ {total:.2f}")
    print("-" * 40)


def listar_registros(comandas):
    print("\n=== Lista de Comandas ===")

    # Trata o caso de lista vazia com mensagem amigável
    if not comandas:
        print("Nenhuma comanda cadastrada ainda. Que tal cadastrar a primeira?")
        return

    for id_comanda, comanda in comandas.items():
        _mostrar_comanda(id_comanda, comanda)

    print(f"Total de comandas: {len(comandas)}")


def consultar_registro(comandas):
    print("\n=== Consultar Comanda ===")

    if not comandas:
        print("Nenhuma comanda cadastrada para consultar.")
        return

    busca = input("Digite o ID ou o nome do cliente: ").strip()

    if not busca:
        print("Você não digitou nada. Tente novamente.")
        return

    encontradas = []

    # Procura por ID exato ou por nome (parcial, sem diferenciar maiúsculas)
    for id_comanda, comanda in comandas.items():
        nome = str(_pegar(comanda, "responsavel", "cliente", padrao="")).lower()
        if busca == id_comanda or busca.lower() in nome:
            encontradas.append((id_comanda, comanda))

    # Trata pesquisa sem resultado sem quebrar o sistema
    if not encontradas:
        print(f"Nenhuma comanda encontrada para '{busca}'.")
        return

    print(f"\n{len(encontradas)} comanda(s) encontrada(s):")
    for id_comanda, comanda in encontradas:
        _mostrar_comanda(id_comanda, comanda)


# Teste rápido: só roda se executar este arquivo diretamente
if __name__ == "__main__":
    dados = carregar_dados()
    listar_registros(dados)
    consultar_registro(dados)