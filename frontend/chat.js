const input = document.getElementById("input");
const sendBtn = document.getElementById("send-btn");
const messages = document.getElementById("messages");

sendBtn.addEventListener("click", send);

input.addEventListener("keydown", (e) => {
  if (e.key === "Enter") {
    send();
  }
});

async function send() {
  const text = input.value.trim();
  if (!text) return;

  input.value = "";

  addMessage(text, "user");

  try {
    const res = await fetch("http://127.0.0.1:8000/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message: text })
    });

    const data = await res.json();
    addMessage(data.response, "system");
  } catch (err) {
    addMessage("Error al conectar con el backend 😢", "system");
  }
}

function addMessage(text, type) {
  const div = document.createElement("div");
  div.className = `message ${type}`;
  div.innerText = text;
  messages.appendChild(div);
  messages.scrollTop = messages.scrollHeight;
}
