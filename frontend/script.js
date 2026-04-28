async function enviar() {
    const fileInput = document.getElementById("fileInput");
    const status = document.getElementById("status");

    if (!fileInput.files.length) {
        alert("Selecciona un PDF");
        return;
    }

    const formData = new FormData();
    formData.append("file", fileInput.files[0]);

    status.innerText = "Procesando...";

    const response = await fetch("https://TU_BACKEND.onrender.com/procesar", {
        method: "POST",
        body: formData
    });

    const blob = await response.blob();
    const url = window.URL.createObjectURL(blob);

    const a = document.createElement("a");
    a.href = url;
    a.download = "resultado.docx";
    a.click();

    status.innerText = "Listo ✅";
}