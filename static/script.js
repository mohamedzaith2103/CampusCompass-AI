async function sendMessage() {
    let input = document.getElementById("userInput");
    let message = input.value.trim();

    if (message === "") {
        return;
    }

    let chatBox = document.getElementById("chatBox");

    // User message
    let userMessage = document.createElement("div");
    userMessage.className = "user-message";
    userMessage.innerText = message;
    chatBox.appendChild(userMessage);

    // Bot typing message
    let botMessage = document.createElement("div");
    botMessage.className = "bot-message";
    botMessage.innerText = "🤖 Thinking...";
    chatBox.appendChild(botMessage);

    input.value = "";
    chatBox.scrollTop = chatBox.scrollHeight;

    try {
        const response = await fetch("/chat", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                message: message
            })
        });

        const data = await response.json();

        botMessage.innerText = data.reply || data.error;

    } catch (error) {
        botMessage.innerText = "❌ Server Error";
    }

    chatBox.scrollTop = chatBox.scrollHeight;
}

// Press Enter to send
document.getElementById("userInput").addEventListener("keypress", function(event) {
    if (event.key === "Enter") {
        sendMessage();
    }
});