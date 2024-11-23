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
