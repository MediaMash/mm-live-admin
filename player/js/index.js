const $video = document.querySelector('#video');
const $play = document.querySelector('#play');
const $pause = document.querySelector('#pause');
const $backward = document.querySelector('#backward');
const $forward = document.querySelector('#forward');

$play.addEventListener('click', handlePlay);
function handlePlay() {
    $video.play()
    $play.hidden = true
    $pause.hidden = false
}

$pause.addEventListener('click', handlePause);
function handlePause() {
    $video.pause()
    $pause.hidden = true
    $play.hidden = false
}

$backward.addEventListener('click', handleBackward);
function handleBackward() {
    /* $video.currentTime = $video.currentTime - 10; */
    $video.currentTime -= 10; /*.currentTime esta propiedad devuelve los segundos por donde va la reproducción de mi video*/
}

$forward.addEventListener('click', handleForward);
function handleForward() {
    $video.currentTime += 10;
}

/* para asignarle el máximo a mi barrita con el tiempo total de mi video */
const $progress = document.querySelector('#progress');
$video.addEventListener('loadedmetadata', handleLoaded);
function handleLoaded() {
    $progress.max = $video.duration; /*con .duration estoy pasándole el total de segundos que dura mi video y guardádondolo para que quede como mi máximo */
}

/* función para que la barrita se mueva */
$video.addEventListener('timeupdate', handleTimeUpDate);
function handleTimeUpDate() {
    $progress.value = $video.currentTime; /* .currentTime devuelve el numero del segundo en donde va mi video y se lo asigno a Value para que se mueva mi barrita */
}

/* hasta este punto no puedo manejar mi barrita con el mouse y poner el video en el minuto en el que yo quiero, para eso es la siguiente función */
$progress.addEventListener('input', HandleInput); /* input es un evento al igual que click, timeupdate, etc. */
function HandleInput(){
    $video.currentTime = $progress.value; /* le asigno al tiempo actual del video el valor de mi barrita  */
}
