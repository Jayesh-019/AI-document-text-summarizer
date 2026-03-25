const API_BASE = "http://127.0.0.1:8000";

const textInput = document.getElementById("textInput");
const textButton = document.getElementById("textButton");
const fileInput = document.getElementById("fileInput");
const fileButton = document.getElementById("fileButton");
const result = document.getElementById("result");

async function summarizeText() {
  const text = textInput.value.trim();

  if (!text) {
    result.textContent = "Please enter some text.";
    return;
  }

  result.textContent = "Summarizing...";

  const response = await fetch(`${API_BASE}/summarize-text`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ text }),
  });

  const data = await response.json();
  result.textContent = data.summary || data.detail || "Something went wrong.";
}

async function summarizeFile() {
  const file = fileInput.files[0];

  if (!file) {
    result.textContent = "Please choose a TXT or PDF file.";
    return;
  }

  result.textContent = "Summarizing file...";

  const formData = new FormData();
  formData.append("file", file);

  const response = await fetch(`${API_BASE}/summarize-file`, {
    method: "POST",
    body: formData,
  });

  const data = await response.json();
  result.textContent = data.summary || data.detail || "Something went wrong.";
}

textButton.addEventListener("click", summarizeText);
fileButton.addEventListener("click", summarizeFile);
