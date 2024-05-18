from PIL import Image
import os

def filtro_media(imagem, tamanho_janela):
    
    img = Image.open(imagem)
    # Obtém as dimensões da imagem
    largura, altura = img.size

    # Cria a nova imagem
    img_filtrada = Image.new('RGB', (largura, altura))

    # Aplica o filtro de média
    for x in range(largura):
        for y in range(altura):
            # Obtém os pixels vizinhos dentro da janela
            pixels_vizinhos = []
            for i in range(x - tamanho_janela, x + tamanho_janela + 1):
                for j in range(y - tamanho_janela, y + tamanho_janela + 1):
                    # Verifica se o pixel está dentro dos limites da imagem
                     if i >= 0 and i < largura and j >= 0 and j < altura:
                        pixels_vizinhos.append(img.getpixel((i, j)))

            # Calcula a média dos valores dos pixels vizinhos
            media_r = sum([pixel[0] for pixel in pixels_vizinhos]) // len(pixels_vizinhos)
            media_g = sum([pixel[1] for pixel in pixels_vizinhos]) // len(pixels_vizinhos)
            media_b = sum([pixel[2] for pixel in pixels_vizinhos]) // len(pixels_vizinhos)

            # Define o filtro
            img_filtrada.putpixel((x, y), (media_r, media_g, media_b))

    # Salva a imagem
    caminho_destino = 'images/filtro-media-output/img-filtrada.jpg'
    img_filtrada.save(caminho_destino)


caminho_imagem = 'images/img-original.jpg'
tamanho_janela = 3
filtro_media(caminho_imagem, tamanho_janela)