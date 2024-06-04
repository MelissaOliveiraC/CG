import os
import matplotlib.pyplot as plt
import cv2
import pytesseract
from matplotlib.widgets import Button
from functions import exibir_resultado, substituir_letras_por_numeros, gerar_possibilidades_mercosul
import re

def encontrar_placa(string, padrao):
    """Encontra a primeira placa no texto que corresponda ao padrão."""
    placas_encontradas = re.findall(padrao, string)
    return placas_encontradas[0] if placas_encontradas else None

def aplicar_ocr(possiveis_placas):
    """Aplica OCR para detectar a placa e realiza as devidas conversões."""
    for tupla in possiveis_placas:
        placa_recortada, placa_recortada_processada = tupla

        x, y, w, h = cv2.boundingRect(placa_recortada_processada)

        # Ajuste para placas do modelo antigo
        if h > 120:
            placa_recortada_processada = placa_recortada_processada[30:-10]

        # Executar OCR com Tesseract para detectar a placa em português
        resultado_tesseract_por = pytesseract.image_to_string(
            placa_recortada_processada, lang='por', config=r'-c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 --psm 6 --oem 3')
        placa_detectada_por = "".join(filter(str.isalnum, resultado_tesseract_por))

        placa_mercosul = encontrar_placa(placa_detectada_por, r'[A-Z]{3}[0-9][0-9A-Z][0-9]{2}')
        if placa_mercosul:
            return placa_mercosul, placa_recortada, placa_recortada_processada
        placa_antiga = encontrar_placa(placa_detectada_por, r'[A-Z]{3}\d{4}')
        if placa_antiga:
            return placa_antiga, placa_recortada, placa_recortada_processada

        # Executar OCR com Tesseract para detectar a placa em inglês
        resultado_tesseract_eng = pytesseract.image_to_string(
            placa_recortada_processada, lang='eng', config=r'-c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 --psm 6 --oem 3')
        placa_detectada_eng = "".join(filter(str.isalnum, resultado_tesseract_eng))

        placa_mercosul = encontrar_placa(placa_detectada_eng, r'[A-Z]{3}[0-9][0-9A-Z][0-9]{2}')
        if placa_mercosul:
            return placa_mercosul, placa_recortada, placa_recortada_processada
        placa_antiga = encontrar_placa(placa_detectada_eng, r'[A-Z]{3}\d{4}')
        if placa_antiga:
            return placa_antiga, placa_recortada, placa_recortada_processada

        # Pegar os últimos quatro caracteres da placa detectada e aplicar substituição de letras por números
        ultimos_4_caracteres = placa_detectada_por[-4:]

        # Possibilidades de placa normal
        possibilidades = substituir_letras_por_numeros(ultimos_4_caracteres)
        result = ""
        for i in range(len(possibilidades)):
            result += placa_detectada_por[:3] + possibilidades[i] + "\n"
        result += "\nMercosul:\n"

        # Possibilidades de placa Mercosul
        possibilidades_mercosul = gerar_possibilidades_mercosul(ultimos_4_caracteres)
        for i in range(len(possibilidades_mercosul)):
            result += placa_detectada_por[:3] + possibilidades_mercosul[i] + "\n"

        return result, placa_recortada, placa_recortada_processada