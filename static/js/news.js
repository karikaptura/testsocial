document.addEventListener("DOMContentLoaded", function () {
    const likeButtons = document.querySelectorAll(".like-button");

    likeButtons.forEach(button => {
        button.addEventListener("click", function () {
            const postId = this.dataset.postId;

            fetch(`/news/toggle-like/${postId}/`, {
                method: "POST",
                headers: {
                    "X-CSRFToken": document.querySelector('[name=csrfmiddlewaretoken]').value
                }
            })
                .then(response => response.json())
                .then(data => {
                    this.querySelector(".likes-count").textContent = data.likes_count;
                })
                .catch(error => console.error("Ошибка:", error));
        });
    });
});
