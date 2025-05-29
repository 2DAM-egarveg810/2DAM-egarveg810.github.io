function enseniar_puntos(){
    let fidelidad = document.getElementById('punto_fidelidad');
    let gasta_fidelidad = document.getElementById('gasta_punto_fidelidad');
    let rangu = document.getElementById('rango');
    let puntos_fidelidad = localStorage.getItem('puntos_fidelidad');
    let puntos_gastados = localStorage.getItem('puntos_fidelidad_gastados');

    if (fidelidad === null || gasta_fidelidad === null || rangu === null){
        return;
    }

    if (puntos_fidelidad === null){
        fidelidad.innerText = "0";
        localStorage.setItem('puntos_fidelidad', '0');
    }else{
        fidelidad.innerText = puntos_fidelidad;
    }

    if (puntos_gastados === null){
        gasta_fidelidad.parentNode.innerText = "No has gastado ningun punto de fidelidad";
        gasta_fidelidad.innerText = "";
        rangu.innerText = "Solo me pasaba por aqui";
    }else{
        gasta_fidelidad.innerText = puntos_gastados;

        let puntos_finales = ((puntos_fidelidad === null) ? 0 : parseInt(puntos_fidelidad)) + parseInt(puntos_gastados);
        
        if (puntos_finales <= 20){
            rangu.innerText = "Acabo de conocer la tienda";
        } else if (puntos_finales <= 50){
            rangu.innerText = "Full supporter de la tienda";
        }else{
            rangu.innerText = "Hardcore bakender. Subscrito a nuestro 'Only Bakends'"
        }
    }
}

enseniar_puntos();