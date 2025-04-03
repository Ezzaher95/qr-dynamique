from flask import Flask, request, redirect, send_file, render_template_string
import qrcode
import os
import json

app = Flask(__name__)

# Template HTML avec bouton télécharger et supprimer
template = """
<!DOCTYPE html>
<html>
<head>
    <title>QR Code Manager</title>
    <style>
        body { font-family: Arial, sans-serif; padding: 40px; background: #f5f5f5; }
        h1 { text-align: center; }
        form { margin: auto; width: 100%; max-width: 500px; background: #fff; padding: 20px; border-radius: 8px; box-shadow: 0 2px 6px rgba(0,0,0,0.1); }
        input[type=text], input[type=submit] { width: 100%; padding: 10px; margin: 8px 0; font-size: 16px; }
        .qr-section { display: flex; flex-wrap: wrap; gap: 20px; justify-content: center; margin-top: 40px; }
        .qr-box { background: #fff; padding: 15px; border-radius: 6px; box-shadow: 0 1px 4px rgba(0,0,0,0.1); text-align: center; width: 240px; }
        img { max-width: 100%; height: auto; }
        .edit-form { margin-top: 10px; }
        .actions a, .actions form { display: inline-block; margin: 4px; }
    </style>
</head>
<body>
    <h1>🎯 Gestionnaire de QR Codes Dynamiques</h1>
    <form method="POST">
        <input type="text" name="id" placeholder="ID du QR (ex: qr1, qr2...)" required>
        <input type="text" name="url" placeholder="Lien de redirection" required>
        <input type="submit" value="📤 Générer le QR Code">
    </form>

    <div class="qr-section">
        {% for key, link in links.items() %}
        <div class="qr-box">
            <p><strong>{{ key }}</strong></p>
            <img src="/static/{{ key }}.png" alt="QR {{ key }}">
            <form method="POST" class="edit-form">
                <input type="hidden" name="id" value="{{ key }}">
                <input type="text" name="url" value="{{ link }}">
                <input type="submit" value="🔄 Modifier">
            </form>
            <div class="actions">
                <a href="/qr/{{ key }}" target="_blank">🔗 Test</a>
                <a href="/download/{{ key }}">⬇️ Télécharger</a>
                <form method="POST" action="/delete/{{ key }}" style="display:inline">
                    <button type="submit">🗑️ Supprimer</button>
                </form>
            </div>
        </div>
        {% endfor %}
    </div>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def index():
    links = {}
    try:
        with open("redirect_config.json", "r") as f:
            links = json.load(f)
    except:
        links = {}

    if request.method == "POST":
        qr_id = request.form.get("id")
        url = request.form.get("url")
        if qr_id and url:
            links[qr_id] = url
            with open("redirect_config.json", "w") as f:
                json.dump(links, f, indent=2)
            os.makedirs("static", exist_ok=True)
            img = qrcode.make(url)
            img.save(f"static/{qr_id}.png")

    return render_template_string(template, links=links)

@app.route("/qr/<qr_id>")
def redirect_qr(qr_id):
    try:
        with open("redirect_config.json", "r") as f:
            data = json.load(f)
            return redirect(data.get(qr_id, "https://google.com"))
    except:
        return redirect("https://google.com")

@app.route("/download/<qr_id>")
def download_qr(qr_id):
    path = f"static/{qr_id}.png"
    if os.path.exists(path):
        return send_file(path, as_attachment=True)
    return "QR code non trouvé."

@app.route("/delete/<qr_id>", methods=["POST"])
def delete_qr(qr_id):
    try:
        # Supprimer du JSON
        with open("redirect_config.json", "r") as f:
            data = json.load(f)
        data.pop(qr_id, None)
        with open("redirect_config.json", "w") as f:
            json.dump(data, f, indent=2)
        # Supprimer le fichier image
        img_path = f"static/{qr_id}.png"
        if os.path.exists(img_path):
            os.remove(img_path)
    except:
        pass
    return redirect("/")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
