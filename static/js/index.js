// Selecting DOM elements
const button = document.querySelector('.button');
const input = document.querySelector('.input');
const chat = document.querySelector('.chat');
const form = document.querySelector('.form');

// Get llama response for user input and render in frontend
button.addEventListener('click', (e) => {
    e.preventDefault();
    if (input.value == '') {
        return
    }

    // Getting user input
    const prompt = input.value;
    input.value = '';

    // Adding user's message to the chat
    chat.innerHTML += `
        <div class="user chat__message">
            ${prompt}
        </div>
        <div class="assistant chat__message">
            <div class="spinner">
                <div class="bounce1"></div>
                <div class="bounce2"></div>
                <div class="bounce3"></div>
            </div>
        </div>
    `;
    
    // Scrolling to the bottom of the chat container
    chat.scrollTop = chat.scrollHeight;

    // Making a POST request to the server with user input
    fetch('/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            prompt: prompt
        })
    })
    .then(response => response.json())
    .then((data) => {
        // Updating the chat container with assistant's responses
        let chatContent = [];
        data.map((message) => {
            if (message.role !== "system") {
                chatContent.push(
                    `<div
                    class="${message.role} chat__message"
                    style="margin-bottom: 20px"
                    >
                    ${message.content}
                    </div>`
                    );
            }
        });
        // Updating the chat container content
        chat.innerHTML = chatContent.join("");
        // Scrolling to the bottom of the updated chat container
        chat.scrollTop = chat.scrollHeight;
    })
    .catch(error => console.error(error));
});
