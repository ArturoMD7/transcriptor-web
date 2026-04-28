document.getElementById("fileInput").addEventListener("change", function(e) {
  const fileNameDisplay = document.getElementById("fileName");
  const fileLabel = document.querySelector(".file-label");
  
  if (e.target.files.length > 0) {
    fileNameDisplay.textContent = e.target.files[0].name;
    fileLabel.classList.add("active");
  } else {
    fileNameDisplay.textContent = "Seleccionar archivo PDF";
    fileLabel.classList.remove("active");
  }
});

async function enviar() {
  const btn = document.getElementById("btnProcesar");
  const statusContainer = document.getElementById("statusContainer");
  const loader = document.getElementById("loader");
  const status = document.getElementById("status");
  const fileInput = document.getElementById("fileInput");

  const pagInicio = document.getElementById("pagInicio").value;
  const pagFin = document.getElementById("pagFin").value;

  if (!fileInput.files.length) {
    alert("Por favor, selecciona un documento PDF.");
    return;
  }

  // Reset classes
  statusContainer.className = "status-container";
  loader.className = "loader";
  
  btn.disabled = true;
  status.innerText = "Procesando documento... (Esto puede tardar)";

  const formData = new FormData();
  formData.append("file", fileInput.files[0]);
  formData.append("pag_inicio", pagInicio || 1);
  if (pagFin) formData.append("pag_fin", pagFin);

  try {
    const response = await fetch("/procesar", {
      method: "POST",
      body: formData
    });

    if (!response.ok) {
      const err = await response.json().catch(() => ({}));
      throw new Error(err.detail || "Error al procesar el documento");
    }

    const blob = await response.blob();
    const url = window.URL.createObjectURL(blob);

    const a = document.createElement("a");
    a.href = url;
    a.download = fileInput.files[0].name.replace(".pdf", "_corregido.docx");
    a.click();

    statusContainer.classList.add("success");
    loader.classList.add("hidden");
    status.innerText = "✅ Documento descargado con éxito.";
  } catch (error) {
    statusContainer.classList.add("error");
    loader.classList.add("hidden");
    status.innerText = "❌ " + error.message;
  }

  btn.disabled = false;
}