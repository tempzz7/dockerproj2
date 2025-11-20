from flask import Flask, jsonify, request
import requests
import os
from datetime import datetime

app = Flask(__name__)

URL_SERVICO_USUARIOS = os.getenv('USERS_URL', 'http://users:8002')
URL_SERVICO_PEDIDOS = os.getenv('ORDERS_URL', 'http://orders:8003')

@app.route('/')
def inicio():
    return jsonify({
        'gateway': 'API Gateway - Desafio 5',
        'versao': '1.0.0',
        'status': 'online',
        'rotas_disponiveis': {
            '/usuarios': 'Lista todos os usuários',
            '/usuarios/<id>': 'Detalhes de um usuário',
            '/pedidos': 'Lista todos os pedidos',
            '/pedidos/<id>': 'Detalhes de um pedido',
            '/pedidos/usuario/<id>': 'Pedidos de um usuário específico',
            '/relatorio/<id>': 'Relatório completo: usuário + pedidos'
        }
    })

@app.route('/usuarios')
def gateway_usuarios():
    try:
        resposta = requests.get(f"{URL_SERVICO_USUARIOS}/usuarios", timeout=5)
        return (resposta.content, resposta.status_code, resposta.headers.items())
    except requests.exceptions.RequestException as erro:
        return jsonify({
            'erro': 'Serviço de usuários indisponível',
            'detalhes': str(erro)
        }), 503

@app.route('/usuarios/<int:id_usuario>')
def gateway_usuario_detalhe(id_usuario):
    try:
        resposta = requests.get(f"{URL_SERVICO_USUARIOS}/usuarios/{id_usuario}", timeout=5)
        return (resposta.content, resposta.status_code, resposta.headers.items())
    except requests.exceptions.RequestException:
        return jsonify({'erro': 'Serviço de usuários indisponível'}), 503

@app.route('/pedidos')
def gateway_pedidos():
    try:
        id_usuario = request.args.get('id_usuario')
        url = f"{URL_SERVICO_PEDIDOS}/pedidos"
        if id_usuario:
            url += f"?id_usuario={id_usuario}"
        resposta = requests.get(url, timeout=5)
        return (resposta.content, resposta.status_code, resposta.headers.items())
    except requests.exceptions.RequestException:
        return jsonify({'erro': 'Serviço de pedidos indisponível'}), 503

@app.route('/pedidos/<int:id_pedido>')
def gateway_pedido_detalhe(id_pedido):
    try:
        resposta = requests.get(f"{URL_SERVICO_PEDIDOS}/pedidos/{id_pedido}", timeout=5)
        return (resposta.content, resposta.status_code, resposta.headers.items())
    except requests.exceptions.RequestException:
        return jsonify({'erro': 'Serviço de pedidos indisponível'}), 503

@app.route('/pedidos/usuario/<int:id_usuario>')
def gateway_pedidos_usuario(id_usuario):
    try:
        resposta = requests.get(f"{URL_SERVICO_PEDIDOS}/pedidos/usuario/{id_usuario}", timeout=5)
        return (resposta.content, resposta.status_code, resposta.headers.items())
    except requests.exceptions.RequestException:
        return jsonify({'erro': 'Serviço de pedidos indisponível'}), 503

@app.route('/relatorio/<int:id_usuario>')
def relatorio_completo(id_usuario):
    try:
        resp_usuario = requests.get(f"{URL_SERVICO_USUARIOS}/usuarios/{id_usuario}", timeout=5)
        resp_pedidos = requests.get(f"{URL_SERVICO_PEDIDOS}/pedidos/usuario/{id_usuario}", timeout=5)

        if resp_usuario.status_code != 200:
            return jsonify({'erro': 'Usuário não encontrado'}), 404

        usuario = resp_usuario.json()
        dados_pedidos = resp_pedidos.json()

        total_gasto = sum(p['valor'] for p in dados_pedidos.get('pedidos', []))

        return jsonify({
            'usuario': usuario,
            'estatisticas_pedidos': {
                'total_pedidos': dados_pedidos.get('total_pedidos', 0),
                'valor_total': total_gasto
            },
            'pedidos': dados_pedidos.get('pedidos', []),
            'gerado_em': datetime.now().isoformat()
        })
    except requests.exceptions.RequestException as erro:
        return jsonify({
            'erro': 'Falha ao gerar relatório',
            'detalhes': str(erro)
        }), 503

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
