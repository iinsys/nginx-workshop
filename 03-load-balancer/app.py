from flask import Flask, jsonify
import sys
import os

app = Flask(__name__)

# Get port from command line argument or use default
PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 5000
SERVER_ID = os.environ.get('SERVER_ID', f'server-{PORT}')

@app.route('/')
def home():
    return jsonify({
        'message': 'Hello from Flask Backend!',
        'server_id': SERVER_ID,
        'port': PORT,
        'status': 'running'
    })

@app.route('/api/data')
def get_data():
    return jsonify({
        'data': [1, 2, 3, 4, 5],
        'count': 5,
        'server': SERVER_ID
    })

@app.route('/api/health')
def health():
    return jsonify({
        'status': 'healthy',
        'server': SERVER_ID
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=PORT, debug=True)
