document.addEventListener("DOMContentLoaded", function () {
    const sidebarToggle = document.getElementById("sidebar-toggle");
    const sidebar = document.getElementById("sidebar");

    sidebarToggle.addEventListener("click", () => {
        sidebar.classList.toggle("active");
    });

    // Закрываем сайдбар, если щелкаем вне его
    document.addEventListener("click", (e) => {
        if (!sidebar.contains(e.target) && !sidebarToggle.contains(e.target)) {
            sidebar.classList.remove("active");
        }
    });
});
