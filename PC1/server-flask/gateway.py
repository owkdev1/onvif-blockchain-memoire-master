from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

def verifier_authentification(device_info):
    """
    Vérification simulée : autorise uniquement le périphérique dont l'ID est 'authorized_device'.
    Dans une version future, cette fonction interrogerait la blockchain.
    """
    return device_info == "authorized_device"

@app.route('/', methods=['GET', 'POST'])
def gateway():
    # Extraire l'information d'identification depuis les headers de la requête
    device_info = request.headers.get('X-Device-ID', '')
    print(f"X-Device-ID reçu : {device_info}")
    
    if verifier_authentification(device_info):
        # Rediriger la requête vers le serveur HTTP de test
        camera_url = "http://localhost:8080/"
        try:
            if request.method == 'GET':
                response = requests.get(camera_url, params=request.args, timeout=5)
            else:
                response = requests.post(camera_url, data=request.form, timeout=5)
            return (response.content, response.status_code, response.headers.items())
        except Exception as e:
            return jsonify({"erreur": "Erreur lors de la redirection vers le serveur HTTP de test", "détail": str(e)}), 500
    else:
        return jsonify({"erreur": "Accès non autorisé"}), 403

if __name__ == '__main__':
    # Lancer le serveur sur le port 5000, accessible sur toutes les interfaces
    app.run(host='0.0.0.0', port=5000)