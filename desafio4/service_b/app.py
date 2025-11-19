from flask import Flask, jsonify
import requests
import os

app = Flask(__name__)

SERVICE_A_URL = os.getenv('SERVICE_A_URL', 'http://service_a:8000')

@app.route('/')
def index():
    return jsonify({'message': 'Service B (consumer) running'})

@app.route('/combined')
def combined():
    try:
        resp = requests.get(f"{SERVICE_A_URL}/users", timeout=5)
        resp.raise_for_status()
        users = resp.json()
    except Exception as e:
        return jsonify({'error': 'failed to fetch users', 'details': str(e)}), 502

    # enriquecer usuários com uma frase amigável (em PT-BR)
    enriquecidos = []
    for u in users:
        ativo = u.get('ativo_desde') or u.get('joined')
        texto = f"Usuário {u.get('name')} ativo desde {ativo}"
        enriquecidos.append({'id': u.get('id'), 'nome': u.get('name'), 'texto': texto})

    return jsonify(enriquecidos)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8001)
