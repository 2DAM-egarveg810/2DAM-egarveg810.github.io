const canvas = document.getElementById('matrix');
const ctx = canvas.getContext('2d');
const letters = (
    'あいうえおかきくけこさしすせそたちつてとなにぬねの' +  // hiragana
    'アイウエオカキクケコサシスセソタチツテトナニヌネノ' +  // katakana
    '0123456789'
).split('');

// Paleta de colores pastel oscuros
const colors = [
    '#C4A484', // marrón claro topo
    '#7E5E3B', // marrón medio
    '#5B3A29', // marrón oscuro
    '#A67B5B', // marrón caramelo
    '#D2B48C'  // marrón arena claro
];

const colorsChef = [
    '#FF69B4', // rosa chicle
    '#FFD700', // amarillo dorado (tipo pastel de cumpleaños)
    '#00FFFF', // cian eléctrico
    '#FF4500', // naranja intenso (glaseado loco)
    '#8A2BE2', // púrpura brillante
    '#00FF00', // verde neón
    '#FF1493', // rosa fuerte (tipo frosting)
    '#1E90FF', // azul brillante
    '#FF6347', // rojo tomate (pero saturado)
    '#9400D3'  // violeta intenso // marrón arena claro
];
let chefmode = false;
let chefCont = 0;
let w, h;
const fontSize = 16;
let columns;
let drops;

function resize() {
    w = window.innerWidth;
    h = window.innerHeight;
    canvas.width = w;
    canvas.height = h;
}
function resize_columns(arr, newSize, defaultValue) {
    if (arr.length >= newSize){
        return;
    }
    var originLength = arr.length; // cache original length
    arr.length = newSize; // resize array to newSize
    if (newSize > originLength){
        arr.fill(defaultValue, originLength);
    } 
}

function draw(){
    columns = Math.floor(w / fontSize);
    resize_columns(drops, columns, 0);

    // Fondo semitransparente para efecto estela
    ctx.fillStyle = 'rgba(18,18,18, 0.1)';
    ctx.fillRect(0, 0, w, h);

    ctx.font = fontSize + 'px monospace';

    for (let i = 0; i < columns; i++) {
        // Elegimos letra y color aleatorio para esta columna y posición
        const text = letters[Math.floor(Math.random() * letters.length)];
        let color;
        if (!chefmode){
            color = colors[Math.floor(Math.random() * colors.length)];
        }else{
            color = colorsChef[Math.floor(Math.random() * colorsChef.length)];
        }
        
        ctx.fillStyle = color;

        // Dibujar letra
        ctx.fillText(text, i * fontSize, drops[i] * fontSize);

        // Reincio aleatorio para caída infinita
        if(drops[i] * fontSize > h && Math.random() > 0.975) {
            drops[i] = 0;
        }
        drops[i]++;
    }
}

function init(){
    window.addEventListener('resize', resize);
    document.getElementById('playaudio').addEventListener('click', () => {
        chefCont++;
        if(chefCont >=10){
          chefmode = true;
        }
    });
    resize();
    columns = Math.floor(w / fontSize);
    drops = Array(columns).fill(0);
    setInterval(draw, 50);
}
init();