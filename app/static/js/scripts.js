function toggleChat() {
    const chatWidget = document.getElementById('chat-widget');
    chatWidget.classList.add('toggle_chat')
    chatWidget.classList.add('transition')
    chatWidget.style.display = (chatWidget.style.display === 'none' || chatWidget.style.display === '') ? 'flex' : 'none';
}

function sendMessage() { 
    const chatInput = document.getElementById('chat-input');
    const chatBody = document.getElementById('chat-body');
    const userMessage = chatInput.value;

    if (userMessage.trim() === "") return;

    // Añadir mensaje del usuario
    const userMessageElement = document.createElement('p');
    userMessageElement.classList.add('message', 'user');
    userMessageElement.innerText = userMessage;
    chatBody.appendChild(userMessageElement);

    // Limpiar el textarea
    chatInput.value = "";

    // Enviar mensaje al servidor Flask
    fetch('/chat', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ question: userMessage }),
    })
    .then(response => response.json())
    .then(data => {
        // Formatear la respuesta del bot para negrita y saltos de pagina
        const FormatResponse = data.response.replace(/\n/g, '<br>').replace(/\*\*(.*?)\*\*/g, '<b>$1</b>');
         

        const botMessageElement = document.createElement('p');
        botMessageElement.classList.add('message', 'bot');
        botMessageElement.innerHTML = FormatResponse;
        chatBody.appendChild(botMessageElement);

        // Desplazar hacia abajo para ver el nuevo mensaje
        chatBody.scrollTop = chatBody.scrollHeight;
    })
    .catch( error => { console.error('Error:', error);} );

    // Desplazar hacia abajo para ver el nuevo mensaje
    chatBody.scrollTop = chatBody.scrollHeight;
}
