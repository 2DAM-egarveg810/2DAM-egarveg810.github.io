/*const audio = document.getElementById('hidden-audio');
alert('me reproduzco');
audio.play().catch(e => {
    console.log("El navegador bloqueó la reproducción automática:", e);
});*/

let playing = false;

function cambiaIcono(){
    if (!playing){
        document.getElementById('playaudio').src = "img/play-button.png";
    }else{
        document.getElementById('playaudio').src = "img/pause-button.png";
    }
}

document.getElementById('playaudio').addEventListener('mouseover', () => {
    cambiaIcono();
   
});

document.getElementById('playaudio').addEventListener('mouseleave', () => {
    document.getElementById('playaudio').src = "img/cake-slice(1).png";
});

document.getElementById('playaudio').addEventListener('click', () => {
    const audio = document.getElementById('hidden-audio');
    if (!playing){
        audio.play().catch(e => {
            alert("No se puede reproducir la musiquita de bakend", e);
        });
    }else{
        audio.pause();
        audio.currentTime = 0;
    }
    playing = !playing;
    cambiaIcono();
});