from flask import Flask, request, jsonify
import firebase_admin
from firebase_admin import credentials, firestore
from flask_cors import CORS
import json, os


app = Flask(__name__)
CORS(app)

# Inicializa Firebase
cred_dict = json.loads(os.environ["FIREBASE_CREDENTIALS_JSON"])
cred = credentials.Certificate(cred_dict)
firebase_admin.initialize_app(cred)
db = firestore.client()

@app.route("/")
def home():
    return jsonify({"mensagem": "API online!"})

@app.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    nome = data.get("name")
    email = data.get("email")

    if not nome or not email:
        return jsonify({"error": "Nome e email são obrigatórios."}), 400

    try:
        db.collection("usuarios").add({"nome": nome, "email": email})
        return jsonify({"mensagem": "Cadastro realizado com sucesso!"}), 200
    except Exception as e:
        return jsonify({"error": f"Erro ao salvar no banco: {str(e)}"}), 500
