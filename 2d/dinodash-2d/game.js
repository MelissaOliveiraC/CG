const images = {
    bg: './img/bg.png',        // Imagem do céu laranja
    cloud: './img/clouds.png', // Imagem das nuvens
    dino: './img/dino.png',    // Imagem do personagem dinossauro
    cactus: './img/cactos.png' // Imagem do obstáculo cacto
};

const screenSize = {
    x: 1127, // Largura da tela
    y: 606   // Altura da tela
};

// Espaço constante entre os obstáculos
const obstacleGap = 200;

// Intervalo de geração de obstáculos (milissegundos)
const obstacleGenerationInterval = 800;

// Variáveis para controle de tempo
var lastFrameTime = 0;
var lastObstacleGenerationTime = 0;

// Seleciona o elemento canvas e define suas dimensões
var canvas = document.querySelector('canvas');
canvas.width = screenSize.x;
canvas.height = screenSize.y;
resizeScreen(); // Função para ajustar o tamanho do canvas conforme a tela
var ctx = canvas.getContext('2d'); // Contexto 2D do canvas

// Configurações de volume dos sons
const ambientSound = document.getElementById('ambientSound');
ambientSound.volume = 0.9; // Volume do som ambiente
const failSound = document.getElementById('failSound');
failSound.volume = 0.9; // Volume do som de falha

// Classe Background para desenhar o fundo do jogo
class Background {
    constructor() {
        this.img = new Image(); // Cria uma nova imagem
        this.img.src = images.bg; // Define a imagem de fundo
        this.img.onload = () => { // Quando a imagem carregar, desenha-a
            this.draw(0);
        };
    }
    draw(delta) { // Método para desenhar o fundo
        ctx.drawImage(this.img, 0, 0); // Desenha a imagem nas coordenadas (0,0)
    }
}

// Classe Clouds para desenhar as nuvens em movimento
class Clouds {
    constructor() {
        this.totalSeconds = 0; // Contador de segundos
        this.speed = 50; // Velocidade das nuvens
        this.img = new Image(); // Cria uma nova imagem para as nuvens
        this.slideImages = 1; // Número de imagens de nuvem necessárias para preencher o canvas
        this.img.src = images.cloud; // Define a imagem das nuvens
        this.img.onload = () => { // Quando a imagem carregar, desenha as nuvens
            this.slideImages = Math.ceil(canvas.width / this.img.width);
            this.draw(0);
        };
    }
    draw(delta) { // Método para desenhar as nuvens
        this.totalSeconds += delta; // Atualiza o tempo total
        var new_pos = this.totalSeconds * this.speed % this.img.width;
        ctx.save();
        ctx.translate(-new_pos, 0); // Move o contexto para simular o movimento das nuvens
        for (var i = 0; i < this.slideImages; i++) {
            ctx.drawImage(this.img, i * this.img.width, 0); // Desenha as nuvens repetidamente
        }
        ctx.restore();
    }
}

// Classe Ground para desenhar o chão do jogo
class Ground {
    constructor() {
        this.y = canvas.height - 50; // Posição vertical do chão
        this.height = 50; // Altura do chão
    }
    draw() {
        ctx.fillStyle = '#F4E3B1'; // Cor do chão
        ctx.fillRect(0, this.y, canvas.width, this.height); // Desenha o chão
    }
}

// Classe Dino para representar o personagem principal
class Dino {
    constructor() {
        this.x = 50; // Posição horizontal inicial do dinossauro
        this.y = canvas.height - 90; // Posição vertical inicial do dinossauro
        this.width = 100; // Largura do dinossauro
        this.height = 100; // Altura do dinossauro
        this.dy = 0; // Velocidade vertical inicial (dy)
        this.jumpStrength = 19; // Força do pulo
        this.gravity = 1.0; // Gravidade aplicada ao dinossauro
        this.grounded = false; // Flag para indicar se está no chão
        this.img = new Image(); // Imagem do dinossauro
        this.img.src = images.dino; // Define a imagem do dinossauro
        this.collisionMargin = 15; // Margem de colisão única para o dinossauro
    }
    draw() {
        ctx.drawImage(this.img, this.x, this.y, this.width, this.height); // Desenha o dinossauro na tela
    }
    update() {
        if (this.grounded && this.dy === 0 && isJumping) {
            this.dy = -this.jumpStrength; // Aplica a força do pulo se estiver no chão e estiver pulando
            this.grounded = false;
        }

        this.dy += this.gravity; // Aplica a gravidade para o dinossauro cair
        this.y += this.dy; // Atualiza a posição vertical do dinossauro

        if (this.y + this.height > canvas.height - ground.height) {
            this.y = canvas.height - ground.height - this.height; // Impede que o dinossauro passe do chão
            this.dy = 0; // Reseta a velocidade vertical
            this.grounded = true; // Indica que está no chão
        }
    }
}

// Classe Obstacle para representar os obstáculos (cactos)
class Obstacle {
    constructor(x, y, width, height) {
        this.x = x; // Posição horizontal do obstáculo
        this.y = y; // Posição vertical do obstáculo
        this.width = width; // Largura do obstáculo
        this.height = height; // Altura do obstáculo
        this.img = new Image(); // Imagem do obstáculo
        this.img.src = images.cactus; // Define a imagem do cacto
        this.collisionMargin = 20; // Margem de colisão única para o obstáculo
    }
    draw() {
        ctx.drawImage(this.img, this.x, this.y, this.width, this.height); // Desenha o obstáculo na tela
    }
    update() {
        this.x -= gameSpeed; // Move o obstáculo para a esquerda conforme a velocidade do jogo
    }
}

let dino = new Dino(); // Cria um novo dinossauro
let obstacles = []; // Array para armazenar os obstáculos
let gameSpeed = 20; // Velocidade inicial do jogo
let score = 0; // Pontuação inicial
let isJumping = false; // Flag para controlar se o dinossauro está pulando

// Função para atualizar os obstáculos em cena
function updateObstacles() {
    obstacles.forEach(obstacle => {
        obstacle.update(); // Atualiza a posição dos obstáculos
    });

    // Verifica se é hora de gerar um novo obstáculo
    let currentTime = Date.now();
    if (currentTime - lastObstacleGenerationTime > obstacleGenerationInterval) {
        let obstacleWidth = 140; // Largura padrão do cacto
        let obstacleHeight = 140; // Altura padrão do cacto
        let obstacleX = canvas.width; // Posição horizontal inicial do obstáculo (fora da tela)
        let obstacleY = canvas.height - ground.height - obstacleHeight; // Posição vertical do obstáculo
        let obstacle = new Obstacle(obstacleX, obstacleY, obstacleWidth, obstacleHeight); // Cria um novo obstáculo
        obstacles.push(obstacle); // Adiciona o obstáculo ao array
        lastObstacleGenerationTime = currentTime; // Atualiza o tempo do último obstáculo gerado
    }

    // Remove os obstáculos que já passaram da tela
    if (obstacles.length > 0 && obstacles[0].x + obstacles[0].width < 0) {
        obstacles.shift(); // Remove o obstáculo do início do array
        score++; // Incrementa a pontuação
    }
}

// Função para detectar colisões entre o dinossauro e os obstáculos
function detectCollision() {
    obstacles.forEach(obstacle => {
        // Verifica a colisão considerando as margens de colisão
        if (
            dino.x + dino.collisionMargin < obstacle.x + obstacle.width - obstacle.collisionMargin &&
            dino.x + dino.width - dino.collisionMargin > obstacle.x + obstacle.collisionMargin &&
            dino.y + dino.collisionMargin < obstacle.y + obstacle.height - obstacle.collisionMargin &&
            dino.y + dino.height - dino.collisionMargin > obstacle.y + obstacle.collisionMargin
        ) {
            // Para o som ambiente e toca o som de falha
            ambientSound.pause();
            failSound.play();

            // Define o jogo como encerrado
            isGameOver = true;

            // Para o loop de atualização do jogo
            cancelAnimationFrame(updateAnimationFrameId);

            // Exibe a pontuação no console ou realiza outras ações necessárias
            console.log('Game Over! Score: ' + score);

            // Exibe a tela de Game Over
            document.getElementById('game-over-container').style.display = 'flex';
        }
    });
}

// Flag para indicar se o jogo está encerrado
let isGameOver = false;

// Event listeners para controle do pulo do dinossauro
document.addEventListener('keydown', (e) => {
    if (e.code === 'Space') {
        isJumping = true; // Define isJumping como verdadeiro quando a tecla Espaço é pressionada
    }
});

document.addEventListener('keyup', (e) => {
    if (e.code === 'Space') {
        isJumping = false; // Define isJumping como falso quando a tecla Espaço é solta
    }
});

// Event listener para o botão "Play"
document.getElementById('play-button').addEventListener('click', () => {
    // Esconde o menu principal e exibe o canvas do jogo
    document.getElementById('main-menu').style.display = 'none';
    canvas.style.display = 'block';

    // Inicia o loop de atualização do jogo
    startUpdate();
});

// Event listener para o botão "Retry"
document.getElementById('retry-button').addEventListener('click', () => {
    // Esconde o contêiner de Game Over
    document.getElementById('game-over-container').style.display = 'none';

    // Redefine as variáveis do jogo
    isGameOver = false;
    score = 0;
    obstacles = [];
    dino = new Dino();

    // Reinicia o som ambiente
    ambientSound.currentTime = 0;
    ambientSound.play();

    // Inicia o loop de atualização do jogo
    startUpdate();
});

// Função para atualizar o jogo
function update() {
    updateAnimationFrameId = requestAnimationFrame(update); // Chama novamente a função update para criar um loop
    var now = Date.now(); // Obtém o tempo atual
    var deltaSeconds = (now - lastFrameTime) / 1000; // Calcula a diferença de tempo em segundos
    lastFrameTime = now; // Atualiza o tempo do último frame

    ctx.clearRect(0, 0, canvas.width, canvas.height); // Limpa o canvas

    bg.draw(deltaSeconds); // Desenha o fundo do jogo
    cloud.draw(deltaSeconds); // Desenha as nuvens
    ground.draw(); // Desenha o chão

    dino.update(); // Atualiza o dinossauro
    dino.draw(); // Desenha o dinossauro

    updateObstacles(); // Atualiza os obstáculos
    obstacles.forEach(obstacle => obstacle.draw()); // Desenha os obstáculos

    if (!isGameOver) {
        detectCollision(); // Verifica colisões se o jogo não estiver encerrado
    }

    // Configurações da pontuação
    ctx.fillStyle = 'white';
    ctx.font = '30px Arial';
    ctx.strokeStyle = 'black';
    ctx.lineWidth = 5;
    ctx.strokeText('Score: ' + score, 10, 30); // Desenha a pontuação com borda
    ctx.fillText('Score: ' + score, 10, 30); // Desenha a pontuação
}

// Instâncias das classes de fundo, nuvens e chão
var bg = new Background();
var cloud = new Clouds();
var ground = new Ground();

// Função para redimensionar o canvas conforme o tamanho da tela
function resizeScreen() {
    var aspectRatio = screenSize.x / screenSize.y; // Calcula a proporção de aspecto do canvas
    var windowRatio = window.innerWidth / window.innerHeight; // Calcula a proporção de aspecto da janela

    if (aspectRatio < windowRatio) {
        canvas.style.width = "auto"; // Ajusta a largura do canvas automaticamente
        canvas.style.height = window.innerHeight + 'px'; // Define a altura do canvas
    } else {
        canvas.style.height = "auto"; // Ajusta a altura do canvas automaticamente
        canvas.style.width = window.innerWidth + 'px'; // Define a largura do canvas
    }
}

// Função para iniciar o loop de atualização do jogo
function startUpdate() {
    lastFrameTime = Date.now(); // Define o tempo do último frame como o tempo atual
    updateAnimationFrameId = requestAnimationFrame(update); // Chama a função update para iniciar o loop
}

// Event listener para redimensionar o canvas quando a janela for redimensionada
window.addEventListener("resize", resizeScreen);