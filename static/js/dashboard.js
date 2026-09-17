document.addEventListener("DOMContentLoaded", () => {
    const programasElement = document.getElementById("dashboard-programas");
    const actividadesElement = document.getElementById("dashboard-actividades");
    const beneficiariosElement = document.getElementById("dashboard-beneficiarios");
    const inventarioElement = document.getElementById("dashboard-inventario");

    if (
        !programasElement ||
        !actividadesElement ||
        !beneficiariosElement ||
        !inventarioElement
    ) {
        return;
    }

    async function cargarEstadisticas() {
        try {
            const respuesta = await fetch("/api/dashboard/estadisticas/", {
                method: "GET",
                headers: {
                    "Accept": "application/json",
                },
            });

            if (!respuesta.ok) {
                throw new Error(
                    `Error HTTP al consultar estadísticas: ${respuesta.status}`
                );
            }

            const datos = await respuesta.json();

            programasElement.textContent = datos.programas;
            actividadesElement.textContent = datos.actividades;
            beneficiariosElement.textContent = datos.beneficiarios;
            inventarioElement.textContent = datos.inventario;
        } catch (error) {
            console.error("No se pudieron cargar las estadísticas:", error);
        }
    }

    cargarEstadisticas();
});