import os
import matplotlib.pyplot as plt
import cv2
from matplotlib.widgets import Button

# Dicionário de mapeamento de letras para números
letras_numeros = {
    'I': '1', 'O': '0', 'Q': '0', 'Z': '2', 'S': ['5', '9'],
    'G': '6', 'B': '8', 'A': '4', 'E': '8', 'T': '7', 'Y': '7',
    'L': '1', 'U': '0', 'D': '0', 'R': '2', 'P': '0', 'F': '0',
    'J': '1', 'K': '1', 'V': '0', 'W': '0', 'X': '0', 'N': '0',
    'M': '0', 'H': '0', 'C': '0', 'Ç': '0', 'Á': '0', 'Â': '0',
    'Ã': '0', 'À': '0'
}

def exibir_resultado(imagem, imagem_processada, imagem_recortada, imagem_recortada_processada, placa_detectada):
    """Exibe os resultados da detecção de placas em uma janela gráfica."""
    fig, axs = plt.subplots(1, 4, figsize=(16, 4)) # 1 linha, 4 colunas

    # Imagem Original
    axs[0].imshow(cv2.cvtColor(imagem, cv2.COLOR_BGR2RGB))
    axs[0].set_title("Original - Sem efeitos ou recorte", fontsize=10, color='red')  
    axs[0].axis('off')

    # Imagem Processada
    axs[1].imshow(cv2.cvtColor(imagem_processada, cv2.COLOR_BGR2RGB))
    axs[1].set_title("Imagem Pós-Filtros (Processada)", fontsize=10, color='red')  
    axs[1].axis('off')

    # Imagem Recortada
    axs[2].imshow(cv2.cvtColor(imagem_recortada, cv2.COLOR_BGR2RGB))
    axs[2].set_title("Imagem Recortada - (Recorte Sem-filtros)", fontsize=10, color='red')  
    axs[2].axis('off')

    # Recorte Processado
    axs[3].imshow(cv2.cvtColor(imagem_recortada_processada, cv2.COLOR_BGR2RGB))
    axs[3].set_title("Imagem Recortada - (Recorte Com-Filtros)", fontsize=10, color='green')  
    axs[3].axis('off')

    # Informações da Placa Detectada
    info_text = f"Placa Detectada: {placa_detectada}"
    fig.text(0.5, 0.95, info_text, fontsize=8, ha='center', va='top', color='blue')  

    plt.tight_layout()
    plt.show()

def substituir_letras_por_numeros(ultimos_caracteres: str):
    """Substitui letras por números de acordo com o mapeamento definido."""
    todas_possibilidades = ['']

    for caractere in reversed(ultimos_caracteres):
        possibilidades = []

        try:
            for letra_numero in letras_numeros[caractere]:
                for possibilidade in todas_possibilidades:
                    possibilidades.append(letra_numero + possibilidade)
        except KeyError:
            for possibilidade in todas_possibilidades:
                possibilidades.append(caractere + possibilidade)

        todas_possibilidades = possibilidades

    return todas_possibilidades

def gerar_possibilidades_mercosul(value: str):
    """Gera todas as possibilidades de placas com letras e números."""
    def combinar_elementos(lista, prefixo=''):
        if not lista:
            return [prefixo]

        resultado = []
        elemento_atual = lista[0]
        for item in elemento_atual:
            novo_prefixo = prefixo + item
            resultado.extend(combinar_elementos(lista[1:], novo_prefixo))

        return resultado

    segurar_letra = []
    index = 0
    for caractere in value:
        if caractere in letras_numeros:
            segurar_letra.append((
                caractere, index
            ))
        index += 1

    todas_possibilidades = []
    for letra_travada, index_travado in segurar_letra:
        index = 0
        possibilidades = []
        for caractere in value:
            if(caractere != letra_travada or index != index_travado):
                if(caractere in letras_numeros):
                    valor_convertido = letras_numeros[caractere]
                    if isinstance(valor_convertido, list):
                        possibilidade_multipla = []
                        for letra_numero in valor_convertido:
                            possibilidade_multipla.append(
                                letra_numero)
                        possibilidades.append(possibilidade_multipla)
                    else:
                        possibilidades.append(valor_convertido)
                else:
                    possibilidades.append(caractere)
            else:
                possibilidades.append(caractere)

            index += 1
        todas_possibilidades.extend(combinar_elementos(possibilidades))
    return todas_possibilidades