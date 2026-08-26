/* =========================================================
   MOBILE SIDEBAR
========================================================= */

const menuButton =
    document.getElementById("menuButton");

const sidebar =
    document.getElementById("sidebar");


if (menuButton && sidebar) {

    menuButton.addEventListener(
        "click",
        function () {

            sidebar.classList.toggle("open");

        }
    );

}


/* =========================================================
   CONFIRM DELETE
========================================================= */

function confirmDelete(message) {

    return window.confirm(
        message || "Are you sure?"
    );

}


/* =========================================================
   NEWS EDITOR
========================================================= */

function openNewsEditor(
    id,
    title,
    content,
    status
) {

    const modal =
        document.getElementById("newsModal");

    const form =
        document.getElementById("newsEditForm");

    const titleInput =
        document.getElementById("editNewsTitle");

    const contentInput =
        document.getElementById("editNewsContent");

    const statusInput =
        document.getElementById("editNewsStatus");


    if (!modal || !form) {

        return;

    }


    form.action =
        "/news/edit/" + id;


    titleInput.value =
        title;


    contentInput.value =
        content;


    statusInput.value =
        status;


    modal.classList.add("show");

}


function closeNewsEditor() {

    const modal =
        document.getElementById("newsModal");

    if (modal) {

        modal.classList.remove("show");

    }

}


/* =========================================================
   SERVICE EDITOR
========================================================= */

function openServiceEditor(
    id,
    title,
    description,
    status
) {

    const modal =
        document.getElementById("serviceModal");

    const form =
        document.getElementById("serviceEditForm");

    const titleInput =
        document.getElementById("editServiceTitle");

    const descriptionInput =
        document.getElementById(
            "editServiceDescription"
        );

    const statusInput =
        document.getElementById(
            "editServiceStatus"
        );


    if (!modal || !form) {

        return;

    }


    form.action =
        "/services/edit/" + id;


    titleInput.value =
        title;


    descriptionInput.value =
        description;


    statusInput.value =
        status;


    modal.classList.add("show");

}


function closeServiceEditor() {

    const modal =
        document.getElementById("serviceModal");

    if (modal) {

        modal.classList.remove("show");

    }

}


/* =========================================================
   CLOSE MODALS BY CLICKING OUTSIDE
========================================================= */

document.addEventListener(
    "click",
    function (event) {

        const newsModal =
            document.getElementById("newsModal");

        const serviceModal =
            document.getElementById("serviceModal");


        if (
            newsModal &&
            event.target === newsModal
        ) {

            closeNewsEditor();

        }


        if (
            serviceModal &&
            event.target === serviceModal
        ) {

            closeServiceEditor();

        }

    }
);


/* =========================================================
   ESCAPE KEY
========================================================= */

document.addEventListener(
    "keydown",
    function (event) {

        if (event.key !== "Escape") {

            return;

        }


        closeNewsEditor();

        closeServiceEditor();

    }
);


/* =========================================================
   AUTO HIDE ALERTS
========================================================= */

document.addEventListener(
    "DOMContentLoaded",
    function () {

        const alerts =
            document.querySelectorAll(
                ".alert"
            );


        alerts.forEach(
            function (alert) {

                setTimeout(
                    function () {

                        alert.style.opacity =
                            "0";

                        alert.style.transform =
                            "translateY(-5px)";

                        alert.style.transition =
                            "all 0.3s ease";


                        setTimeout(
                            function () {

                                alert.remove();

                            },
                            300
                        );

                    },
                    4000
                );

            }
        );

    }
);