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

        const reader = response.body.getReader();
        const decoder = new TextDecoder();
        let botMessage = '';
        let botElement = null;

        while (true) {
            const { done, value } = await reader.read();
            if (done) break;

            const chunk = decoder.decode(value);
            const lines = chunk.split('\n\n');
            for (const line of lines) {
                if (line.startsWith('data: ')) {
                    const data = JSON.parse(line.slice(6));
                    if (data.delta) {
                        if (!botElement) {
                            botElement = document.createElement('div');
                            botElement.className = 'message bot';
                            messagesContainer.appendChild(botElement);
                        }
                        botMessage += data.delta;
                        botElement.textContent = botMessage;
                        scrollToBottom();
                    } else if (data.done) {
                        break;
                    } else if (data.error) {
                        addMessage('error', `Error: ${data.error}`);
                        break;
                    }
                }
            }
        }
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