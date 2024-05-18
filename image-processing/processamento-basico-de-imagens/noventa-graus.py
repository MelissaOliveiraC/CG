from PIL import Image

def rotaciona_img(caminho_imagem, caminho_saida):
    # Abre a img
    img = Image.open(caminho_imagem)

    # Gira a img em 90 graus
    img_rotacinada = img.rotate(-90)

    # Salva a img girada
    img_rotacinada.save(caminho_saida)

# Caminho da img de entrada e saída
caminho_imagem = "images/img-original.jpg"
caminho_saida = "images/noventa-graus-output/img-90-graus.jpg"

# Chama a função para girar a imgm e salvar
rotaciona_img(caminho_imagem, caminho_saida)