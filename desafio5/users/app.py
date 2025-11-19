from flask import Flask, jsonify

app = Flask(__name__)

USERS = [
    {"id": 1, "name": "Alice"},
    {"id": 2, "name": "Bob"}
]

@app.route('/users')
def users():
    # Retorna lista de usuários em português
    return jsonify({ 'usuarios': USERS })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8002)
