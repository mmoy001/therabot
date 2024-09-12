document.addEventListener('DOMContentLoaded', initializeChat);

const sendButton = document.getElementById('send-btn');
const userInput = document.getElementById('user-input');
const messagesContainer = document.getElementById('messages');

sendButton.addEventListener('click', sendMessage);
userInput.addEventListener('keydown', (event) => {
    if (event.key === 'Enter') {
        sendMessage();
    }
});

async function initializeChat() {
    try {
        const response = await fetch('/new-context', { method: 'POST' });
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        const data = await response.json();
        
        addMessage('system', data.message);
    } catch (error) {
        console.error('Error:', error);
        addMessage('error', "Error: Unable to start a new chat session.");
    }
    userInput.focus();
}

async function sendMessage() {
    const message = userInput.value.trim();
    if (message === "") return;

    addMessage('user', message);
    userInput.value = '';

    try {
        const response = await fetch('/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: new URLSearchParams({
                'message': message
            })
        });

        if (!response.ok) {
            throw new Error('Network response was not ok');
        }

        const data = await response.json();
        addMessage('bot', data.response);
    } catch (error) {
        console.error('Error:', error);
        addMessage('error', "Error: Unable to get response from the server.");
    }

    userInput.focus();
}

function addMessage(sender, content) {
    const messageElement = document.createElement('div');
    messageElement.className = `message ${sender}`;
    messageElement.textContent = content;
    messagesContainer.appendChild(messageElement);
    scrollToBottom();
}

function scrollToBottom() {
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
}