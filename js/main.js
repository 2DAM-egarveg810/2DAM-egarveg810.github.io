// Menú hamburguesa
document.getElementById("menu-toggle").addEventListener("click", () => {
  document.getElementById("nav-menu").classList.toggle("active");
});

let fidelidad_mode = document.body.id.includes('fidelidad');

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
    { singular: "Pan de código", plural: "Panes de código" },
    { singular: "Croissant binario", plural: "Croissants binarios" },
    { singular: "Tarta digital", plural: "Tartas digitales" },
    { singular: "Bollo de bits", plural: "Bollos de bits" },
    { singular: "Bizcocho en la nube", plural: "Bizcochos en la nube" },
    { singular: "Napolitana cacheada", plural: "Napolitanas cacheadas" },
    { singular: "Baguette de algoritmo", plural: "Baguettes de algoritmo" },
    { singular: "Rosquilla de bytes", plural: "Rosquillas de bytes" },
    { singular: "Galleta firewall", plural: "Galletas firewall" },
    { singular: "Pan integral cifrado", plural: "Panes integrales cifrados" },
];

const cantidades = [1, 2, 3, 4, 5];

const ciudades = [
    "Madrid",
    "Barcelona",
    "Valencia",
    "Sevilla",
    "Zaragoza",
    "Málaga",
    "Murcia",
    "Palma",
    "Las Palmas",
    "Bilbao",
    "Alicante",
    "Córdoba",
    "Valladolid",
    "Vigo",
    "Gijón",
];

function generarEntrada() {
    const nombre = nombres[Math.floor(Math.random() * nombres.length)];
    const producto =
    productosTech[Math.floor(Math.random() * productosTech.length)];
    const cantidad = cantidades[Math.floor(Math.random() * cantidades.length)];
    const ciudad = ciudades[Math.floor(Math.random() * ciudades.length)];

    const productoTexto = cantidad === 1 ? producto.singular : producto.plural;

    return `Cliente: ${nombre} - Compró ${cantidad} ${productoTexto} en la tienda de ${ciudad}`;
}

// Agregar al log
const logList = document.getElementById("log-list");

function agregarEntradaAlLog() {
    const entrada = generarEntrada();
    const li = document.createElement("li");
    li.textContent = entrada;
    if (logList !== null){
        logList.appendChild(li);
        // Scroll automático hacia abajo
        logList.parentElement.scrollTop = logList.parentElement.scrollHeight;
    }
}

// Genera algunas entradas iniciales
for (let i = 0; i < 5; i++) {
    agregarEntradaAlLog();
}

// Añade una nueva cada 5 segundos
setInterval(agregarEntradaAlLog, 8000);

const carritoLateral = document.getElementById("carrito-lateral");
const btnCarrito = document.getElementById("btn-carrito");
const listaCarrito = document.getElementById("lista-carrito");
const totalCarrito = document.getElementById("total-carrito");
const btnVaciar = document.getElementById("vaciar-carrito");
const btnComprar = document.getElementById("comprar-carrito");
const botonesAgregar = document.querySelectorAll(".boton-agregar");
const logAviso = document.getElementById('log_aviso');
//logAviso.style.top = "0%";


function abrirCarrito() {
    carritoLateral.classList.toggle("abierto");
    btnCarrito.classList.toggle("abierto");

    if (carritoLateral.classList.contains("abierto")) {
        btnCarrito.textContent = "✖";
        //btnCarrito.style.right = "320px"; // Se mueve hacia la izquierda del carrito
    } else {
        btnCarrito.textContent = "🛒";
        //btnCarrito.style.right = "20px"; // Vuelve a la esquina derecha
    }
}

let carrito = {};
btnCarrito.addEventListener("click", () => {
    abrirCarrito();
});

function loadcarrito(){
    //alert('cagada de manual');
    if (fidelidad_mode){
        carrito = {};
    }else{
        let carritocargado = localStorage.getItem('carrito');

        if (carritocargado == null){
            carrito = {};
        }else{
            carrito = JSON.parse(carritocargado);
        }
    }
    actualizarCarrito();
}

window.addEventListener('load', loadcarrito);

function quita_uno(item){
    let nom = item.attributes["itemname"];
    carrito[nom].cantidad -= 1;
    if (carrito[nom].cantidad <= 0){
        delete carrito[nom];
    }
    actualizarCarrito();
    /*const nombre = boton.getAttribute("data-nombre");
    const precio = parseFloat(boton.getAttribute("data-precio"));*/
}

function actualizarCarrito() {
    listaCarrito.innerHTML = "";

    let total = 0;
    for (const key in carrito) {
        const item = carrito[key];
        total += item.precio * item.cantidad;

        const li = document.createElement("li");
        li.textContent = `${item.nombre} x${item.cantidad}`;

        const precioSpan = document.createElement("span");
        if (fidelidad_mode){
            precioSpan.textContent = `${(item.precio * item.cantidad).toString()}pt`;
        }else{
            precioSpan.textContent = `$${(item.precio * item.cantidad).toFixed(2)}`;
        }
        const cierra = document.createElement('span');
        cierra.textContent = '✖';
        cierra.attributes["itemname"] = key;
        cierra.id = "quititem";
        cierra.addEventListener('click', (item) => {
            quita_uno(item.target);
        });

        li.appendChild(precioSpan);
        li.appendChild(cierra);
        listaCarrito.appendChild(li);
    }

    if (!fidelidad_mode){
        localStorage.setItem('carrito', JSON.stringify(carrito));
    }

    totalCarrito.textContent = total.toFixed(2);
}

let cookieClick = 0;

botonesAgregar.forEach((boton) => {
    boton.addEventListener("click", () => {
        const nombre = boton.getAttribute("data-nombre");
        const precio = parseFloat(boton.getAttribute("data-precio"));

        if (carrito[nombre]) {
            carrito[nombre].cantidad += 1;
        } else {
            carrito[nombre] = { nombre, precio, cantidad: 1 };
        }

        if (nombre === "Galleta firewall") {
            cookieClick++;
            if (cookieClick === 20) {
                boton.textContent = "Cookie Clicker";
                document.title = "Cookie Clicker";
            }
            if (cookieClick === 50) {
                boton.textContent = "Se viene sindrome del tunel carpiano";
            }
        }

        actualizarCarrito();
        //alert(window.innerWidth)
        if (!carritoLateral.classList.contains("abierto") && window.innerWidth > 768) {
            abrirCarrito();
        }
    });
});

btnVaciar.addEventListener("click", () => {
    carrito = {};
    actualizarCarrito();
});

btnComprar.addEventListener("click", () => {
    let precio_final = 0;
    for (const [key, value] of Object.entries(carrito)) {
        let entrada = `Cliente: Compraste ${value.cantidad} ${value.nombre} en tu casa`;
        const li = document.createElement("li");
        li.textContent = entrada;
        if (logList !== null){
            logList.appendChild(li);
            // Scroll automático hacia abajo
            logList.parentElement.scrollTop = logList.parentElement.scrollHeight;
        }
        precio_final += value.cantidad * value.precio;
    }
    
    // Actualiza los puntos de fidelidad
    if (fidelidad_mode){
        // Hace cositas
        let puntos_fidelidad = parseInt(localStorage.getItem('puntos_fidelidad'));
        if (puntos_fidelidad === null || puntos_fidelidad < precio_final){
            alert('Error: No tienes los suficientes puntos de fidelidad.');
        }else{
            localStorage.setItem('puntos_fidelidad', (puntos_fidelidad - precio_final).toString());
            let puntos_gastados = parseInt(localStorage.getItem('puntos_fidelidad_gastados'));
            if (puntos_gastados === null || isNaN(puntos_gastados)){
                localStorage.setItem('puntos_fidelidad_gastados', puntos_fidelidad.toString())
            }else{
                localStorage.setItem('puntos_fidelidad_gastados', (puntos_fidelidad+puntos_gastados).toString())
            }
            document.location.reload();
        }
    }else{
        // Añade puntos de fidelidad
        let puntos_obtenidos = Math.trunc(precio_final / 6);
        let puntos_fidelidad = parseInt(localStorage.getItem('puntos_fidelidad'));
        
    
        if (puntos_fidelidad === null){
            puntos_fidelidad = puntos_obtenidos;
        }else{
            puntos_fidelidad = puntos_fidelidad + puntos_obtenidos;
        }
    
        localStorage.setItem('puntos_fidelidad', puntos_fidelidad.toString());
    }

    carrito = {};
    actualizarCarrito();
});

function toggleCarrito() {
    const carrito = document.querySelector(".carrito-lateral");
    carrito.classList.toggle("visible");
}

let secret = "";

document.addEventListener("keydown", (e) => {
    secret += e.key.toLowerCase();
    if (secret.includes("galleta")) {
        let url = "https://orteil.dashnet.org/cookieclicker/";
        //window.location.href = url;
        window.open(url, '_blank').focus();
        secret = ""; // reset
    }
});
