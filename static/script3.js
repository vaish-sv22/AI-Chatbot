async function sendMessage() {

    const input = document.getElementById("user-input");
    const chatBox = document.getElementById("chat-box");

    const message = input.value.trim();

    if (message === "") {
        return;
    }

    // Display user message
    const userMessage = document.createElement("div");
    userMessage.className = "user-message";
    userMessage.innerHTML = "<strong>You:</strong> " + message;
    chatBox.appendChild(userMessage);

    // Clear input
    input.value = "";

    // Scroll to bottom
    chatBox.scrollTop = chatBox.scrollHeight;

    // Display thinking message
    const thinking = document.createElement("div");
    thinking.className = "bot-message";
    thinking.innerHTML = "<strong>Bot:</strong> Thinking...";
    chatBox.appendChild(thinking);

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

        thinking.innerHTML = "<strong>Bot:</strong> " + data.reply;

    }
    catch (error) {

        thinking.innerHTML =
            "<strong>Bot:</strong> Unable to connect to the server.";

        console.error(error);

    }

    chatBox.scrollTop = chatBox.scrollHeight;
}

// Send message when Enter is pressed
document.getElementById("user-input").addEventListener("keypress", function(event){

    if(event.key === "Enter"){

        sendMessage();

    }

});