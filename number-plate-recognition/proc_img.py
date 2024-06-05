import os
import matplotlib.pyplot as plt
import cv2
import pytesseract
from matplotlib.widgets import Button

# Converte a imagem para tons de cinza.
def converter_para_cinza(imagem):
    return cv2.cvtColor(imagem, cv2.COLOR_BGR2GRAY)

# Aplica filtros para remover ruídos.
def aplicar_filtros(imagem_cinza):
    imagem_filtrada = cv2.bilateralFilter(imagem_cinza, 9, 75, 75) # Suaviza a imagem enquanto preserva as bordas

    # Aplicação de filtro Gaussiano (NÃO-APLICADO INICIALMENTE EM ALGUMAS IMAGENS)
    imagem_filtrada = cv2.GaussianBlur(imagem_filtrada, (5, 5), 0) # Suaviza a imagem inteira mas borra as bordas
    return imagem_filtrada

# Aplica limiarização adaptativa para destacar os caracteres.
def limiarizacao_adaptativa(imagem_filtrada):
    return cv2.adaptiveThreshold(
        imagem_filtrada, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2
    )

def processar_imagem(imagem_placa):
    """Processar a imagem da placa para destacar os caracteres."""
    imagem_cinza = converter_para_cinza(imagem_placa)
    imagem_filtrada = aplicar_filtros(imagem_cinza)
    imagem_limiarizada = limiarizacao_adaptativa(imagem_filtrada)
    return imagem_limiarizada