from flask import Flask, jsonify, request
import os
import psycopg2
import redis
import time

app = Flask(__name__)

HOST_BANCO = os.getenv('DATABASE_HOST', 'db')
USUARIO_BANCO = os.getenv('DATABASE_USER', 'web_user')
SENHA_BANCO = os.getenv('DATABASE_PASSWORD', 'example')
NOME_BANCO = os.getenv('DATABASE_NAME', 'desafio3db')
HOST_REDIS = os.getenv('REDIS_HOST', 'cache')

def conectar_banco():
    tentativas = 0
    while tentativas < 10:
        try:
            conexao = psycopg2.connect(
                host=HOST_BANCO,
                user=USUARIO_BANCO,
                password=SENHA_BANCO,
                dbname=NOME_BANCO
            )
            return conexao
        except Exception as erro:
            tentativas += 1
            print(f'Aguardando banco de dados... tentativa {tentativas}')
            time.sleep(1)
    raise RuntimeError('Não foi possível conectar ao banco de dados')

cache = redis.Redis(host=HOST_REDIS, port=6379, db=0, decode_responses=True)

@app.route('/')
def index():
    return jsonify({'mensagem': 'Web do Desafio 3 em execução'})

@app.route('/usuarios', methods=['GET'])
def listar_usuarios():
    conn = conectar_banco()
    cursor = conn.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS pessoas (id SERIAL PRIMARY KEY, nome TEXT);')
    conn.commit()
    cursor.execute('SELECT id, nome FROM pessoas;')
    linhas = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify([{'id': linha[0], 'nome': linha[1]} for linha in linhas])

@app.route('/usuarios', methods=['POST'])
def adicionar_usuario():
    dados = request.json or {}
    nome = dados.get('nome')
    if not nome:
        return jsonify({'erro': 'campo nome é obrigatório'}), 400
    conn = conectar_banco()
    cursor = conn.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS pessoas (id SERIAL PRIMARY KEY, nome TEXT);')
    conn.commit()
    cursor.execute('INSERT INTO pessoas (nome) VALUES (%s) RETURNING id;', (nome,))
    id_usuario = cursor.fetchone()[0]
    conn.commit()
    cursor.close()
    conn.close()
    cache.hset(f'usuario:{id_usuario}', mapping={'id': id_usuario, 'nome': nome})
    return jsonify({'id': id_usuario, 'nome': nome}), 201

@app.route('/cache/<chave>')
def consultar_cache(chave):
    valor = cache.get(chave)
    return jsonify({'chave': chave, 'valor': valor})

@app.route('/cache', methods=['POST'])
def gravar_cache():
    dados = request.json or {}
    chave = dados.get('chave')
    valor = dados.get('valor')
    if not chave:
        return jsonify({'erro': 'campo chave é obrigatório'}), 400
    cache.set(chave, valor)
    return jsonify({'chave': chave, 'valor': valor}), 201

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
