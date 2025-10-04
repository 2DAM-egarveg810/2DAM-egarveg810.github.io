// Crea un audio, reproduce el sonido y se elimina
export function create_aud_endpoint(file_src, volume=1){
    let audend = document.createElement("audio");
    audend.src = file_src;
    audend.volume = volume;
    audend.addEventListener("ended", (ev) => {
        document.body.removeChild(ev.target);
    });
    audend.play();
    document.body.appendChild(audend);
}
