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

        document
            .getElementById("confirmForm")
            .action = url;

        document
            .getElementById("entityType")
            .textContent = entity;

        document
            .getElementById("entityName")
            .textContent = `"${name}"`;

    });

});