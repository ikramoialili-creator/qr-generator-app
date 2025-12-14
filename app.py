from flask import Flask, request, jsonify, send_from_directory
import qrcode
import os
from datetime import datetime
from azure.storage.blob import BlobServiceClient

app = Flask(__name__, static_folder="static")

@app.route("/")
def home():
    return send_from_directory("static", "index.html")

@app.route("/generate-qr")
def generate_qr():
    text = request.args.get("text")

    if not text:
        return jsonify({"error": "Text parameter is required"}), 400

    filename = f"qr_{datetime.utcnow().strftime('%Y%m%d%H%M%S')}.png"
    file_path = os.path.join("/tmp", filename)

    # Générer QR
    img = qrcode.make(text)
    img.save(file_path)

    # Connexion Blob Storage
    connect_str = os.environ.get("AZURE_STORAGE_CONNECTION_STRING")
    container_name = os.environ.get("BLOB_CONTAINER_NAME")

    blob_service_client = BlobServiceClient.from_connection_string(connect_str)
    blob_client = blob_service_client.get_blob_client(
        container=container_name,
        blob=filename
    )

    # Upload vers Blob
    with open(file_path, "rb") as data:
        blob_client.upload_blob(data, overwrite=True)

    blob_url = blob_client.url

    return jsonify({
        "message": "QR Code generated",
        "url": blob_url
    })
