

// Menú hamburguesa
document.getElementById('menu-toggle').addEventListener('click', () => {
    document.getElementById('nav-menu').classList.toggle('active');
  });
  
  const nombres = [
    'Ana', 'Luis', 'Marta', 'Pedro', 'Laura',
    'Carlos', 'Paula', 'Jorge', 'Lucía', 'Iván',
    'Sofía', 'Alberto', 'Carmen', 'Diego', 'Isabel',
    'Fernando', 'Elena', 'David', 'María', 'Manuel',
    'Patricia', 'Raúl', 'Sandra', 'Javier', 'Verónica',
    'Andrés', 'Natalia', 'Rubén', 'Beatriz', 'Sergio',
    'Irene', 'Antonio', 'Mercedes', 'Alba', 'Óscar',
    'Mónica', 'Juan', 'Cristina', 'Miguel', 'Carla',
    'Eduardo', 'Silvia', 'Pablo', 'Teresa', 'Hugo',
    'Rosa', 'Francisco', 'Natalia', 'Samuel', 'Marta',
    'Marcos', 'Inés', 'Víctor', 'Paula', 'Raquel',
    'Diego', 'Lorena', 'Óliver', 'Nuria', 'Joaquín',
    'Sara', 'Alfredo', 'Noelia', 'Enrique', 'Alicia',
    'Rubén', 'Celia', 'Esteban', 'Verónica', 'David',
    'Elisa', 'Mario', 'Claudia', 'Ignacio', 'Ángela'
  ];
  
  
  const productosTech = [
    { singular: 'Pan de código', plural: 'Panes de código' },
    { singular: 'Croissant binario', plural: 'Croissants binarios' },
    { singular: 'Tarta digital', plural: 'Tartas digitales' },
    { singular: 'Bollo de bits', plural: 'Bollos de bits' },
    { singular: 'Bizcocho en la nube', plural: 'Bizcochos en la nube' },
    { singular: 'Napolitana cacheada', plural: 'Napolitanas cacheadas' },
    { singular: 'Baguette de algoritmo', plural: 'Baguettes de algoritmo' },
    { singular: 'Rosquilla de bytes', plural: 'Rosquillas de bytes' },
    { singular: 'Galleta firewall', plural: 'Galletas firewall' },
    { singular: 'Pan integral cifrado', plural: 'Panes integrales cifrados' }
  ];
  
  
  
  const cantidades = [1, 2, 3, 4, 5];
  
  const ciudades = [
    'Madrid', 'Barcelona', 'Valencia', 'Sevilla', 'Zaragoza',
    'Málaga', 'Murcia', 'Palma', 'Las Palmas', 'Bilbao',
    'Alicante', 'Córdoba', 'Valladolid', 'Vigo', 'Gijón'
  ];
  
  function generarEntrada() {
    const nombre = nombres[Math.floor(Math.random() * nombres.length)];
    const producto = productosTech[Math.floor(Math.random() * productosTech.length)];
    const cantidad = cantidades[Math.floor(Math.random() * cantidades.length)];
    const ciudad = ciudades[Math.floor(Math.random() * ciudades.length)];
  
    const productoTexto = cantidad === 1 ? producto.singular : producto.plural;
  
    return `Cliente: ${nombre} - Compró ${cantidad} ${productoTexto} en la tienda de ${ciudad}`;
  }
  
  
  // Agregar al log
  const logList = document.getElementById('log-list');
  
  function agregarEntradaAlLog() {
    const entrada = generarEntrada();
    const li = document.createElement('li');
    li.textContent = entrada;
    logList.appendChild(li);
    // Scroll automático hacia abajo
    logList.parentElement.scrollTop = logList.parentElement.scrollHeight;
  }
  
  // Genera algunas entradas iniciales
  for (let i = 0; i < 5; i++) {
    agregarEntradaAlLog();
  }
  
  // Añade una nueva cada 5 segundos
  setInterval(agregarEntradaAlLog, 8000);
  
  const carritoLateral = document.getElementById('carrito-lateral');
const btnCarrito = document.getElementById('btn-carrito');
const listaCarrito = document.getElementById('lista-carrito');
const totalCarrito = document.getElementById('total-carrito');
const btnVaciar = document.getElementById('vaciar-carrito');
const botonesAgregar = document.querySelectorAll('.boton-agregar');

let carrito = {};
btnCarrito.addEventListener('click', () => {
    carritoLateral.classList.toggle('abierto');
  
    if (carritoLateral.classList.contains('abierto')) {
      btnCarrito.textContent = '✖';
      btnCarrito.style.right = '320px'; // Se mueve hacia la izquierda del carrito
    } else {
      btnCarrito.textContent = '🛒';
      btnCarrito.style.right = '20px'; // Vuelve a la esquina derecha
    }
  });
function actualizarCarrito() {
  listaCarrito.innerHTML = '';

  let total = 0;
  for (const key in carrito) {
    const item = carrito[key];
    total += item.precio * item.cantidad;

    const li = document.createElement('li');
    li.textContent = `${item.nombre} x${item.cantidad}`;
    
    const precioSpan = document.createElement('span');
    precioSpan.textContent = `$${(item.precio * item.cantidad).toFixed(2)}`;

    li.appendChild(precioSpan);
    listaCarrito.appendChild(li);
  }

  totalCarrito.textContent = total.toFixed(2);
}

botonesAgregar.forEach(boton => {
  boton.addEventListener('click', () => {
    const nombre = boton.getAttribute('data-nombre');
    const precio = parseFloat(boton.getAttribute('data-precio'));

    if(carrito[nombre]) {
      carrito[nombre].cantidad += 1;
    } else {
      carrito[nombre] = { nombre, precio, cantidad: 1 };
    }

    actualizarCarrito();
  });
});

btnVaciar.addEventListener('click', () => {
  carrito = {};
  actualizarCarrito();
});
  

  function toggleCarrito() {
    const carrito = document.querySelector('.carrito-lateral');
    carrito.classList.toggle('visible');
  }

  (() => {
    const canvas = document.getElementById('matrix');
    const ctx = canvas.getContext('2d');
  
    // Ajustamos tamaño
    let w, h;
    function resize() {
      w = window.innerWidth;
      h = window.innerHeight;
      canvas.width = w;
      canvas.height = h;
    }
    window.addEventListener('resize', resize);
    resize();
  
    // Letras que caen (puedes cambiar o ampliar)
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
    // Columnas
    const fontSize = 16;
    let columns = Math.floor(w / fontSize);
  
    // Posición vertical de cada columna
    let drops = Array(columns).fill(0);
    function resize_cols(arr, newSize, defaultValue) {
        if (arr.length >= newSize){
            return;
        }
        var originLength = arr.length; // cache original length

        arr.length = newSize; // resize array to newSize

        (newSize > originLength) && arr.fill(defaultValue, originLength); 
    }

    function draw() {
      columns = Math.floor(w / fontSize);
      resize_cols(drops, columns, 0);
	
      // Fondo semitransparente para efecto estela
      ctx.fillStyle = 'rgba(18,18,18, 0.1)';
      ctx.fillRect(0, 0, w, h);
  
      ctx.font = fontSize + 'px monospace';
  
      for(let i = 0; i < columns; i++) {
        // Elegimos letra y color aleatorio para esta columna y posición
        const text = letters[Math.floor(Math.random() * letters.length)];
        const color = colors[Math.floor(Math.random() * colors.length)];
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
  
    setInterval(draw, 50);
  })();

  