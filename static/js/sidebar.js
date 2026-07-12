document.addEventListener("DOMContentLoaded", function(){

    const boton=document.getElementById("toggleSidebar");

    const sidebar=document.getElementById("sidebar-container");

    boton.addEventListener("click",function(){

        sidebar.classList.toggle("sidebar-collapsed");

    });

});