document.addEventListener("DOMContentLoaded", () => {

    const modal = document.getElementById("confirmModal");

    if (!modal) {

        return;

    }

    modal.addEventListener("show.bs.modal", event => {

        const trigger = event.relatedTarget;

        if (!trigger) {

            return;

        }

        const url = trigger.dataset.url;

        const name = trigger.dataset.name;

        const entity = trigger.dataset.entity || "elemento";

        const message = (
            trigger.dataset.message
            || `¿Está seguro de desactivar este ${entity}?`
        );

        document
            .getElementById("confirmForm")
            .action = url;

        document
            .getElementById("confirmModalMessage")
            .textContent = message;

        document
            .getElementById("entityName")
            .textContent = `"${name}"`;

   });

});