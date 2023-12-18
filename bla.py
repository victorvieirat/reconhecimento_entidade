def dividir_em_grupos(texto, tamanho_grupo=3):
    palavras = texto.split()
    grupos = [palavras[i:i+tamanho_grupo] for i in range(0, len(palavras))]
    return grupos

# Exemplo de uso
texto = "Este é um exemplo de texto que será dividido em grupos de três palavras."
grupos_palavras = dividir_em_grupos(texto)

for grupo in grupos_palavras:
    print(grupo)
