from flask import Flask, jsonify, request
import time
import random

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({
        'message': 'Hello from Flask Backend!',
        'timestamp': time.time(),
        'uncached': 'This response is not cached'
    })

@app.route('/api/data')
def get_data():
    # Simulate some processing time
    time.sleep(0.1)
    return jsonify({
        'data': [1, 2, 3, 4, 5],
        'count': 5,
        'timestamp': time.time(),
        'random': random.randint(1, 1000)
    })

@app.route('/api/static')
def get_static():
    return jsonify({
        'message': 'This content rarely changes',
        'version': '1.0.0',
        'timestamp': time.time()
    })

@app.route('/api/uncached')
def get_uncached():
    return jsonify({
        'message': 'This should never be cached',
        'timestamp': time.time(),
        'random': random.randint(1, 10000)
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
