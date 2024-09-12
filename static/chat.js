document.addEventListener('DOMContentLoaded', initializeChat);

document.getElementById('send-btn').addEventListener('click', async () => {
    await sendMessage();
});

document.getElementById('user-input').addEventListener('keydown', async (event) => {
    if (event.key === 'Enter') {
        await sendMessage();
    }
});

async function initializeChat() {
    try {
        const response = await fetch('/new-context', { method: 'POST' });
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        const data = await response.json();
        
        const messageContainer = document.getElementById('messages');
        const welcomeMessage = document.createElement('div');
        welcomeMessage.className = 'message system';
        welcomeMessage.innerText = data.message;
        messageContainer.appendChild(welcomeMessage);
    } catch (error) {
        console.error('Error:', error);
        const errorMessage = document.createElement('div');
        errorMessage.className = 'message system error';
        errorMessage.innerText = "Error: Unable to start a new chat session.";
        messageContainer.appendChild(errorMessage);
    }
}

async function sendMessage() {
    const userInput = document.getElementById('user-input').value;
    if (userInput.trim() === "") return;

    const messageContainer = document.getElementById('messages');
    
    // Display the user's message
    const userMessage = document.createElement('div');
    userMessage.className = 'message user';
    userMessage.innerText = "You: " + userInput;
    messageContainer.appendChild(userMessage);

    // Send the user's message to the backend
    try {
        const response = await fetch('/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: new URLSearchParams({
                'message': userInput
            })
        });

        if (!response.ok) {
            throw new Error('Network response was not ok');
        }

        const data = await response.json();

        // Display Claude's response
        const botMessage = document.createElement('div');
        botMessage.className = 'message bot';
        botMessage.innerText = "Claude: " + data.response;
        messageContainer.appendChild(botMessage);
    } catch (error) {
        console.error('Error:', error);
        const errorMessage = document.createElement('div');
        errorMessage.className = 'message bot error';
        errorMessage.innerText = "Error: Unable to get response from the server.";
        messageContainer.appendChild(errorMessage);
    }

    // Clear the input field
    document.getElementById('user-input').value = '';

    // Scroll to the bottom of the chat
    messageContainer.scrollTop = messageContainer.scrollHeight;
}