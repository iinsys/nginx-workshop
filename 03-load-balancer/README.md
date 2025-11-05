# Topic 3: nginx as Load Balancer

This section demonstrates how to configure nginx as a load balancer to distribute traffic across multiple backend instances.

## Learning Objectives

- Understand load balancing concepts
- Configure nginx upstream blocks
- Implement different load balancing algorithms
- Run multiple instances of the same application
- Monitor request distribution

## Prerequisites

- Python 3.x and Flask installed
- Basic understanding of reverse proxy (Topic 2)

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

## Backend Application Setup

1. Create directory for the load balancer demo:
```bash
mkdir -p ~/nginx-demo/load-balancer
cd ~/nginx-demo/load-balancer
```

2. Create the Flask application with server identification:
```bash
cat > app.py << 'EOF'
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
EOF
```

## Running Multiple Backend Instances

Open three separate terminal windows and run:

**Terminal 1:**
```bash
cd ~/nginx-demo/load-balancer
SERVER_ID=server-1 python3 app.py 5001
```

**Terminal 2:**
```bash
cd ~/nginx-demo/load-balancer
SERVER_ID=server-2 python3 app.py 5002
```

**Terminal 3:**
```bash
cd ~/nginx-demo/load-balancer
SERVER_ID=server-3 python3 app.py 5003
```

Verify all three are running:
```bash
curl http://localhost:5001
curl http://localhost:5002
curl http://localhost:5003
```

## nginx Load Balancer Configuration

1. Create nginx configuration:
```bash
sudo nano /etc/nginx/sites-available/load-balancer-demo
```

Add the following configuration:
```nginx
# Define upstream backend servers
upstream backend_servers {
    # Default load balancing method is round-robin
    server 127.0.0.1:5001;
    server 127.0.0.1:5002;
    server 127.0.0.1:5003;
}

server {
    listen 8080;
    server_name localhost;

    location / {
        proxy_pass http://backend_servers;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /api/ {
        proxy_pass http://backend_servers;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
```

2. Enable the site:
```bash
sudo ln -s /etc/nginx/sites-available/load-balancer-demo /etc/nginx/sites-enabled/
```

3. Test and reload nginx:
```bash
sudo nginx -t
sudo nginx -s reload
```

## Testing Load Balancing

Test the load balancer:
```bash
# Make multiple requests and observe different server responses
for i in {1..10}; do
    echo "Request $i:"
    curl -s http://localhost:8080 | grep server_id
    sleep 0.5
done
```

You should see requests being distributed across server-1, server-2, and server-3.

## Load Balancing Methods

### 1. Round Robin (Default)
Requests are distributed evenly across servers in order.
```nginx
upstream backend_servers {
    server 127.0.0.1:5001;
    server 127.0.0.1:5002;
    server 127.0.0.1:5003;
}
```

### 2. Least Connections
Sends requests to server with fewest active connections.
```nginx
upstream backend_servers {
    least_conn;
    server 127.0.0.1:5001;
    server 127.0.0.1:5002;
    server 127.0.0.1:5003;
}
```

### 3. IP Hash
Distributes requests based on client IP, ensuring same client goes to same server.
```nginx
upstream backend_servers {
    ip_hash;
    server 127.0.0.1:5001;
    server 127.0.0.1:5002;
    server 127.0.0.1:5003;
}
```

### 4. Weighted Round Robin
Assign different weights to servers.
```nginx
upstream backend_servers {
    server 127.0.0.1:5001 weight=3;
    server 127.0.0.1:5002 weight=2;
    server 127.0.0.1:5003 weight=1;
}
```

### 5. Backup Server
Mark a server as backup (used only if others are down).
```nginx
upstream backend_servers {
    server 127.0.0.1:5001;
    server 127.0.0.1:5002;
    server 127.0.0.1:5003 backup;
}
```

### 6. Health Checks (Advanced)
Mark server as down if it fails.
```nginx
upstream backend_servers {
    server 127.0.0.1:5001 max_fails=3 fail_timeout=30s;
    server 127.0.0.1:5002 max_fails=3 fail_timeout=30s;
    server 127.0.0.1:5003 max_fails=3 fail_timeout=30s;
}
```

## Testing Failover

1. Stop one backend server (Ctrl+C in one terminal)
2. Continue making requests:
```bash
curl http://localhost:8080
```
3. nginx will automatically skip the down server
4. Restart the stopped server and it will be included again

## Frontend Demo

Create a simple HTML page to visualize load balancing:

```bash
mkdir -p ~/nginx-demo/load-balancer/static
cat > ~/nginx-demo/load-balancer/static/index.html << 'EOF'
<!DOCTYPE html>
<html>
<head>
    <title>nginx Load Balancer Demo</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 1000px;
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
            background-color: #28a745;
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 4px;
            cursor: pointer;
            margin: 10px 5px;
        }
        button:hover {
            background-color: #218838;
        }
        #requests {
            margin-top: 20px;
        }
        .request-item {
            padding: 10px;
            margin: 5px 0;
            background-color: #f8f9fa;
            border-left: 4px solid #007bff;
            border-radius: 4px;
        }
        .server-1 { border-left-color: #dc3545; }
        .server-2 { border-left-color: #28a745; }
        .server-3 { border-left-color: #ffc107; }
    </style>
</head>
<body>
    <div class="container">
        <h1>nginx Load Balancer Demo</h1>
        <p>Click the button multiple times to see requests distributed across backend servers.</p>
        
        <button onclick="makeRequest()">Send Request</button>
        <button onclick="makeMultipleRequests(10)">Send 10 Requests</button>
        <button onclick="clearRequests()">Clear</button>
        
        <div id="requests"></div>
    </div>

    <script>
        let requestCount = 0;
        
        async function makeRequest() {
            requestCount++;
            try {
                const response = await fetch('/');
                const data = await response.json();
                const serverClass = data.server_id;
                const requestDiv = document.createElement('div');
                requestDiv.className = `request-item ${serverClass}`;
                requestDiv.innerHTML = `
                    <strong>Request #${requestCount}</strong> → 
                    ${data.server_id} (Port: ${data.port})
                `;
                document.getElementById('requests').prepend(requestDiv);
            } catch (error) {
                alert('Error: ' + error.message);
            }
        }
        
        async function makeMultipleRequests(count) {
            for (let i = 0; i < count; i++) {
                await makeRequest();
                await new Promise(resolve => setTimeout(resolve, 200));
            }
        }
        
        function clearRequests() {
            document.getElementById('requests').innerHTML = '';
            requestCount = 0;
        }
    </script>
</body>
</html>
EOF
```

Update nginx config to serve static files:
```nginx
upstream backend_servers {
    server 127.0.0.1:5001;
    server 127.0.0.1:5002;
    server 127.0.0.1:5003;
}

server {
    listen 8080;
    server_name localhost;

    location / {
        root /home/YOUR_USERNAME/nginx-demo/load-balancer/static;
        index index.html;
        try_files $uri $uri/ =404;
    }

    location /api/ {
        proxy_pass http://backend_servers;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
```

## Benefits of Load Balancing

- High availability: Continue serving if one server fails
- Scalability: Add more servers to handle increased load
- Performance: Distribute load across multiple servers
- Flexibility: Route based on different algorithms

## Cleanup

```bash
# Stop all Flask instances (Ctrl+C in each terminal)
sudo rm /etc/nginx/sites-enabled/load-balancer-demo
sudo nginx -s reload
```
