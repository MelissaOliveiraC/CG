import os
import matplotlib.pyplot as plt
import cv2
import pytesseract
from matplotlib.widgets import Button
from functions import exibir_resultado
from ocr import aplicar_ocr

def processar_contornos(imagem_original, imagem_processada):
    contornos, _ = cv2.findContours(imagem_processada, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
    placas_detectadas = []

    for contorno in contornos:
        # Aproximar o contorno a um polígono
        comprimento = cv2.arcLength(contorno, True)
        aproximacao = cv2.approxPolyDP(contorno, 0.02 * comprimento, True)
        area_contorno = cv2.contourArea(contorno)
        x, y, largura, altura = cv2.boundingRect(contorno)

        # Ignorar contornos onde a altura é maior que a largura
        if altura > largura:
            continue

        # Ignorar contornos onde a altura é menor que 20% da largura
        if altura < (largura * 0.2):
            continue

        # Ignorar contornos com área fora do intervalo desejado
        if area_contorno < 10000 or area_contorno > 70000:
            continue

        # Considerar como possível placa se o polígono tiver entre 4 e 10 lados
        if 4 <= len(aproximacao) < 10:
            cv2.drawContours(imagem_original, [aproximacao], -1, (0, 255, 0), 2)

            # Recortar a área da possível placa
            x, y, largura, altura = cv2.boundingRect(contorno)
            recorte_placa = imagem_original[y:y + altura, x:x + largura]

            # Converter o recorte para tons de cinza
            recorte_cinza = cv2.cvtColor(recorte_placa, cv2.COLOR_BGR2GRAY)

            # Aplicar limiarização para destacar os caracteres
            _, limiarizada = cv2.threshold(recorte_cinza, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

            # Operação de fechamento para preencher regiões de contornos
            kernel_fechamento = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
            processada = cv2.morphologyEx(limiarizada, cv2.MORPH_CLOSE, kernel_fechamento)

            # Operação de abertura para remover ruídos
            kernel_abertura = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
            processada = cv2.morphologyEx(processada, cv2.MORPH_OPEN, kernel_abertura)

            # Dilatação para aumentar a espessura dos caracteres
            processada = cv2.dilate(processada, kernel_abertura, iterations=1)

            # Erosão para reduzir a espessura dos caracteres
            processada = cv2.erode(processada, kernel_abertura, iterations=1)

            placas_detectadas.append((recorte_placa, processada))

    return placas_detectadas