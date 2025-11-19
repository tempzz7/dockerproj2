from flask import Flask, jsonify, request
import requests
import os

app = Flask(__name__)

USERS_URL = os.getenv('USERS_URL', 'http://users:8002')
ORDERS_URL = os.getenv('ORDERS_URL', 'http://orders:8003')

@app.route('/users')
def gateway_users():
    resp = requests.get(f"{USERS_URL}/users")
    return (resp.content, resp.status_code, resp.headers.items())

@app.route('/orders')
def gateway_orders():
    resp = requests.get(f"{ORDERS_URL}/orders")
    return (resp.content, resp.status_code, resp.headers.items())

@app.route('/')
def index():
    return jsonify({'message': 'API Gateway running', 'routes': ['/users', '/orders']})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
