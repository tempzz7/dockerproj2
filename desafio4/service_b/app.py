from flask import Flask, jsonify
import requests
import os
from datetime import datetime

app = Flask(__name__)

URL_SERVICO_A = os.getenv('SERVICE_A_URL', 'http://service_a:8000')

@app.route('/')
def inicio():
    return jsonify({
        'servico': 'Microsserviço B - Agregador de Informações',
        'versao': '1.0',
        'endpoints': ['/relatorio', '/resumo']
    })

@app.route('/relatorio')
def gerar_relatorio():
    try:
        resposta = requests.get(f"{URL_SERVICO_A}/usuarios", timeout=5)
        resposta.raise_for_status()
        usuarios = resposta.json()
    except requests.exceptions.RequestException as erro:
        return jsonify({
            'erro': 'Falha ao buscar dados do serviço de usuários',
            'detalhes': str(erro)
        }), 502

    relatorio_completo = []
    ano_atual = datetime.now().year

    for usuario in usuarios:
        data_ativo = usuario.get('ativo_desde', '')
        ano_cadastro = int(data_ativo.split('-')[0]) if data_ativo else ano_atual
        tempo_ativo = ano_atual - ano_cadastro

        info = {
            'id': usuario.get('id'),
            'nome': usuario.get('nome'),
            'data_cadastro': data_ativo,
            'anos_ativo': tempo_ativo,
            'descricao': f"{usuario.get('nome')} está ativo desde {data_ativo} ({tempo_ativo} anos)"
        }
        relatorio_completo.append(info)

    return jsonify({
        'total_usuarios': len(relatorio_completo),
        'usuarios': relatorio_completo
    })

@app.route('/resumo')
def resumo_usuarios():
    try:
        resposta = requests.get(f"{URL_SERVICO_A}/usuarios", timeout=5)
        resposta.raise_for_status()
        usuarios = resposta.json()
    except requests.exceptions.RequestException:
        return jsonify({'erro': 'Serviço de usuários indisponível'}), 502

    nomes = [u.get('nome') for u in usuarios]
    return jsonify({
        'quantidade': len(usuarios),
        'nomes': nomes
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8001)
