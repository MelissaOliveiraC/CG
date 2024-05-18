from PIL import Image
import numpy as np
import os

def carregar_imagem(caminho):
    return Image.open(caminho)

def separar_canais(imagem):
    np_imagem = np.array(imagem)
    
    # três Arrays zerados de tam = img-orig
    canal_r = np.zeros_like(np_imagem)
    canal_g = np.zeros_like(np_imagem)
    canal_b = np.zeros_like(np_imagem)
    
    # copia os valores dos canais
    # R
    canal_r[:,:,0] = np_imagem[:,:,0]  
    # G
    canal_g[:,:,1] = np_imagem[:,:,1]  
    # B
    canal_b[:,:,2] = np_imagem[:,:,2]  
    

    # Converte os arrays de volta para imagens
    imagem_r = Image.fromarray(canal_r)
    imagem_g = Image.fromarray(canal_g)
    imagem_b = Image.fromarray(canal_b)
    
    # retorna as imagens R G B
    return imagem_r, imagem_g, imagem_b

def salvar_canais(canais, caminho_saida):
    nomes_canais = ['R', 'G', 'B']
    if not os.path.exists(caminho_saida):
        os.makedirs(caminho_saida)
    for canal, nome in zip(canais, nomes_canais):
        canal.save(os.path.join(caminho_saida, f"canal_{nome}.png"))

def main(caminho_imagem, caminho_saida):
    imagem = carregar_imagem(caminho_imagem)
    canais = separar_canais(imagem)
    salvar_canais(canais, caminho_saida)

if __name__ == "__main__":
    caminho_imagem = "images/img-original.jpg"
    caminho_saida = "images/cores-output"
    main(caminho_imagem, caminho_saida)