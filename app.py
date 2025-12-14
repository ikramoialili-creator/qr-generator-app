from flask import Flask, request, jsonify
import qrcode
import os
from datetime import datetime

app = Flask(__name__)

@app.route("/")
def home():
    return "QR Generator API is running"

@app.route("/generate-qr", methods=["GET"])
def generate_qr():
    text = request.args.get("text")

    if not text:
        return jsonify({"error": "Missing text parameter"}), 400

    filename = f"qr_{datetime.now().strftime('%Y%m%d%H%M%S')}.png"
    filepath = os.path.join("/tmp", filename)

    img = qrcode.make(text)
    img.save(filepath)

    return jsonify({
        "message": "QR Code generated",
        "file": filename
    })
