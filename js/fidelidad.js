function enseniar_puntos(){
    let fidelidad = document.getElementById('punto_fidelidad');
    let puntos_fidelidad = localStorage.getItem('puntos_fidelidad');

    if (fidelidad === null){
        return;
    }

    if (puntos_fidelidad === null){
        fidelidad.innerText = "0";
    }else{
        puntos_fidelidad = puntos_fidelidad;
    }
}

enseniar_puntos();