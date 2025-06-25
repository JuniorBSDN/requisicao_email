import firebase_admin
from firebase_admin import credentials, firestore
from flask import Flask, request, jsonify, render_template
import smtplib
from email.mime.text import MIMEText
import os
import firebase_admin
from firebase_admin import credentials

app = Flask(__name__)

# Inicializar Firebase com credencial
cred = credentials.Certificate("path/to/serviceAccountKey.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

# CONFIGURANDO O GMAIL PARA ENVIO AUTOMATICO
#EMAIL_ORIGEM = 'seuemail@gmail.com'
#SENHA = 'sua_senha_de_app'
#def enviar_email(nome, email_destino):
 #   msg = MIMEText(f"Olá {nome}, obrigado por se cadastrar.")
  #  msg['Subject'] = 'Cadastro Realizado'
   # msg['From'] = EMAIL_ORIGEM
    #msg['To'] = email_destino
    #with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
     #   smtp.starttls()
      #  smtp.login(EMAIL_ORIGEM, SENHA)
       # smtp.send_message(msg)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')

    if not name or not email:
        return jsonify({'error': 'Nome e e-mail obrigatórios'}), 400

    try:
        doc_ref = db.collection('users').add({
            'name': name,
            'email': email
        })
        enviar_email(name, email)
        return jsonify({'message': 'Usuário salvo com sucesso'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
