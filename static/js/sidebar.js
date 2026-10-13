document.addEventListener("DOMContentLoaded", function () {
    const boton = document.getElementById("toggleSidebar");
    const sidebar = document.getElementById("sidebar-container");

    if (!boton || !sidebar) {
        return;
    }

    const consultaMovil = window.matchMedia("(max-width: 768px)");

    function actualizarModo() {
        if (consultaMovil.matches) {
            // En móvil, el menú funciona como panel superpuesto.
            sidebar.classList.remove("sidebar-collapsed");
        } else {
            // En escritorio, eliminar el estado de menú móvil.
            sidebar.classList.remove("sidebar-mobile-open");
        }
    }

    boton.addEventListener("click", function () {
        if (consultaMovil.matches) {
            sidebar.classList.toggle("sidebar-mobile-open");
        } else {
            sidebar.classList.toggle("sidebar-collapsed");
        }
    });

    consultaMovil.addEventListener("change", actualizarModo);

    actualizarModo();
});