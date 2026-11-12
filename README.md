README - CARDAPY


Integrantes: Guilherme Eduardo, Guilherme Leandro, Matheus de Moura, Sofia Pericin.
Tema: Sistema de Comandas para Restaurante


        Este projeto tem como objetivo o desenvolvimento de um sistema de comandas para restaurante através da linguagem python.


- Base e Estrutura de dados: (Hubner)


* Base e estrutura de memória: Definição do formato da base de dados (Dicionários e listas) para representar os registros de informações.

* Leitura de arquivos('Carregamento de dados'): Implementação de leitura de arquivos (.txt, .json ou .csv), tratar exceção 'FileNotFoundError' criando uma estrutura vazia se o arquivo não existir.


   * Escrita de Arquivo: Implementação de escrita/atualização de dados no arquivo físico diretamente no disco para que os dados persistam entre atualizações.


________________




-Entrada(Cadastro, Validações e Tratamento de Erros): (Leandro)


   * Cadastro: Criar função para cadastrar os dados do novo registro via terminal.


   * ID Único: Implementação de lógica de geração ou validação de identificador único sem duplicidades


   * Validação com try/except: impedir entradas inválidas (textos em campos numéricos, valores negativos, campos vazios) garantindo estabilidade do sistema.


   * Integração: Inserir os dados validados na estrutura de memória e invocar a instrução ‘salvar_dados’.




________________




-Visão(Listagem e Consulta/Pesquisa) (Sophia)


   * Listagem (`listar_registros()`): Desenvolver a exibição organizada de todos os registros armazenados. Tratar o caso de lista vazia com mensagem amigável.


   * Consulta (`consultar_registro()`): Permitir pesquisar um registro específico por ID/código ou nome.


   * Tratamento de Erros: Tratar pesquisas que não retornem resultados sem interromper o sistema.
________________




-Fechamento(Alteração, Exclusão e Interface) (Matheus)


A FAZER
   * Fechamento do código e valor final dos produtos com base na comanda 


   * Alteração: Alterar registro, localizar um registro existente e permitir a atualização dos seus campos, salvando o arquivo em seguida. 


   * Exclusão: Permitir a remoção de um registro com base em sua denominação e atualizar o arquivo. (Menu Interativo): 


   * Construir um loop principal (`while True`) com opções para sair, integrando todas as funções dos 4 participantes com tratamento de entradas inválidas no menu.