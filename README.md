# QR Code Dynamique (Version finale)

Projet Flask permettant de générer un QR code dynamique, modifiable sans changer le code QR.

## Installation

1. Ouvrir le terminal
2. Se placer dans le dossier : cd ~/Downloads/qr_dynamique_final
3. Installer les dépendances : pip3 install -r requirements.txt
4. Lancer le projet : python3 app.py
5. Ouvrir : http://localhost:5000/generate_qr

## Modifier le lien

Éditez le fichier `redirect_config.json` pour changer la redirection :
{
  "qr1": "https://google.com"
}