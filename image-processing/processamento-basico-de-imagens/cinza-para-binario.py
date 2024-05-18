from PIL import Image

def converter_para_preto_e_branco(imagem, limiar):
    imagem = imagem.convert("L")  # Converte para tons de cinza
    pixels = imagem.load()

    largura, altura = imagem.size
    for i in range(largura):
        for j in range(altura):
            if pixels[i, j] < limiar:
                pixels[i, j] = 0  # Define como preto
            else:
                pixels[i, j] = 255  # Define como branco

    return imagem

# Caminho da imagem de entrada
caminho_imagem = "images/img-original.jpg"

# Limiar p/ binarização (0-255) ==> [128] 
lim  = 128

# abre a imagem
imagem = Image.open(caminho_imagem)

# Converte para P/B 
imagem_pb = converter_para_preto_e_branco(imagem, lim)

# salva a imagem
caminho_saida = "images/cinza-para-binario-output/imagem-bin.jpg"
imagem_pb.save(caminho_saida)