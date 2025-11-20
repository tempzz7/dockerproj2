from flask import Flask, jsonify, request

app = Flask(__name__)

PEDIDOS = [
    {
        "id": 101,
        "id_usuario": 1,
        "produto": "Notebook Dell",
        "valor": 3500.00,
        "status": "entregue"
    },
    {
        "id": 102,
        "id_usuario": 2,
        "produto": "Mouse Gamer",
        "valor": 250.00,
        "status": "em_transporte"
    },
    {
        "id": 103,
        "id_usuario": 1,
        "produto": "Teclado Mecânico",
        "valor": 450.00,
        "status": "processando"
    },
    {
        "id": 104,
        "id_usuario": 3,
        "produto": "Monitor 27 polegadas",
        "valor": 1200.00,
        "status": "entregue"
    }
]

@app.route('/')
def inicio():
    return jsonify({
        'servico': 'Microsserviço de Pedidos',
        'versao': '1.0.0',
        'endpoints': ['/pedidos', '/pedidos/<id>', '/pedidos/usuario/<id_usuario>']
    })

@app.route('/pedidos')
def listar_pedidos():
    id_usuario = request.args.get('id_usuario', type=int)
    if id_usuario:
        pedidos_filtrados = [p for p in PEDIDOS if p['id_usuario'] == id_usuario]
        return jsonify(pedidos_filtrados)
    return jsonify(PEDIDOS)

@app.route('/pedidos/<int:id_pedido>')
def obter_pedido(id_pedido):
    pedido = next((p for p in PEDIDOS if p['id'] == id_pedido), None)
    if pedido:
        return jsonify(pedido)
    return jsonify({'erro': 'Pedido não encontrado'}), 404

@app.route('/pedidos/usuario/<int:id_usuario>')
def pedidos_por_usuario(id_usuario):
    pedidos_usuario = [p for p in PEDIDOS if p['id_usuario'] == id_usuario]
    return jsonify({
        'id_usuario': id_usuario,
        'total_pedidos': len(pedidos_usuario),
        'pedidos': pedidos_usuario
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8003)
