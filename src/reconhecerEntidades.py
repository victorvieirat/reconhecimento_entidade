import json
import sys
import re
from unidecode import unidecode
from abc import ABC, abstractmethod
import Levenshtein

def is_iterable(obj):
    try:
        iter(obj)
        return True
    except TypeError:
        return False
class TratarTexto():   
    def __init__(self) -> None:
        pass
    @classmethod
    def processar(cls,text):
        text = cls.minuscula(text)
        text = cls.remove_accents(text)
        text = cls.remover_caracteres_especiais(text)
        text = cls.rm_espaco_excessivo(text)
        text = cls.remover_palavras_curta(text)
        return text
    
    @staticmethod
    def remove_accents(text):
        text_without_accents = unidecode(text)
        return text_without_accents
    @staticmethod
    def remover_caracteres_especiais(texto):
        # Usa uma expressão regular para manter apenas letras, números, pontos e espaços
        texto_limpo = re.sub(r'[^a-zA-Z ]', ' ', texto)
        return texto_limpo
    @staticmethod
    def rm_espaco_excessivo(text):
        return re.sub(r'\s+', ' ', text).strip()
    @staticmethod
    def minuscula(text):
        return text.lower()
    @staticmethod
    def remover_palavras_curta(text):
        palavras = text.split()
        palavras_filtradas = [palavra for palavra in palavras if len(palavra) > 2]
        texto_filtrado = ' '.join(palavras_filtradas)
        return texto_filtrado
       
class LeitorJson():
    def __init__(self,caminho_arquivo)-> None:

        if isinstance(caminho_arquivo, str):
            self.json_data = self.ler_arquivo_json(caminho_arquivo)
        elif isinstance(caminho_arquivo, dict) or is_iterable(caminho_arquivo):
            self.json_data = caminho_arquivo
        self.data = self.json_data

    def __str__(self):
            return json.dumps(self.data,ensure_ascii=False)
    
    @staticmethod
    def ler_arquivo_json(caminho_arquivo):
        with open(caminho_arquivo, 'r', encoding='utf-8') as file:
            data = json.load(file)
            return data 
        
    @abstractmethod
    def valida_json(self):
        pass

    @abstractmethod
    def normalizar_texto(self,processa_texto):
        pass 

class Classes(LeitorJson):
    def __init__(self,caminho_arquivo)-> None:
        super().__init__(caminho_arquivo)
        self.unique = None
     
    def valida_json(self):
        
        for chave, valor in self.json_data.items():
             if not isinstance(valor, dict):
                    raise ValueError(f"A chave '{chave}' deve ser um dicionário.")
             for subchave, subvalor in valor.items():
                if not is_iterable(subvalor):
                    raise ValueError(f"A categoria '{subchave}' da chave '{chave}' deve ser uma lista como valor.")
        return True
    
    def normalizar_texto(self,processa_texto):
        novo_dicionario = {}
        for chave, valor in self.json_data.items():
            sub_dict = {}
            for subchave, subvalor in valor.items():
                sub_dict[processa_texto(subchave)] = [processa_texto(i) for i in subvalor]
            novo_dicionario[processa_texto(chave)] = sub_dict
        self.json_data = novo_dicionario
    
    def organizar(self):
        self.unique =self.json_data.keys()
        novo_dicionario = {}
        saida = []
        for chave, valor in self.json_data.items():
            novo_dicionario[chave] = [(key, key) for key in valor]
            novo_dicionario[chave].extend([(key, value) for key, array in valor.items() for value in array])
        saida = [(key, value[0],value[1]) for key, array in novo_dicionario.items() for value in array]
        saida = sorted(saida, key=lambda x: len(x[-1]), reverse=True)
        self.data = saida

class Textos(LeitorJson):
    def __init__(self,caminho_arquivo)-> None:
        super().__init__(caminho_arquivo)
    
    def valida_json(self):
        if not is_iterable(self.json_data):
                raise ValueError(f"O json de texto deve vir no tipo lista.")
        return True
    
    def normalizar_texto(self,processa_texto):
         self.data =  [processa_texto(i) for i in self.json_data]


class Classificador():
    def __init__(self,classes,categorias_tipos):
        self.classes = classes
        self.categorias_tipos = categorias_tipos

    @staticmethod
    def calcular_distancia_edicao(texto,classe):
        # (inserção, deleção, substituição)
        distance = Levenshtein.distance(texto,classe,weights=(1, 1, 1))
        distance = distance/len(classe)
        return distance

    
    def predict(self,textos):
        def dividir_em_grupos(texto, tamanho_grupo=3):
            palavras = texto.split()
            if len(palavras) < tamanho_grupo:
                return [texto]
            grupos = [palavras[i:i+tamanho_grupo] for i in range(0, len(palavras))]
            return grupos
        def processar_categoria(predicoes, indice, categoria_tipo, categoria_nome, categoria_variacao):
            coluna_distancia = f'{categoria_tipo}_distancia'
            coluna_classe = f'{categoria_tipo}_classe'
            if predicoes[coluna_distancia][indice] != 0:
                if categoria_variacao in textos[indice]:
                    predicoes[coluna_classe][indice] = categoria_nome
                    predicoes[coluna_distancia][indice] = 0
                tamanho_ngrama = len(categoria_variacao.split(" "))
                for grupo in dividir_em_grupos(textos[indice], tamanho_ngrama):
                    var_classe_fragmento = " ".join(grupo)
                    
                    distancia = self.calcular_distancia_edicao(var_classe_fragmento, categoria_variacao)
                    if distancia < predicoes[coluna_distancia][indice]:
                        predicoes[coluna_classe][indice] = categoria_nome
                        predicoes[coluna_distancia][indice] = distancia

        predicoes = {}
        for categoria_tipo in self.categorias_tipos:
            predicoes[f'{categoria_tipo}_distancia'] = [float('inf')]*len(textos)
            predicoes[f'{categoria_tipo}_classe'] = ['']*len(textos)

        for indice, _ in enumerate(textos):
            for categoria_tipo, categoria_nome, categoria_variacao in self.classes:
                processar_categoria(predicoes, indice, categoria_tipo, categoria_nome, categoria_variacao)

        return predicoes

def executar(categorias,textos):
    classes = Classes(categorias)
    classes.valida_json()
    classes.normalizar_texto(TratarTexto.processar)
    classes.organizar()
    
    textos = Textos(textos)
    textos.valida_json()
    textos.normalizar_texto(TratarTexto.processar)

    clsf = Classificador(classes.data,classes.unique)
    predictions = clsf.predict(textos.data)
    return predictions

def printar():
    print('mimde')

def main():
    if len(sys.argv) != 4:
        print("Uso: python reconhecerEntidades <caminho_json_dicionario> <caminho_json_textos> <caminho_saida>")
        sys.exit(1)

    caegorias_path = sys.argv[1]
    textos_path = sys.argv[2]
    output_path = sys.argv[3]   
    
    predictions= executar(caegorias_path,textos_path)
    predictions =  json.dumps(predictions, indent=2)
    with open(output_path, 'w') as arquivo_json:
        arquivo_json.write(predictions)


if __name__ == "__main__":
    main()

