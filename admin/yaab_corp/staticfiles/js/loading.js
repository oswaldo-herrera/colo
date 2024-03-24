document.addEventListener("DOMContentLoaded", function () {
    console.log("El script de carga se ha ejecutado correctamente.");

    document.getElementById('loading-container').style.display = 'block';


    window.addEventListener('load', function () {

        setTimeout(function () {
            document.getElementById('loading-container').style.display = 'none';
        }, 1500);
        //document.getElementById('loading-container').style.display = 'none';
        
    });
});