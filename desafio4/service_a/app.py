from flask import Flask, jsonify

app = Flask(__name__)

# Simple in-memory users list
USERS = [
    {"id": 1, "name": "Alice", "ativo_desde": "2023-01-15"},
    {"id": 2, "name": "Bob", "ativo_desde": "2024-03-02"}
]

@app.route('/users')
def users():
    return jsonify(USERS)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
