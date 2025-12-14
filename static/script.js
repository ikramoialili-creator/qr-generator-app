function generateQR() {
  const text = document.getElementById("text").value;
  if (!text) return alert("Enter text");

  document.getElementById("qr").src =
    `/generate-qr?text=${encodeURIComponent(text)}`;
}
