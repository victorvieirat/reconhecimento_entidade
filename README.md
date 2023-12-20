# Reconhecimento de Entidades

Este é um programa Python destinado ao reconhecimento de entidades em textos, usando um dicionário de categorias. O programa aceita dois arquivos JSON como entrada: um contendo o dicionário de categorias e outro contendo os textos a serem processados. O resultado do reconhecimento de entidades é então salvo em um novo arquivo JSON, contendo sua classe e a distância, que varia de 0 quando a classe foi encontrada diretamente até 1 quando não há nenhuma palavra nem próxima de parecer com a classe.

## Pré-requisitos
- Python 3.x


## Instalação de Dependências
Certifique-se de ter todas as dependências instaladas. Execute o seguinte comando para instalar as dependências necessárias:

```bash
pip install -r requirements.txt
```

## Execução do Programa
O programa é executado a partir da linha de comando com a seguinte sintaxe:

```bash
python reconhecerEntidades.py <caminho_json_dicionario> <caminho_json_textos> <caminho_saida>
```

- `<caminho_json_dicionario>`: O caminho para o arquivo JSON que contém o dicionário de categorias.
- `<caminho_json_textos>`: O caminho para o arquivo JSON que contém os textos a serem processados.
- `<caminho_saida>`: O caminho para o arquivo de saída onde as entidades reconhecidas serão salvas.

### Estrutura do dicionário

O arquivo JSON de dicionário utilizado como entrada para o programa deve seguir uma estrutura específica. Cada chave principal do dicionário deve referir-se obrigatoriamente a outros dicionários, e as chaves desses dicionários secundários devem ter valores obrigatoriamente em lista, podendo essas listas serem vazias.

Aqui está um exemplo:

```json
{
    "Fruta": {
        "Abobóra": [
            "Jerimun"
        ],
        "Tangerina": [
            "mexirica",
            "bergamota"
        ]
    },
    "Cor": {
        "Roxo": [
            "Lilás"
        ],
        "Azul": [
            "Ciano"
        ]
    }
}
```

Neste exemplo, temos duas categorias principais: "Fruta" e "Cor". Cada uma dessas categorias contém subcategorias (por exemplo, "Abobora" e "Tangerina" em "Fruta"). Cada subcategoria possui uma lista de valores sinônimos.

### Estrutura dos textos

O arquivo JSON de textos utilizado como entrada para o programa deve ser uma lista de strings, onde cada string representa um texto a ser processado pelo programa de reconhecimento de entidades.

Aqui está um exemplo:

```json
["Hoje, no mercado, comprei uma fruta roxa que não costumo comer com frequência: a abóbora azul.",
"As flores do jardim começaram a desabrochar, exibindo uma tonalidade incrível de lilás de uma tangerina.",
"No café da manhã, saboreei uma deliciosa tangerina.",
"Ao pintar a parede da sala, escolhi uma cor vibrante e moderna: o ciano"]
]
```

Neste exemplo, temos uma lista contendo quatro textos. Cada texto é uma string que representa uma observação.


### Saída
O programa gera um arquivo JSON contendo com o a subcategoria mais próximo para cada categoria principal juntamente com sua distância calculada.

Exemplo de saída:
```json
{
  "fruta_distancia": [0,0,0,0.5555555555555556],
  "fruta_classe": ["abobora","tangerina","tangerina","tangerina"],
  "cor_distancia": [0,0,0.6,0],
  "cor_classe": ["azul","roxo","azul","azul"]
}
```

## Classes



### `TratarTexto`
Serve de pré-processamento de textos, incluindo a remoção de acentos, caracteres especiais, espaços excessivos, conversão para minúsculas e remoção de palavras curtas (tamanho 2).


### `LeitorJson`
Classe abstrata serve como uma base para classes que leem arquivos JSON.

### `Classes`
Herda de `LeitorJson` e é especializada para lidar com o dicionário de categorias. Realiza validação, normalização e organização das categorias.

### `Textos`
Herda de `LeitorJson` e é especializada para lidar com o arquivo JSON de textos. Realiza validação e normalização dos textos.

### `Classificador`
Realiza a classificação de textos com base em um conjunto de classes previamente definidas. Utiliza a distância de edição normalizada pelo tamanho de classe para determinar a similaridade entre o texto e as classes,criando uma métrica de distância que vai de 0 até 1
