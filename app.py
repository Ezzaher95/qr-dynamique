from flask import Flask, redirect, url_for
import qrcode
import os
import json

app = Flask(__name__, static_folder='static')

CONFIG_FILE = 'redirect_config.json'

def get_redirect_url():
    with open(CONFIG_FILE, 'r') as f:
        data = json.load(f)
    return data.get("qr1", "https://default-destination.com")

@app.route("/")
def home():
    return '''
    <h2>Bienvenue dans le générateur de QR Code Dynamique !</h2>
    <p><a href="/generate_qr">Clique ici pour générer le QR code</a></p>
    '''

@app.route("/qr1")
def dynamic_redirect():
    return redirect(get_redirect_url(), code=302)

@app.route("/generate_qr")
def generate_qr():
    url = "http://localhost:5000/qr1"
    img = qrcode.make(url)

    os.makedirs("static", exist_ok=True)
    path = os.path.join("static", "mon_qr_code.png")
    img.save(path)

    return f'''
    <html>
        <head><title>QR Code</title></head>
        <body style="text-align: center; font-family: sans-serif; margin-top: 50px;">
            <h1>Voici ton QR Code</h1>
            <p>Scanne-le avec ton téléphone :</p>
            <img src="{url_for('static', filename='mon_qr_code.png')}" alt="QR Code">
            <br><br>
            <a href="/">Retour à l'accueil</a>
        </body>
    </html>
    '''

if __name__ == "__main__":
    app.run(debug=True)