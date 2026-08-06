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

        document
            .getElementById("confirmForm")
            .action = url;

        document
            .getElementById("entityName")
            .textContent = `"${name}"`;

    });

});