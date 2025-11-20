from flask import Flask, jsonify

app = Flask(__name__)

USUARIOS = [
    {"id": 1, "nome": "Alice Martins", "ativo_desde": "2023-01-15"},
    {"id": 2, "nome": "Bruno Costa", "ativo_desde": "2024-03-02"},
    {"id": 3, "nome": "Carla Souza", "ativo_desde": "2023-08-20"}
]

@app.route('/')
def inicio():
    return jsonify({
        'servico': 'Microsserviço A - Gerenciamento de Usuários',
        'versao': '1.0',
        'endpoints': ['/usuarios']
    })

@app.route('/usuarios')
def listar_usuarios():
    return jsonify(USUARIOS)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
