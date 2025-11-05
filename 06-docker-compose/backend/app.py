from flask import Flask, jsonify
import os
import socket

app = Flask(__name__)
HOSTNAME = socket.gethostname()
PORT = int(os.environ.get('PORT', 5000))

@app.route('/')
def home():
    return jsonify({
        'message': 'Hello from Flask Backend!',
        'hostname': HOSTNAME,
        'port': PORT,
        'status': 'running'
    })

@app.route('/api/data')
def get_data():
    return jsonify({
        'data': [1, 2, 3, 4, 5],
        'count': 5,
        'server': HOSTNAME
    })

@app.route('/api/health')
def health():
    return jsonify({
        'status': 'healthy',
        'server': HOSTNAME
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=PORT, debug=True)
