from PIL import Image
import os

def inverte_vertical(imagem):
    imagem_invertida = imagem.transpose(Image.FLIP_TOP_BOTTOM)
    return imagem_invertida

def inverte_horizontal(imagem):
    imagem_invertida = imagem.transpose(Image.FLIP_LEFT_RIGHT)
    return imagem_invertida

def salvar_imagem(imagem, caminho):
    imagem.save(caminho)

def main():
    # Carrega a imagem original
    caminho_imagem_original = "images/img-original.jpg"
    imagem_original = Image.open(caminho_imagem_original)

    # Inverte verticalmente
    img_invertida_v = inverte_vertical(imagem_original)
    salvar_imagem(img_invertida_v, "images/inverter-img-output/invertida-v.jpg")

    # Inverte horizontalmente
    img_invertida_h = inverte_horizontal(imagem_original)
    salvar_imagem(img_invertida_h, "images/inverter-img-output/invertida-h.jpg")

if __name__ == "__main__":
    main()