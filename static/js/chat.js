

// Получаем элементы DOM
const messagesContainer = document.getElementById("messages-container");
const messageInput = document.getElementById("message-input");
const sendButton = document.getElementById("send-button");

// Подключение к WebSocket
const socket = new WebSocket(
    `ws://${window.location.host}/ws/messages/${conversationId}/`
);


// Обработка входящих сообщений
socket.onmessage = function (event) {
    const data = JSON.parse(event.data);

    // Создаем новый элемент для сообщения
    const newMessage = document.createElement("div");
    newMessage.classList.add("message", data.sender === "me" ? "sent" : "received");
    newMessage.innerHTML = `
        <p>${data.message}</p>
        <span class="message-time">${data.timestamp}</span>
    `;

    // Добавляем сообщение в контейнер
    messagesContainer.appendChild(newMessage);
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
};

// Обработка отправки сообщения
sendButton.addEventListener("click", function () {
    const message = messageInput.value.trim();

    if (message) {
        if (socket.readyState === WebSocket.OPEN) {
            // Отправляем сообщение через WebSocket
            socket.send(JSON.stringify({
                message: message
            }));

            // Очищаем поле ввода и устанавливаем фокус
            messageInput.value = "";
            messageInput.focus();
        } else {
            console.error("WebSocket-соединение не установлено.");
        }
    }
});

// Обработка ошибок WebSocket
socket.onerror = function (error) {
    console.error("Ошибка WebSocket:", error);
};

// Обработка закрытия соединения
socket.onclose = function (e) {
    console.warn("WebSocket закрыт:", e);
};

// Устанавливаем автофокус на поле ввода
messageInput.focus();
