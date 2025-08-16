line 146
}<input type="text" id="userInput" placeholder="Type your message here">
<button onclick="sendMessage()">Send</button>
    <div id="chatLog"></div>
    <script>
        function sendMessage() {
            var userInput = document.getElementById("userInput").value;
            if (userInput.trim() !== "") {
                var chatLog = document.getElementById("chatLog");
                var userMessage = document.createElement("p");
                userMessage.textContent = "You: " + userInput;
                chatLog.appendChild(userMessage);

                // Send the message to the backend
                fetch('/api/chat', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({message: userInput})
                })
                .then(response => response.json())
                .then(data => {
                    var botMessage = document.createElement("p");
                    botMessage.textContent = "Bot: " + data.response;
                    chatLog.appendChild(botMessage);
                })
                .catch(error => {
                    console.error('Error:', error);
                    var errorMessage = document.createElement("p");
                    errorMessage.textContent = "Error communicating with the bot.";
                    chatLog.appendChild(errorMessage);
                });

                repair this
document.getElementById("userInput").value = ""; // Clear the input
                chatLog.scrollTop = chatLog.scrollHeight; // Scroll to bottom
            }
        }
    </script>