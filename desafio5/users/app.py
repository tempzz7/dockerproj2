from flask import Flask, jsonify

app = Flask(__name__)

USUARIOS = [
    {
        "id": 1,
        "nome": "Ana Clara Santos",
        "email": "ana.santos@email.com",
        "cidade": "São Paulo"
    },
    {
        "id": 2,
        "nome": "Roberto Lima",
        "email": "roberto.lima@email.com",
        "cidade": "Rio de Janeiro"
    },
    {
        "id": 3,
        "nome": "Fernanda Costa",
        "email": "fernanda.costa@email.com",
        "cidade": "Belo Horizonte"
    }
]

@app.route('/')
def inicio():
    return jsonify({
        'servico': 'Microsserviço de Usuários',
        'versao': '1.0.0',
        'endpoints': ['/usuarios']
    })

@app.route('/usuarios')
def listar_usuarios():
    return jsonify(USUARIOS)

@app.route('/usuarios/<int:id_usuario>')
def obter_usuario(id_usuario):
    usuario = next((u for u in USUARIOS if u['id'] == id_usuario), None)
    if usuario:
        return jsonify(usuario)
    return jsonify({'erro': 'Usuário não encontrado'}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8002)
