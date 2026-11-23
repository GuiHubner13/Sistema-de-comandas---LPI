README - CARDAPY


Integrantes: Guilherme Eduardo, Guilherme Leandro, Matheus de Moura, Sofia Pericin.
Tema: Sistema de Comandas para Restaurante


        Este projeto tem como objetivo o desenvolvimento de um sistema de comandas para restaurante através da linguagem python.


- Base e Estrutura de dados: (Guilherme Eduardo)


* Base e estrutura de memória: Definição do formato da base de dados (Dicionários e listas) para representar os registros de informações.

* Leitura de arquivos('Carregamento de dados'): Implementação de leitura de arquivos (.txt, .json ou .csv), tratar exceção 'FileNotFoundError' criando uma estrutura vazia se o arquivo não existir.


   * Escrita de Arquivo: Implementação de escrita/atualização de dados no arquivo físico diretamente no disco para que os dados persistam entre atualizações.


________________




-Entrada(Cadastro, Validações e Tratamento de Erros): (Guilherme Leandro)


   * Cadastro: Criar função para cadastrar os dados do novo registro via terminal.


   * ID Único: Implementação de lógica de geração ou validação de identificador único sem duplicidades


   * Validação com try/except: impedir entradas inválidas (textos em campos numéricos, valores negativos, campos vazios) garantindo estabilidade do sistema.


   * Integração: Inserir os dados validados na estrutura de memória e invocar a instrução ‘salvar_dados’.




________________




-Visão(Listagem e Consulta/Pesquisa): (Sofia)


   * Listagem (`listar_registros()`): Desenvolver a exibição organizada de todos os registros armazenados. Tratar o caso de lista vazia com mensagem amigável.


   * Consulta (`consultar_registro()`): Permitir pesquisar um registro específico por ID/código ou nome.


   * Tratamento de Erros: Tratar pesquisas que não retornem resultados sem interromper o sistema.
________________




-Fechamento(Alteração, Exclusão e Interface): (Matheus)



   * Fechamento do código e valor final dos produtos com base na comanda 


   * Alteração: Alterar registro, localizar um registro existente e permitir a atualização dos seus campos, salvando o arquivo em seguida. 


   * Exclusão: Permitir a remoção de um registro com base em sua denominação e atualizar o arquivo. (Menu Interativo): 


   * Construir um loop principal (`while True`) com opções para sair, integrando todas as funções dos 4 participantes com tratamento de entradas inválidas no menu.


---

Atualização 1.1:

--------------- Estrutura de Dados(`base_dados.py`) -----------------------------------------------------------------------------

--------------- MANTER OS IDs DAS COMANDAS COMO STRING PRA O FUNCIONAMENTO CORRETO DO CÓDIGO! -----------------------------------

--------------- Sempre que uma comanda for cadastrada, alterada ou excluída, chamem salvar_dados(comandas) logo em seguida ------


O módulo `base_dados.py` já está implementado e deve ser importado pelos demais arquivos do projeto assim:

```python

from base_dados import carregar_dados, salvar_dados

#Como ficou definida a estrutura das comandas no código: 
comandas = {
    "182": {
        "cliente": "Alessandro Santos",
        "itens": [
            {"produto": "X-Salada", "quantidade": 2, "preco": 25.50},
            {"produto": "Coca-Cola", "quantidade": 1, "preco": 6.00}
        ]
    }
}

```

Atualização 1.2:

base dados.py foi atualizada incluindo um tratamento de erro para os arquivos .json

também foi implementado o sistema de entrada e armazenamento de dados das comandas no arquivo Cardapy1.2.py

```python

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

```

Atualização 1.3:

Foi implementado o arquivo visao.py (Sofia), com a listagem e a consulta de comandas. As funções aceitam o formato de comanda do Cardapy1.2.py e também o formato da Atualização 1.1.

- listar_registros(comandas): mostra todas as comandas de forma organizada. Se não houver nenhuma, exibe uma mensagem amigável.
- consultar_registro(comandas): pesquisa comandas por ID ou por nome do cliente. Se não encontrar nada, avisa sem interromper o programa.

Para usar no menu:

from visao import listar_registros, consultar_registro

```python

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

```


Atualização 1.4 (Matheus):

Foi implementado o arquivo Cardapy1.4.py, com o fechamento, a alteração, a exclusão, e o menu interativo. Ele integra as funções em geral e é o arquivo que deve ser executado para rodar o sistema:

python Cardapy1.4.py


```
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
```
**Observações:**
```
fechar_comanda(comandas):
```
localiza a comanda por ID ou nome do cliente, calcula o valor final com base nos itens e, após confirmação, muda o status para "fechada", grava o total e salva. Não fecha comanda já fechada nem sem itens.
```
alterar_comanda(comandas):
```
permite alterar o nome do cliente/mesa e adicionar, alterar ou remover itens. Recalcula o total e salva após cada alteração. Comandas fechadas não podem ser alteradas.
```
excluir_comanda(comandas):
```
 localiza a comanda por ID ou nome, pede confirmação, remove e atualiza o arquivo.
 ```
menu_principal():
```
 loop principal (while True) com as opções:
```
1 - Cadastrar | 2 - Listar | 3 - Consultar | 4 - Alterar | 5 - Excluir | 6 - Fechar | 0 - Sair
Opções inválidas no menu são tratadas sem interromper o sistema.
```
Observe-se que:
- Os IDs continuam como "string".
- Reaproveita cadastrar_comanda e as validações do Cardapy1.2.py, e listar_registros / consultar_registro do visao.py, sem alterá-los.
