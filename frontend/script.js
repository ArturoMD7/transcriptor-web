const API_URL = "https://transcriptor-web-7qx3.onrender.com/procesar";

async function enviar() {
  const fileInput = document.getElementById("fileInput");
  const loader = document.getElementById("loader");

  const pagInicio = document.getElementById("pagInicio").value;
  const pagFin = document.getElementById("pagFin").value;

  if (!fileInput.files.length) {
    alert("Selecciona un PDF");
    return;
  }

  const formData = new FormData();
  formData.append("file", fileInput.files[0]);
  formData.append("pag_inicio", pagInicio);
  formData.append("pag_fin", pagFin);

  loader.classList.remove("hidden");

  try {
    const response = await fetch(API_URL, {
      method: "POST",
      body: formData
    });

    const blob = await response.blob();
    const url = window.URL.createObjectURL(blob);

    const a = document.createElement("a");
    a.href = url;
    a.download = "resultado.docx";
    a.click();

  } catch (err) {
    alert("Error");
    console.error(err);
  }

  loader.classList.add("hidden");
}