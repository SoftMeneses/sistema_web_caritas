document.addEventListener("DOMContentLoaded", () => {
    const modal = document.getElementById("usuariosActividadModal");

    if (!modal) {
        return;
    }

    const nombreElement = document.getElementById(
        "usuariosActividadNombre"
    );

    const contenidoElement = document.getElementById(
        "usuariosActividadContenido"
    );

    modal.addEventListener("show.bs.modal", async (event) => {
        const trigger = event.relatedTarget;

        if (!trigger) {
            return;
        }

        const actividadId = trigger.dataset.actividadId;
        const actividadNombre = trigger.dataset.actividadNombre;

        if (!actividadId) {
            contenidoElement.innerHTML = `
                <div class="alert alert-danger mb-0">
                    No se pudo identificar la actividad.
                </div>
            `;
            return;
        }

        nombreElement.textContent = actividadNombre || "";

        contenidoElement.innerHTML = `
            <div class="text-center py-4">
                <div
                    class="spinner-border"
                    role="status"
                    aria-hidden="true">
                </div>

                <p class="text-muted mt-2 mb-0">
                    Cargando usuarios...
                </p>
            </div>
        `;

        try {
            const respuesta = await fetch(
                `/api/actividades/${actividadId}/usuarios/`,
                {
                    method: "GET",
                    headers: {
                        "Accept": "application/json",
                    },
                }
            );

            if (!respuesta.ok) {
                throw new Error(
                    `Error HTTP: ${respuesta.status}`
                );
            }

            const usuarios = await respuesta.json();

            if (!usuarios.length) {
                contenidoElement.innerHTML = `
                    <div class="text-center py-4">
                        <i class="bi bi-people fs-1 text-muted"></i>

                        <p class="text-muted mt-3 mb-0">
                            No hay usuarios asignados a esta actividad.
                        </p>
                    </div>
                `;

                return;
            }

            contenidoElement.innerHTML = usuarios
                .map((asignacion) => `
                    <div class="d-flex align-items-center py-2 border-bottom">
                        <div class="me-3">
                            <i class="bi bi-person-circle fs-4 text-primary"></i>
                        </div>

                        <div>
                            <div class="fw-semibold">
                                ${escapeHtml(asignacion.usuario_nombre)}
                            </div>

                            <small class="text-muted">
                                ${escapeHtml(asignacion.usuario_email)}
                            </small>
                        </div>
                    </div>
                `)
                .join("");

        } catch (error) {
            console.error(
                "No se pudieron cargar los usuarios de la actividad:",
                error
            );

            contenidoElement.innerHTML = `
                <div class="alert alert-danger mb-0">
                    <i class="bi bi-exclamation-triangle me-2"></i>
                    No fue posible cargar los usuarios asignados.
                </div>
            `;
        }
    });

    function escapeHtml(valor) {
        const elemento = document.createElement("div");
        elemento.textContent = valor ?? "";
        return elemento.innerHTML;
    }
});