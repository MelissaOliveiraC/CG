from PIL import Image
import numpy as np

def filtro_mediana(image):
    # Converte a img para escala de cinza
    img_cinza = image.convert('L')

    # Converte a img em uma matriz
    pixels = np.array(img_cinza)

    # Cria uma matriz vazia para armazenar os pixels filtrados
    pxl_filtrados = np.zeros_like(pixels)

    # Obtém as dimensões
    altura, largura = pixels.shape

    # Aplica o filtro de mediana a cada pixel da img
    for i in range(1, altura - 1):
        for j in range(1, largura - 1):
            # Obtém os valores dos pixels vizinhos
            vizinhos = [
                pixels[i-1, j-1], pixels[i-1, j], pixels[i-1, j+1],
                pixels[i, j-1], pixels[i, j], pixels[i, j+1],
                pixels[i+1, j-1], pixels[i+1, j], pixels[i+1, j+1]
            ]

            # Ordena os valores dos pixels vizinhos e obtém a mediana
            valores_mediana = np.median(vizinhos)

            # Atribui o valor da mediana ao pixel filtrado
            pxl_filtrados[i, j] = valores_mediana

    # Cria uma nova img com base nos pixels filtrados
    img_filtrada = Image.fromarray(pxl_filtrados)

    return img_filtrada

# Carrega a img e aplica filtro de mediana
caminho_imagem = 'images/img-original.jpg'
imagem = Image.open(caminho_imagem)
img_filtrada = filtro_mediana(imagem)

# Salva a img
caminha_saida = 'images/filtro-mediana-output/imagem-filtrada-mediana.jpg'
img_filtrada.save(caminha_saida)