from flask import Flask, request, redirect, send_file, render_template_string
import qrcode
import os
import json

app = Flask(__name__)

# Nouveau template avec téléchargement et design amélioré
template = """
<!DOCTYPE html>
<html>
<head>
    <title>QR Code Dynamique</title>
    <style>
        body { font-family: Arial, sans-serif; text-align: center; padding: 40px; background: #f9f9f9; }
        input[type=text] { width: 320px; padding: 10px; font-size: 16px; }
        button { padding: 10px 20px; font-size: 16px; margin: 10px; cursor: pointer; }
        .preview { margin-top: 20px; background: #fff; padding: 20px; display: inline-block; border-radius: 8px; box-shadow: 0 0 10px rgba(0,0,0,0.1); }
        img { margin-top: 10px; }
    </style>
</head>
<body>
    <h1>🎯 Générateur de QR Code Dynamique</h1>
    <form method="POST">
        <input type="text" name="url" placeholder="Entre l'URL ici" value="{{ current_url }}" required />
        <br>
        <button type="submit">📤 Générer le QR Code</button>
    </form>

    {% if qr_generated %}
    <div class="preview">
        <h3>✅ QR Code généré</h3>
        <p><strong>URL :</strong> {{ current_url }}</p>
        <img src="/static/mon_qr_code.png" alt="QR Code" width="200" />
        <br>
        <a href="/download_qr"><button>⬇️ Télécharger le QR Code</button></a>
    </div>
    {% endif %}
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def index():
    current_url = ""
    qr_generated = False

    if request.method == "POST":
        url = request.form.get("url")
        if url:
            with open("redirect_config.json", "w") as f:
                json.dump({"qr1": url}, f)

            img = qrcode.make(url)
            os.makedirs("static", exist_ok=True)
            img.save("static/mon_qr_code.png")
            qr_generated = True
            current_url = url
    else:
        try:
            with open("redirect_config.json", "r") as f:
                data = json.load(f)
                current_url = data.get("qr1", "")
        except:
            current_url = ""

    return render_template_string(template, current_url=current_url, qr_generated=qr_generated)

@app.route("/qr1")
def redirect_qr():
    try:
        with open("redirect_config.json", "r") as f:
            data = json.load(f)
            return redirect(data.get("qr1", "https://google.com"))
    except:
        return redirect("https://google.com")

@app.route("/download_qr")
def download_qr():
    path = "static/mon_qr_code.png"
    if os.path.exists(path):
        return send_file(path, as_attachment=True)
    return "QR code non généré."

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)


