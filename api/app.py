from flask import Flask, request, jsonify
import firebase_admin
from firebase_admin import credentials, firestore
import os
import json
from flask_cors import CORS  # para permitir chamadas do frontend
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)  # Habilita CORS para todas as rotas

#Inicializar Firebase
firebase_config = os.getenv("FIREBASE_CREDENTIALS_JSON")
if firebase_config:
    cred_dict = json.loads(firebase_config)
    cred = credentials.Certificate("path/to/serviceAccountKey.json")
    firebase_admin.initialize_app(cred)
    db = firestore.client()
else:
    raise Exception("FIREBASE_CREDENTIALS_JSON não configurada!")


# 📥 Rota para receber o POST do formulário
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    name = data.get('name')
    email = data.get('email')

    if not name or not email:
        return jsonify({'error': 'Nome e e-mail são obrigatórios.'}), 400

    try:
        # Salva no Firebase Firestore
        db.collection('cadastros').add({
            'nome': name,
            'email': email
        })
        return jsonify({'message': 'Cadastro realizado com sucesso.'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
