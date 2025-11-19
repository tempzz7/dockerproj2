from flask import Flask, jsonify, request
import datetime

app = Flask(__name__)

@app.route('/')
def index():
    agora = datetime.datetime.utcnow().isoformat() + "Z"
    return jsonify({
        "mensagem": "Servidor do Desafio 1 respondendo",
        "horario": agora,
        "ip_cliente": request.remote_addr
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
