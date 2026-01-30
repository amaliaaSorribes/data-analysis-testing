const input = document.getElementById("input");
const sendBtn = document.getElementById("send-btn");
const messages = document.getElementById("messages");
const uploadBtn = document.getElementById("uploadBtn");
const mdInput = document.getElementById("mdUpload");

const chatOptionsHTML = `
<ol>
  <li>Añadir meeting y transcript</li>
  <li>Listar meetings</li>
  <li>Listar US's en backlog</li>
  <li>Ver una US específica</li>
  <li>Simular cambio de estado de una US</li>
  <li>Revisar US Done y proponer cambios</li>
</ol>`;

uploadBtn.disabled = true;

// Evento del botón de upload
uploadBtn.addEventListener("click", () => mdInput.click());

// Captura cuando el usuario selecciona un archivo
mdInput.addEventListener("change", () => {
  const file = mdInput.files[0];
  if (!file) return;

  addMessage(`Archivo seleccionado: ${file.name}`, "user");

  // Aquí puedes enviar el archivo al backend
  const formData = new FormData();
  formData.append("file", file);

  fetch("http://127.0.0.1:8000/upload-md", {
    method: "POST",
    body: formData
  })
    .then(res => res.json())
    .then(data => addMessage(data.message || data.detail, "system"))
    .catch(err => addMessage("Error al subir el archivo 😢", "system"));
  
  // Después de subir, deshabilitamos otra vez
  uploadBtn.disabled = true;
});

// Evento de enviar chat
sendBtn.addEventListener("click", send);
input.addEventListener("keydown", (e) => {
  if (e.key === "Enter") send();
});

// Función para enviar mensajes
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

    if (data.response_html) {
      addMessageHTML(data.response_html, "system");
    }
    if (data.response) {
      addMessage(data.response, "system");
    }
    // Mostrar las opciones si el backend lo indica
    if (data.show_options) {
      addMessageHTML(`📝 Mostrando opciones ${chatOptionsHTML}`, "system");
    }

    // 🔑 Habilitar upload si backend lo indica
    if (data.enable_upload) {
      uploadBtn.disabled = false;
    }

  } catch (err) {
    addMessage("Error al conectar con el backend 😢", "system");
  }
}

// Función para añadir mensajes al chat
function addMessage(text, type) {
  const div = document.createElement("div");
  div.className = `message ${type}`;
  div.innerText = text;
  messages.appendChild(div);
  messages.scrollTop = messages.scrollHeight;
}

function addMessageHTML(html, type) {
  const div = document.createElement("div");
  div.className = `message ${type}`;
  div.innerHTML = html;
  messages.appendChild(div);
  messages.scrollTop = messages.scrollHeight;
}

addMessageHTML(
  `<p>
      <b>¡Bienvenido al chat del sistema!</b><br>
      ¿En qué puedo ayudarte hoy?
    </p>` 
    + chatOptionsHTML,
  "system-message"
);
