# Topic 2: nginx as Reverse Proxy

This section demonstrates how to configure nginx as a reverse proxy to forward requests to a backend application.

## Learning Objectives

- Understand reverse proxy concept
- Configure nginx to proxy requests to backend services
- Set up a Python Flask application as backend
- Handle different URL paths and routing

## Prerequisites

- Python 3.x installed
- pip package manager
- Flask installed

## Installation

### Install nginx
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install nginx -y
```

### Install Python Dependencies
```bash
pip3 install flask
```

## Backend Application

1. Create a directory for the backend:
```bash
mkdir -p ~/nginx-demo/reverse-proxy
cd ~/nginx-demo/reverse-proxy
```

2. Create the Flask application:
```bash
cat > app.py << 'EOF'
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({
        'message': 'Hello from Flask Backend!',
        'server': 'Flask Application',
        'status': 'running'
    })

@app.route('/api/data')
def get_data():
    return jsonify({
        'data': [1, 2, 3, 4, 5],
        'count': 5
    })

@app.route('/api/health')
def health():
    return jsonify({'status': 'healthy'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
EOF
```

3. Start the Flask application:
```bash
python3 app.py
```

The Flask app will run on `http://localhost:5000`. Keep this terminal open.

## nginx Configuration

1. Create nginx configuration:
```bash
sudo nano /etc/nginx/sites-available/reverse-proxy-demo
```

Add the following configuration:
```nginx
server {
    listen 8080;
    server_name localhost;

    # Proxy all requests to Flask backend
    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # Specific API endpoint
    location /api/ {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
```

2. Enable the site:
```bash
sudo ln -s /etc/nginx/sites-available/reverse-proxy-demo /etc/nginx/sites-enabled/
```

3. Test and reload nginx:
```bash
sudo nginx -t
sudo nginx -s reload
```

## Testing

1. Test the Flask backend directly:
```bash
curl http://localhost:5000
```

2. Test through nginx reverse proxy:
```bash
curl http://localhost:8080
curl http://localhost:8080/api/data
curl http://localhost:8080/api/health
```

You should see the same responses, but now coming through nginx.

## Understanding the Configuration

- `proxy_pass`: Forwards requests to the specified backend server
- `proxy_set_header`: Sets HTTP headers that backend needs
  - `Host`: Original host header
  - `X-Real-IP`: Client's real IP address
  - `X-Forwarded-For`: Chain of proxy IPs
  - `X-Forwarded-Proto`: Original protocol (http/https)

## Frontend + Backend Example

1. Stop the current Flask app (Ctrl+C)

2. Create a simple HTML frontend:
```bash
mkdir -p ~/nginx-demo/reverse-proxy/static
cat > ~/nginx-demo/reverse-proxy/static/index.html << 'EOF'
<!DOCTYPE html>
<html>
<head>
    <title>nginx Reverse Proxy Demo</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 900px;
            margin: 50px auto;
            padding: 20px;
            background-color: #f4f4f4;
        }
        .container {
            background-color: white;
            padding: 30px;
            border-radius: 5px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }
        button {
            background-color: #007bff;
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 4px;
            cursor: pointer;
            margin: 10px 5px;
        }
        button:hover {
            background-color: #0056b3;
        }
        #result {
            margin-top: 20px;
            padding: 15px;
            background-color: #f8f9fa;
            border-radius: 4px;
            white-space: pre-wrap;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>nginx Reverse Proxy Demo</h1>
        <p>This frontend is served by nginx, API calls are proxied to Flask backend.</p>
        
        <button onclick="fetchAPI('/')">Get Home</button>
        <button onclick="fetchAPI('/api/data')">Get Data</button>
        <button onclick="fetchAPI('/api/health')">Check Health</button>
        
        <div id="result"></div>
    </div>

    <script>
        async function fetchAPI(endpoint) {
            try {
                const response = await fetch(endpoint);
                const data = await response.json();
                document.getElementById('result').textContent = JSON.stringify(data, null, 2);
            } catch (error) {
                document.getElementById('result').textContent = 'Error: ' + error.message;
            }
        }
    </script>
</body>
</html>
EOF
```

3. Update nginx configuration to serve static files and proxy API:
```nginx
server {
    listen 8080;
    server_name localhost;

    # Serve static files from frontend
    location / {
        root /home/YOUR_USERNAME/nginx-demo/reverse-proxy/static;
        index index.html;
        try_files $uri $uri/ =404;
    }

    # Proxy API requests to Flask backend
    location /api/ {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

4. Restart Flask app:
```bash
cd ~/nginx-demo/reverse-proxy
python3 app.py
```

5. Reload nginx:
```bash
sudo nginx -s reload
```

6. Open browser: `http://localhost:8080`

## Benefits of Reverse Proxy

- Single entry point for clients
- Hide backend server details
- Load balancing capability
- SSL termination
- Request/response manipulation
- Caching

## Cleanup

```bash
# Stop Flask app (Ctrl+C)
sudo rm /etc/nginx/sites-enabled/reverse-proxy-demo
sudo nginx -s reload
```
