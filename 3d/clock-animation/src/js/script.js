import * as THREE from '../../node_modules/three/build/three.module.js';
import { gsap } from '../../node_modules/gsap/index.js'; // para animações

const canvas = document.querySelector('canvas.webgl');

const scene = new THREE.Scene();


const sizes = {
  width: window.innerWidth,
  height: window.innerHeight, 
};

const textureLoader = new THREE.TextureLoader(); // Cria um carregador de texturas

// Carrega texturas
const torusTexture = textureLoader.load('/src/textures/torusTexture.jpg'); 
const cubeTexture = textureLoader.load('/src/textures/cubeTexture.jpg'); 
const pyramidTexture = textureLoader.load('/src/textures/pyramidTexture.jpg'); 
const backgroundTexture = textureLoader.load('/src/textures/background.jpg'); 


const objectsDistance = 4; // Distância entre os objetos

// Adionando materiais com texturas
const torusMaterial = new THREE.MeshToonMaterial({ map: torusTexture }); // Material da rosquinha usando MeshToonMaterial
const cubeMaterial = new THREE.MeshStandardMaterial({ map: cubeTexture, metalness: 0.5, roughness: 0.5 }); // 
const pyramidMaterial = new THREE.MeshStandardMaterial({ map: pyramidTexture, metalness: 0.5, roughness: 0.5 }); 


const mesh1 = new THREE.Mesh(
  new THREE.TorusGeometry(0.5, 0.2, 16, 60), // Cria a geometria da rosquinha
  torusMaterial // Aplica o material
);
const mesh2 = new THREE.Mesh(new THREE.ConeGeometry(0.5, 1, 32), torusMaterial); // Cria um cone e aplica o material
const mesh3 = new THREE.Mesh(
  new THREE.TorusKnotGeometry(0.4, 0.15, 100, 16), // Cria a geometria do torus
  torusMaterial // Aplica o material
);


const backgroundGeometry = new THREE.BoxGeometry(50, 50, 50); // Cria a geometria do fundo
const backgroundMaterials = [
  new THREE.MeshBasicMaterial({ map: backgroundTexture, side: THREE.BackSide }), // frente
  new THREE.MeshBasicMaterial({ map: backgroundTexture, side: THREE.BackSide }), // direita
  new THREE.MeshBasicMaterial({ map: backgroundTexture, side: THREE.BackSide }), // esquerda
  new THREE.MeshBasicMaterial({ map: backgroundTexture, side: THREE.BackSide }), // cima
  new THREE.MeshBasicMaterial({ map: backgroundTexture, side: THREE.BackSide }), // baixo
  new THREE.MeshBasicMaterial({ map: backgroundTexture, side: THREE.BackSide }), // atrás
];
const backgroundMesh = new THREE.Mesh(backgroundGeometry, backgroundMaterials); // Cria o fundo
scene.add(backgroundMesh); // Adiciona à cena

const cubeGeometry = new THREE.BoxGeometry(1, 1, 1); 
const cube = new THREE.Mesh(cubeGeometry, cubeMaterial); 
const pyramidGeometry = new THREE.CylinderGeometry(0, 0.5, 1, 4);
const pyramid = new THREE.Mesh(pyramidGeometry, pyramidMaterial); 

// Centralização dos objetos
mesh1.position.set(0, -objectsDistance * 0, 0); 
mesh2.position.set(0, -objectsDistance * 1, 0); 
mesh3.position.set(0, -objectsDistance * 2, 0); 
cube.position.set(2.0, 0, 0); 
pyramid.position.set(-2.0, 0, 0); 

scene.add(mesh1, mesh2, mesh3, cube, pyramid); // Adiciona todos à cena

const sectionMeshes = [mesh1, mesh2, mesh3, cube, pyramid]; // Array para facilitar a manipulação

// luz
const directionalLight = new THREE.DirectionalLight('#ffffff', 3); 
directionalLight.position.set(1, 1, 0); // Define a posição da luz direcional
scene.add(directionalLight); 

// luz ambiente
const ambientLight = new THREE.AmbientLight('#ffffff', 0.5); 
scene.add(ambientLight); 

// Camera
const cameraGroup = new THREE.Group(); // Cria um grupo para a câmera
scene.add(cameraGroup); 

const camera = new THREE.PerspectiveCamera(35, sizes.width / sizes.height, 0.1, 100); // Cria câmera com perspectiva
camera.position.z = 6; 
cameraGroup.add(camera); 


const renderer = new THREE.WebGLRenderer({
  canvas: canvas, 
  alpha: true, 
});
renderer.setSize(sizes.width, sizes.height); 
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2)); 

window.addEventListener('resize', () => { // Redimensionar a janela
  sizes.width = window.innerWidth;
  sizes.height = window.innerHeight; 
  camera.aspect = sizes.width / sizes.height;
  camera.updateProjectionMatrix(); 
  renderer.setSize(sizes.width, sizes.height); 
  renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2)); 
});

let scrollY = window.scrollY; 
let currentSection = 0; 

window.addEventListener('scroll', () => { 
  scrollY = window.scrollY;
  const newSection = Math.round(scrollY / sizes.height); 

  if (newSection !== currentSection) { 
    currentSection = newSection; 

    gsap.to(sectionMeshes[currentSection].rotation, { 
      duration: 1.5, // Duração da animação
      ease: 'power2.inOut', 
      x: '+=6', 
      y: '+=3', 
      z: '+=1.5', 
    });
  }
});

const cursor = { // Armazenar a posição do cursor
  x: 0,
  y: 0,
};

window.addEventListener('mousemove', (event) => { 
  cursor.x = event.clientX / sizes.width - 0.5; // Atualiza a posição X do cursor em relação ao tamanho da janela
  cursor.y = event.clientY / sizes.height - 0.5; // Atualiza a posição Y do cursor em relação ao tamanho da janela
});

// Animate
const clock = new THREE.Clock(); 
let previousTime = 0; // Armazena

const tick = () => { // Animação 
  const elapsedTime = clock.getElapsedTime(); 
  const deltaTime = elapsedTime - previousTime; // Calcula a diferença de tempo da última animação
  previousTime = elapsedTime; // Atualiza

  camera.position.y = (-scrollY / sizes.height) * objectsDistance; 

  const parallaxX = cursor.x / 2; // Calcula o efeito de paralaxe no eixo X
  const parallaxY = -cursor.y / 2; // Calcula o efeito de paralaxe no eixo Y

  cameraGroup.position.x += (parallaxX - cameraGroup.position.x) * 10 * deltaTime; // Aplica o movimento de paralaxe na posição X do grupo da câmera
  cameraGroup.position.y += (parallaxY - cameraGroup.position.y) * 10 * deltaTime; // Aplica o movimento de paralaxe na posição Y do grupo da câmera

  sectionMeshes.forEach((mesh) => { 
    mesh.rotation.x += deltaTime * 0.4; 
    mesh.rotation.y += deltaTime * 0.48; 
  });

  backgroundMesh.rotation.y += deltaTime * 0.2; 
  renderer.render(scene, camera); 
  window.requestAnimationFrame(tick); 
};

const clockElement = document.getElementById('clock'); 

const updateClock = () => { 
  const now = new Date(); 
  const hours = String(now.getHours()).padStart(2, '0'); 
  const minutes = String(now.getMinutes()).padStart(2, '0'); 
  const seconds = String(now.getSeconds()).padStart(2, '0'); 
  clockElement.textContent = `${hours}:${minutes}:${seconds}`; // Atualiza o conteúdo do relógio
};

setInterval(updateClock, 1000); // Chama a função updateClock a cada segundo
updateClock(); 
tick(); // Inicia