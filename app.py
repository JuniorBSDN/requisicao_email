from flask import Flask, request, jsonify
import sqlite3
import smtplib
from email.mime.text import MIMEText
from flask import Flask, render_template

app = Flask(__name__)

EMAIL_ORIGEM = 'email@pessoal.corporativo.com.br'
SENHA = 'senha do app'

# Envia e-mail para o cliente após cadastro
def enviar_email(nome, email_destino):
    msg = MIMEText(f"Olá {nome}, obrigado por se cadastrar.")
    msg['Subject'] = 'Cadastro Realizado com Sucesso'
    msg['From'] = EMAIL_ORIGEM
    msg['To'] = email_destino

    with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
        smtp.starttls()
        smtp.login(EMAIL_ORIGEM, SENHA)
        smtp.send_message(msg)

# Rota de cadastro
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    nome = data.get('name')
    email = data.get('email')

    if not nome or not email:
        return jsonify({'error': 'Nome e e-mail são obrigatórios.'}), 400

    try:
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO user (name, email) VALUES (?, ?)", (nome, email))
        conn.commit()
        conn.close()

        enviar_email(nome, email)
        return jsonify({'message': 'Usuário cadastrado com sucesso.'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Rota para teste
@app.route('/')
def home():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
