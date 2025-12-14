from flask import Flask, request, send_file, render_template_string
import qrcode
import io

app = Flask(__name__)

HTML_PAGE = """
<!DOCTYPE html>
<html>
<head>
    <title>QR Generator</title>
</head>
<body>
    <h2>QR Code Generator</h2>
    <form action="/generate-qr" method="get">
        <input type="text" name="text" placeholder="Enter text or URL" required>
        <button type="submit">Generate QR</button>
    </form>
</body>
</html>
"""

@app.route("/")
def index():
    return render_template_string(HTML_PAGE)

@app.route("/generate-qr")
def generate_qr():
    text = request.args.get("text")
    if not text:
        return "Missing text parameter", 400

    qr = qrcode.make(text)
    img_io = io.BytesIO()
    qr.save(img_io, "PNG")
    img_io.seek(0)

    return send_file(img_io, mimetype="image/png")

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000)
