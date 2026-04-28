async function enviar() {
  const btn = document.getElementById("btnProcesar");
  const loader = document.getElementById("loader");
  const status = document.getElementById("status");
  const fileInput = document.getElementById("fileInput");

  const pagInicio = document.getElementById("pagInicio").value;
  const pagFin = document.getElementById("pagFin").value;

  if (!fileInput.files.length) {
    alert("Selecciona un PDF");
    return;
  }

  btn.disabled = true;
  loader.classList.remove("hidden");
  status.innerText = "Procesando documento...";

  const formData = new FormData();
  formData.append("file", fileInput.files[0]);
  formData.append("pag_inicio", pagInicio);
  formData.append("pag_fin", pagFin);

  try {
    const response = await fetch("/procesar", {
      method: "POST",
      body: formData
    });

    if (!response.ok) throw new Error();

    const blob = await response.blob();
    const url = window.URL.createObjectURL(blob);

    const a = document.createElement("a");
    a.href = url;
    a.download = "resultado.docx";
    a.click();

    status.innerText = "✅ Documento listo";
  } catch {
    status.innerText = "❌ Error al procesar";
  }

  loader.classList.add("hidden");
  btn.disabled = false;
}