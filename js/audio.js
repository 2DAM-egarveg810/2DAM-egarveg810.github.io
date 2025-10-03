let playing = false;
let saved_time;

const songURL = "aud/enchanted sunset.mp3";
const audioEndpoint = document.getElementById('hidden-audio');

function loadPlayState() {
    const savedTime = parseFloat(sessionStorage.getItem('song_current_time'));
    if (savedTime === null || isNaN(savedTime)){
        saved_time = 0;
        playing = false;
    }else{
        saved_time = savedTime;
        playing = true;
    }
}

// Save current play state and position
function savePlayState() {
    if (playing) {
        sessionStorage.setItem('song_current_time', audioEndpoint.currentTime.toString());
    }else{
        sessionStorage.removeItem("song_current_time");
    }
}

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
    document.getElementById('playaudio').src = "img/iconitofresh.png";
});

document.getElementById('playaudio').addEventListener('click', () => {
    if (!playing){
        audioEndpoint.play().catch(e => {
            alert("No se puede reproducir la musiquita de bakend", e);
            playing = true;
        });
    }else{
        audioEndpoint.pause();
        audioEndpoint.currentTime = 0;
    }
    playing = !playing;
    cambiaIcono();
});

window.addEventListener('load', async () => {
    loadPlayState();

    if (saved_time != 0){
        audioEndpoint.currentTime = saved_time;
        audioEndpoint.setAttribute("autoplay", "");
        // Para que google no se queje
        document.addEventListener("click", function click_s() {
            playing = true;
            audioEndpoint.play().catch(err =>{
                console.log("Autoplay failed: " + err);
                playing = false;
            });
            document.removeEventListener("click", click_s);
       });
    }
});
audioEndpoint.addEventListener("timeupdate", () => {
    savePlayState()
});

/*
window.onbeforeunload = savePlayState;
window.addEventListener("beforeunload", savePlayState);
*/
