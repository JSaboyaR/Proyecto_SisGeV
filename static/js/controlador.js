window.onload= function(){
    var spaceCarga = document.getElementById('espacioLoding');

    spaceCarga.style.visibility = 'hidden';
    spaceCarga.style.opacity = '0';
}

function mostrarPassword(){
    var clave = document.getElementsByName("contrasena");
    clave[0].type = "text";
    var clave2 = document.getElementsByName("Ojo");
    clave2[0].className = "verClave1";
   
}

function ocultarPassword(){
    var clave = document.getElementsByName("contrasena");
    clave[0].type = "password";
    var clave2 = document.getElementsByName("Ojo");
    clave2[0].className = "verClave";
}


