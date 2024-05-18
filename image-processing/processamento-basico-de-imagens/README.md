# 📌 Processamento Básico de Imagens - Implementação 

**Questão:** 
Crie um conjunto de scripts em Python que contemple as seguintes funcionalidades:

- Processamento de Cores:  separação de canais R, G e B
- Conversão de colorido RGB para tons de cinza
- Conversão de tons de cinza para preto e branco (limiarização/binarização manual)
- Filtros da Média
- Filtro da Mediana
- Girar a imagem 90 graus
- Inverter a imagem (horizontal/vertical)



### Tecnologias Usadas 🔧

- Python

### Referências 🔗

- [**wellingtondellamura**/computer-graphics-playground](https://github.com/wellingtondellamura/computer-graphics-playground)
- [Foto usada para as implementações de **Bagus Pangestu**](https://www.pexels.com/pt-br/foto/fotografia-de-close-up-da-arvore-de-cerejeira-1440476/)
## Documentação 📑

### **Processamento de cores: separação de canais R, G e B**

A função 'separar_canais' recebe uma imagem como entrada, **converte-a em um array NumPy e separa seus canais de cores (R, G, B) em três arrays diferentes**. Depois, converte esses arrays de volta em objetos Image e os retorna. A função 'salvar_canais' recebe uma lista de objetos Image representando os canais de **cores (R, G, B)** e um caminho de saída. Verifica se o diretório de saída existe e, se não existir, cria-o. Em seguida, salva cada canal como uma imagem separada com o prefixo "canal_" e o nome do canal (R, G, B) seguido da extensão ".png".

### **Conversão de colorido (RGB) para tons de cinza**

A função 'rgb_to_gray' aceita dois argumentos: caminho_imagem, que é o caminho da imagem RGB de entrada (imagem-original), e caminho_saida, que é onde a imagem em tons de cinza será salva. Dentro da função, a imagem é aberta usando o método 'open' da classe 'Image' e é **convertida para tons de cinza usando o método 'convert('L')'**. Em seguida, a imagem em tons de cinza é salva no caminho especificado.

### **Conversão de tons de cinza para preto e branco (limiarização/binarização manual)**

A função 'converter_para_preto_e_branco' recebe dois argumentos: imagem, que é a imagem a ser convertida para preto e branco, e limiar, que é o valor utilizado para determinar se um pixel será preto ou branco. Dentro da função, a **imagem é convertida para tons de cinza** usando o método 'convert("L")'. Em seguida, **itera-se sobre cada pixel da imagem e, se o valor de intensidade do pixel for menor que o limiar especificado, o pixel é definido como preto (0); caso contrário, é definido como branco (255)**. A função retorna a imagem convertida para preto e branco.

### **Filtro da média**

A função 'filtro_media' recebe dois argumentos: imagem, que é o caminho da imagem a ser filtrada, e **tamanho_janela, que é o tamanho da janela de vizinhança para aplicar o filtro de média**. A imagem é aberta usando 'Image.open(imagem)'. Uma nova imagem é criada com o mesmo tamanho da imagem original usando Image.new('RGB', (largura, altura)). Em seguida, o **filtro de média é aplicado a cada pixel da imagem original**, logo, para cada pixel, **obtém-se os pixels vizinhos** dentro da janela de tamanho especificado, **calcula-se a média dos valores de cada canal RGB** desses pixels vizinhos e define-se o valor do pixel na imagem filtrada como essa média. Finalmente, **a imagem filtrada** é salva no caminho de destino especificado.

```
for x in range(largura):
    for y in range(altura):
```

Aqui 'largura' e 'altura' representam as dimensões da imagem. Portanto, **x varia de 0 a largura - 1 e y varia de 0 a altura - 1**, percorrendo todos os pixels da imagem.

```
pixels_vizinhos = []
```

Para cada pixel na posição (x, y) da imagem, é criado uma **lista** 'pixels_vizinhos' que **armazena os valores de cor dos pixels vizinhos dentro de uma janela de tamanho (tamanho_janela) ao redor do pixel atual**.

```
for i in range(x - tamanho_janela, x + tamanho_janela + 1):
            for j in range(y - tamanho_janela, y + tamanho_janela + 1):
```

Os **for's aninhados iteram sobre os pixels vizinhos** dentro da janela de tamanho especificado, onde i e j representam as coordenadas x e y dos pixels vizinhos, respectivamente.

```
 if i >= 0 and i < largura and j >= 0 and j < altura:
                    pixels_vizinhos.append(img.getpixel((i, j)))

```

O if garante que **somente os pixels dentro dos limites** da imagem sejam considerados. Se i e j estiverem dentro dos limites da imagem, o valor de cor do pixel vizinho (i, j) é obtido usando o método 'getpixel()' e adicionado à lista 'pixels_vizinhos'.

```
media_r = sum([pixel[0] for pixel in pixels_vizinhos]) // len(pixels_vizinhos)
        media_g = sum([pixel[1] for pixel in pixels_vizinhos]) // len(pixels_vizinhos)
        media_b = sum([pixel[2] for pixel in pixels_vizinhos]) // len(pixels_vizinhos)
```

**Depois que a lista 'pixels_vizinhos' é preenchida** com os valores de cor dos pixels vizinhos, **é calculado a média dos valores de cor para cada canal (R, G, B)**.
A expressão '[pixel[0] for pixel in pixels_vizinhos]' cria uma lista contendo os valores de cor do canal vermelho para todos os pixels vizinhos. O mesmo é feito para os canais verde '([pixel[1] for pixel in pixels_vizinhos])' e azul '([pixel[2] for pixel in pixels_vizinhos])'."
A função sum() é usada para calcular a soma de todos os valores de cor em cada lista."
Em seguida, a **média** de cada canal é calculada dividindo a soma pelo número de pixels vizinhos '(len(pixels_vizinhos))'.

### **Filtro de mediana**

A função 'filtro_mediana' recebe uma imagem como entrada e **converte essa imagem colorida em tons de cinza** usando o método 'convert('L')', em seguida, converte a imagem em uma matriz NumPy para permitir o processamento eficiente dos pixels. 

* É criada uma **matriz vazia do mesmo tamanho que a matriz de pixels, onde os pixels filtrados serão armazenados**.
* As dimensões da imagem em tons de cinza são obtidas.
* São feitas iterações sobre cada pixel, **exceto as bordas**, onde o filtro de mediana não é aplicado. O **for itera sobre as linhas da imagem**, começando da segunda linha (índice 1) até a penúltima linha (altura - 1), **o mesmo ocorre para as colunas**. **Dessa forma, percorrerendo todos os pixels da imagem, menos as bordas**."

* Os valores dos pixels vizinhos ao redor do atual são obtidos, ordenados e após isso é calculada a mediana. Dentro do loop aninhado, uma **lista de 'vizinhos'** é criada que contém os valores dos pixels vizinhos ao redor do pixel atual (i, j). Estes valores são obtidos consultando os pixels nas posições relativas (i-1, j-1), (i-1, j), (i-1, j+1), (i, j-1), (i, j), (i, j+1), (i+1, j-1), (i+1, j), (i+1, j+1). Esses pixels vizinhos são os pixels dentro de uma vizinhança de **3x3** centrada no pixel atual."

* É atribuído o valor da **mediana** ao pixel filtrado na matriz de pixels filtrados.
* Por fim, é convertido a matriz de pixels filtrados **de volta em uma imagem** usando a classe Image.

### **Imagem 90 graus**

A função 'rotaciona_img' recebe dois argumentos: 'caminho_imagem', que é o caminho da imagem de entrada, e 'caminho_saida', que é o caminho onde a imagem girada será salva. Dentro da função: A **imagem é aberta e girada em 90 graus no sentido anti-horário usando o método rotate, o valor -90 é passado como argumento** para girar.

### **Inverter a imagem (horizontal/vertical)**

A Função **'inverte_vertical(imagem)'** recebe uma imagem como entrada e retorna a mesma imagem invertida verticalmente.
Já a função **'inverte_horizontal(imagem)'** recebe uma imagem como entrada e retorna a mesma imagem invertida horizontalmente.
## Imagens resultantes 📷

__Imagem original__

<a href="https://i.imgur.com/Rz5EJKL.jpg"><img src="https://i.imgur.com/Rz5EJKL.jpg" title="source: imgur.com" /></a>

__1. Processamento de Cores:  separação de canais R, G e B__


<a href="https://i.imgur.com/r25fiZh.png"><img src="https://i.imgur.com/r25fiZh.png" title="source: imgur.com" /></a>


<a href="https://i.imgur.com/fLre6CQ.png"><img src="https://i.imgur.com/fLre6CQ.png" title="source: imgur.com" /></a>


<a href="https://i.imgur.com/uZmDhnj.png"><img src="https://i.imgur.com/uZmDhnj.png" title="source: imgur.com" /></a>

__2. Conversão de colorido RGB para tons de cinza__

<a href="https://i.imgur.com/aqjE3hs.jpg"><img src="https://i.imgur.com/aqjE3hs.jpg" title="source: imgur.com" /></a>

__3. Conversão de tons de cinza para preto e branco (limiarização/binarização manual)__

<a href="https://i.imgur.com/rXpgWYB.jpg"><img src="https://i.imgur.com/rXpgWYB.jpg" title="source: imgur.com" /></a>

__4. Filtros da média__ 

<a href="https://i.imgur.com/bcpx1RY.jpg"><img src="https://i.imgur.com/bcpx1RY.jpg" title="source: imgur.com" /></a>


__5. Filtro da mediana__

<a href="https://i.imgur.com/SRvWW6e.jpg"><img src="https://i.imgur.com/SRvWW6e.jpg" title="source: imgur.com" /></a>

__6. Girar a imagem 90 graus__

<a href="https://i.imgur.com/PpdUNvI.jpg"><img src="https://i.imgur.com/PpdUNvI.jpg" title="source: imgur.com" /></a>

__7. Inverter a imagem (horizontal/vertical)__

<a href="https://i.imgur.com/CyLbVJx.jpg"><img src="https://i.imgur.com/CyLbVJx.jpg" title="source: imgur.com" /></a>

<a href="https://i.imgur.com/koJi5b0.jpg"><img src="https://i.imgur.com/koJi5b0.jpg" /></a>