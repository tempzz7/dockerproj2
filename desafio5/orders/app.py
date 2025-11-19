from flask import Flask, jsonify

app = Flask(__name__)

ORDERS = [
    {"id": 101, "user_id": 1, "item": "Book"},
    {"id": 102, "user_id": 2, "item": "Keyboard"}
]

@app.route('/orders')
def orders():
    return jsonify(ORDERS)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8003)
