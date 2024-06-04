import os
import cv2
from proc_img import processar_imagem
from proc_cont import processar_contornos
from ocr import aplicar_ocr
from functions import exibir_resultado
import pytesseract

# Caminho do Tesseract
pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract.exe'

# Carrega a imagem do caminho especificado.
def carregar_imagem(caminho_imagem):
    return cv2.imread(caminho_imagem)

# Processa a imagem para detectar placas.
def processar_placa(imagem_original):
    imagem_processada = processar_imagem(imagem_original)
    placas_potenciais = processar_contornos(imagem_original, imagem_processada)
    return placas_potenciais, imagem_processada

# Exibe os resultados da detecção de placas.
def exibir_resultados(imagem_original, imagem_processada, placas_potenciais):
    if placas_potenciais:
        placa_detectada, placa_recortada, placa_recortada_processada = aplicar_ocr(placas_potenciais)
        exibir_resultado(imagem_original, imagem_processada, placa_recortada, placa_recortada_processada, placa_detectada)

# Combina as etapas de carregamento, processamento e exibição dos resultados.
def detectar_placa(caminho_imagem):
    """Detectar a placa a partir de uma imagem"""
    imagem_original = carregar_imagem(caminho_imagem)
    placas_potenciais, imagem_processada = processar_placa(imagem_original)
    exibir_resultados(imagem_original, imagem_processada, placas_potenciais)

# Itera sobre todas as imagens no diretório e aplica a detecção de placas.
def processar_imagens(diretorio_imagens):
    """Processar todas as imagens em um diretório"""
    arquivos_imagens = [f for f in os.listdir(diretorio_imagens) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
    for arquivo_imagem in arquivos_imagens:
        caminho_imagem = os.path.join(diretorio_imagens, arquivo_imagem)
        detectar_placa(caminho_imagem)

if __name__ == "__main__":
    diretorio_imagens = "images"
    processar_imagens(diretorio_imagens)