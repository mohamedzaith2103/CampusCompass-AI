async function sendMessage() {
    var input = document.getElementById('userInput');
    var text = input.value.trim();
    if (!text) return;
    
    addUserMessage(text);
    input.value = '';
    showTyping();
    
    // Flask backend ku POST request
    try {
        const response = await fetch('/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message: text })
        });
        const data = await response.json();
        hideTyping();
        addBotMessage(data.reply);
    } catch (error) {
        hideTyping();
        addBotMessage('Sorry, something went wrong! Try again.');
    }
}