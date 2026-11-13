
// Automatically dismiss success messages
// after five seconds.

document.addEventListener("DOMContentLoaded", function () {

    const alerts = document.querySelectorAll(".alert");

    alerts.forEach(function (alert) {

        setTimeout(function () {

            if (typeof bootstrap !== "undefined") {
                const alertInstance =
                    bootstrap.Alert.getOrCreateInstance(alert);

                alertInstance.close();
            }

        }, 5000);

    });

});
