// Открытие модального окна для аватара
document.getElementById("profile-avatar").onclick = function () {
    const modal = document.getElementById("avatar-modal");
    const modalImg = document.getElementById("avatar-modal-img");
    modal.style.display = "flex"; 
    modalImg.src = this.src;
};

// Закрытие модального окна для аватара
document.querySelector("#avatar-modal .close").onclick = function () {
    document.getElementById("avatar-modal").style.display = "none";
};

// Открытие модального окна для постов
document.querySelectorAll(".post-zoom").forEach((postImage) => {
    postImage.onclick = function () {
        const modal = document.getElementById("post-modal");
        const modalImg = document.getElementById("post-modal-img");
        modal.style.display = "flex"; 
        modalImg.src = this.src;
    };
});

// Закрытие модального окна для постов
document.querySelector("#post-modal .close").onclick = function () {
    document.getElementById("post-modal").style.display = "none";
};


document.addEventListener('DOMContentLoaded', function () {
    const tabButtons = document.querySelectorAll('.tab-button');
    const tabContents = document.querySelectorAll('.tab-content');

    tabButtons.forEach(button => {
        button.addEventListener('click', function () {
            const targetTab = this.getAttribute('data-tab');

            // Убираем активные классы со всех кнопок и содержимого
            tabButtons.forEach(btn => btn.classList.remove('active'));
            tabContents.forEach(content => content.classList.remove('active'));

            // Добавляем активный класс к выбранной кнопке и вкладке
            this.classList.add('active');
            document.getElementById(targetTab).classList.add('active');
        });
    });
});
