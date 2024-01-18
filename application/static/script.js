const chatbox = document.getElementById("chatbox");
const userMessage = document.getElementById("user-message");
const sendButton = document.getElementById("send-button");
const speechButton = document.getElementById("speech-button");
const modeSelect = document.getElementById("mode-select");

let isSpeechMode = false;
let recognition;

function initializeSpeechRecognition() {
    recognition = new webkitSpeechRecognition();
    recognition.lang = 'en-US';
    recognition.continuous = true;

    recognition.onresult = (event) => {
        const last = event.results.length - 1;
        const userInput = event.results[last][0].transcript;
        userMessage.value = userInput;
        sendMessage();
    };

    recognition.onerror = (event) => {
        console.error("Speech recognition error:", event.error);
    };

    recognition.onend = () => {
        if (isSpeechMode) {
            recognition.start(); // Restart speech recognition if in continuous mode
        }
    };
}

initializeSpeechRecognition();

speechButton.addEventListener("click", () => {
    isSpeechMode = !isSpeechMode;

    if (isSpeechMode) {
        recognition.start();
    } else {
        recognition.stop();
    }
});

modeSelect.addEventListener("change", () => {
    isSpeechMode = modeSelect.value === "speech";

    if (isSpeechMode) {
        recognition.start();
    } else {
        recognition.stop();
    }
});

function createChatMessage(message, isUser) {
    const messageElement = document.createElement("div");
    messageElement.classList.add(isUser ? "user-message" : "bot-message");
    messageElement.textContent = message;
    chatbox.appendChild(messageElement);
    chatbox.scrollTop = chatbox.scrollHeight; // Auto-scroll to the bottom
}

userMessage.addEventListener("keydown", (event) => {
    if (event.key === "Enter") {
        sendMessage();
    }
});

function sendMessage() {
    const userInput = userMessage.value.trim();
    if (userInput) {
        createChatMessage('You :  \n' + userInput, true);
        userMessage.value = "";

        fetch("/generate_response", {
            method: "POST",
            body: JSON.stringify({ user_input: userInput }),
            headers: { "Content-Type": "application/json" }
        })
        .then(response => response.json())
        .then(data => {
            const botResponse = data.response;
            createChatMessage('Response : \n' + botResponse, false);
        })
        .catch(error => console.error(error));
    }
}

sendButton.addEventListener("click", sendMessage);
