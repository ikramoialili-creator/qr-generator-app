from flask import Flask, request, jsonify
import qrcode
import os
CONNECTION_STRING = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
import uuid
from azure.storage.blob import BlobServiceClient

app = Flask(__name__)

# 🔐 Azure Blob Storage config
CONNECTION_STRING = "PASTE_YOUR_CONNECTION_STRING_HERE"
CONTAINER_NAME = "qrcodes"

blob_service_client = BlobServiceClient.from_connection_string(CONNECTION_STRING)
container_client = blob_service_client.get_container_client(CONTAINER_NAME)

@app.route("/generate-qr")
def generate_qr():
    text = request.args.get("text")

    if not text:
        return jsonify({"error": "Text parameter is required"}), 400

    # Générer QR
    qr = qrcode.make(text)
    img_bytes = io.BytesIO()
    qr.save(img_bytes, format="PNG")
    img_bytes.seek(0)

    # Nom unique
    filename = f"{uuid.uuid4()}.png"

    # Upload Blob
    blob_client = container_client.get_blob_client(filename)
    blob_client.upload_blob(img_bytes, overwrite=True)

    # URL publique
    blob_url = blob_client.url

    return jsonify({
        "message": "QR Code generated",
        "url": blob_url
    })
