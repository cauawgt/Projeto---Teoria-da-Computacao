-----

# Biblioteca de Autómatos Finitos 

Este projeto consiste numa biblioteca em Python para a criação, manipulação e utilização de **Autómatos Finitos Determinísticos (AFD)** e **Não-Determinísticos (AFND)**. A principal funcionalidade implementada é a **busca de padrões em texto**, utilizando a abordagem clássica da teoria da computação: construir um autómato que reconhece um padrão e, em seguida, usá-lo para processar um texto de forma eficiente.

O projeto foi desenvolvido como parte de um Exercício-Programa, com o objetivo de aplicar conceitos de linguagens formais e autômatos de maneira prática.

-----

## \#\# Funcionalidades 🚀

  * **Representação de Autómatos**: Classes `AFD` e `AFND` para modelar autômatos com os seus estados, alfabeto, transições, estado inicial e estados finais.
  * **Persistência em Ficheiro**: Funções para **salvar e carregar** autômatos num formato de texto simples e legível.
  * **Construção de Autômato para Padrões**: Algoritmo para gerar um **AFND** que reconhece uma dada palavra (padrão). A construção do AFND é notavelmente simples e intuitiva.
  * **Conversão AFND ➡️ AFD**: Implementação do algoritmo de **Construção de Subconjuntos** para converter um AFND (mesmo com transições épsilon) num AFD totalmente equivalente. Esta é a base para a simulação eficiente.
  * **Busca Eficiente**: Utilização do AFD convertido para percorrer um texto e encontrar todas as ocorrências do padrão original.

-----

## \#\# Formato do Ficheiro de Autômato

Para garantir a interoperabilidade e a legibilidade, foi definido um formato de ficheiro de texto (`.dfa` ou `.nfa`) simples e claro.

A estrutura é baseada em tags seguidas por dois pontos (`:`), com uma tag especial para as transições.

  * `TIPO`: Especifica se é `AFD` ou `AFND`.
  * `ESTADOS`: Lista de todos os estados, separados por vírgula.
      * Exemplo: `ESTADOS:q0,q1,q2`
  * `ALFABETO`: Lista de todos os símbolos do alfabeto, separados por vírgula.
      * Exemplo: `ALFABETO:a,b,c`
  * `INICIAL`: O nome do estado inicial.
      * Exemplo: `INICIAL:q0`
  * `FINAIS`: Lista dos estados finais, separados por vírgula.
      * Exemplo: `FINAIS:q2`
  * `TRANSICOES:`: Todas as linhas seguintes a esta tag definem as transições no formato `origem,simbolo,destino1,destino2,...`.
      * **AFD**: `q0,a,q1`
      * **AFND (múltiplos destinos)**: `q0,a,q0,q1`
      * **AFND (transição épsilon)**: `q1,EPSILON,q2`

#### Exemplo de Ficheiro (`meu_afnd.nfa`)

```
TIPO:AFND
ESTADOS:q0,q1,q2
ALFABETO:a,b
INICIAL:q0
FINAIS:q2
TRANSICOES:
q0,a,q0,q1
q0,b,q0
q1,b,q2
```

-----

## \#\# Estrutura do Projeto 📂

O código está organizado como um pacote Python para promover modularidade e clareza.

```
/
|
├── automatos/              # O pacote da biblioteca
|   ├── __init__.py         # Ponto de entrada do pacote, exporta as funcionalidades
|   ├── afd.py              # Classe AFD e funções relacionadas
|   └── afnd.py             # Classe AFND e funções relacionadas
|   └── conversao.py        # Algoritmo de conversão AFND -> AFD
|
├── examples/               # Exemplos de uso prático
|   └── exemplo_busca_padrao.py
|
└── README.md               # Esta documentação
```

-----

## \#\# Como Usar

### Pré-requisitos

  * Python 3.x

### Executando o Exemplo

1.  Clone o repositório para a sua máquina.
2.  Navegue até o diretório do projeto.
3.  Execute o ficheiro de exemplo principal para ver a biblioteca em ação:
    ```bash
    python examples/exemplo_busca_padrao.py
    ```

O script irá:

1.  Definir um padrão e um texto.
2.  Construir o AFND para o padrão.
3.  Converter o AFND num AFD.
4.  Usar o AFD para encontrar todas as ocorrências do padrão no texto.
5.  Imprimir os resultados de cada etapa no terminal.

-----

## \#\# Exemplo Detalhado: Busca pelo padrão "aba"

O fluxo de trabalho para encontrar um padrão é um excelente exemplo do poder da biblioteca.

### 1\. Construir o AFND

Primeiro, construímos um AFND para o padrão `"aba"`. O resultado é um autômato simples com 4 estados (`q0` a `q3`), onde o caminho `q0 -> q1 -> q2 -> q3` reconhece "aba". O estado `q0` tem um laço para "esperar" pelo início do padrão.