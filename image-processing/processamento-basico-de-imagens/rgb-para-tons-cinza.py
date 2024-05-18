from PIL import Image

def rgb_to_gray(caminho_imagem, caminho_saida):
    # Abre a imagem RGB
    img = Image.open(caminho_imagem)

    # Converte a imagem original para tons de cinza
    gray_img = img.convert('L')

    # Salvar a img tons de cinza
    gray_img.save(caminho_saida)

# Caminho da imagem original input
caminho_imagem = "images/img-original.jpg"

# Caminho de output para a img em tons de cinza
caminho_saida = "images/rgb-para-tons-cinza-output/imagem-tons-cinza.jpg"

rgb_to_gray(caminho_imagem, caminho_saida)