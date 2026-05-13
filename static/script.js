const chatBox = document.getElementById("chat-box");

if (chatBox) {

    chatBox.scrollTop = chatBox.scrollHeight;
}

// =========================
// Typing Effect
// =========================

const typingTexts = document.querySelectorAll(".typing-text");

// 只选择最后一个
const lastText = typingTexts[typingTexts.length - 1];

if (lastText) {

    const originalText = lastText.innerText;

    lastText.innerText = "";

    let index = 0;

    function typeEffect() {

        if (index < originalText.length) {

            lastText.innerText += originalText.charAt(index);

            index++;

            setTimeout(typeEffect, 15);
        }
    }

    typeEffect();
}