from flask import Flask, jsonify, request
import os
import psycopg2
import redis
import time

app = Flask(__name__)

DB_HOST = os.getenv('DATABASE_HOST', 'db')
DB_USER = os.getenv('DATABASE_USER', 'web_user')
DB_PASS = os.getenv('DATABASE_PASSWORD', 'example')
DB_NAME = os.getenv('DATABASE_NAME', 'desafio3db')
REDIS_HOST = os.getenv('REDIS_HOST', 'cache')

# retry connecting to DB on startup
def get_db_connection():
    for _ in range(10):
        try:
            conn = psycopg2.connect(host=DB_HOST, user=DB_USER, password=DB_PASS, dbname=DB_NAME)
            return conn
        except Exception as e:
            print('DB not ready, retrying...', e)
            time.sleep(1)
    raise RuntimeError('Could not connect to DB')

r = redis.Redis(host=REDIS_HOST, port=6379, db=0, decode_responses=True)

@app.route('/')
def index():
    return jsonify({'mensagem': 'Web do Desafio 3 em execução'})

@app.route('/users', methods=['GET'])
def users():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('CREATE TABLE IF NOT EXISTS pessoas (id SERIAL PRIMARY KEY, nome TEXT);')
    conn.commit()
    cur.execute('SELECT id, nome FROM pessoas;')
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify([{'id': r[0], 'nome': r[1]} for r in rows])

@app.route('/users', methods=['POST'])
def add_user():
    data = request.json or {}
    name = data.get('name')
    if not name:
        return jsonify({'erro': 'campo nome (name) é obrigatório'}), 400
    conn = get_db_connection()
    cur = conn.cursor()
    # garantir que a tabela exista antes de inserir
    cur.execute('CREATE TABLE IF NOT EXISTS pessoas (id SERIAL PRIMARY KEY, nome TEXT);')
    conn.commit()
    cur.execute('INSERT INTO pessoas (nome) VALUES (%s) RETURNING id;', (name,))
    user_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    # also cache user in redis
    r.hset('usuario:%s' % user_id, mapping={'id': user_id, 'nome': name})
    return jsonify({'id': user_id, 'nome': name}), 201

@app.route('/cache/<key>')
def get_cache(key):
    value = r.get(key)
    return jsonify({'chave': key, 'valor': value})

@app.route('/cache', methods=['POST'])
def set_cache():
    data = request.json or {}
    key = data.get('key')
    val = data.get('value')
    if not key:
        return jsonify({'erro': 'campo key obrigatório'}), 400
    r.set(key, val)
    return jsonify({'chave': key, 'valor': val}), 201

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
