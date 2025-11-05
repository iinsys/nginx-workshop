# Topic 6: Docker Compose Integration

This section demonstrates how to deploy complete nginx setups using Docker Compose, combining all the concepts from previous topics.

## Learning Objectives

- Understand Docker Compose basics
- Containerize Flask applications
- Configure nginx in Docker containers
- Set up complete multi-container applications
- Implement load balancing, SSL, and caching with Docker

## Prerequisites

- Docker installed
- Docker Compose installed
- Basic understanding of Docker concepts

## Installation

### Install Docker
```bash
# Ubuntu/Debian
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER
```

### Install Docker Compose
```bash
# Docker Compose is included with Docker Desktop
# For Linux, install separately:
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```

Verify installation:
```bash
docker --version
docker-compose --version
```

## Project Structure

```
06-docker-compose/
├── README.md
├── docker-compose.yml
├── nginx/
│   ├── nginx.conf
│   └── ssl/
│       ├── nginx-demo.crt
│       └── nginx-demo.key
├── backend/
│   ├── Dockerfile
│   ├── app.py
│   └── requirements.txt
└── frontend/
    ├── Dockerfile
    └── static/
        └── index.html
```

## Complete Example: Load Balancer + SSL + Caching

This example combines:
- Multiple Flask backend instances (load balancing)
- nginx as reverse proxy and load balancer
- SSL termination
- Caching
- Static file serving

### Step 1: Create Backend Application

Create `backend/app.py`:
```python
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
```

Create `backend/requirements.txt`:
```
Flask==3.0.0
```

Create `backend/Dockerfile`:
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

EXPOSE 5000

CMD ["python", "app.py"]
```

### Step 2: Create Frontend

Create `frontend/static/index.html`:
```html
<!DOCTYPE html>
<html>
<head>
    <title>nginx Docker Compose Demo</title>
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
        <h1>nginx Docker Compose Demo</h1>
        <p>This frontend is served by nginx. API calls are load balanced across multiple Flask backends.</p>
        
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
```

Create `frontend/Dockerfile`:
```dockerfile
FROM nginx:alpine

COPY static/ /usr/share/nginx/html/

EXPOSE 80
```

### Step 3: Create nginx Configuration

Create `nginx/nginx.conf`:
```nginx
# Cache zone
proxy_cache_path /var/cache/nginx levels=1:2 keys_zone=my_cache:10m max_size=100m 
                 inactive=60m use_temp_path=off;

# Upstream backend servers
upstream backend_servers {
    server backend1:5000;
    server backend2:5000;
    server backend3:5000;
}

# HTTP server - redirect to HTTPS
server {
    listen 80;
    server_name localhost;
    
    return 301 https://$server_name$request_uri;
}

# HTTPS server
server {
    listen 443 ssl http2;
    server_name localhost;

    # SSL certificates
    ssl_certificate /etc/nginx/ssl/nginx-demo.crt;
    ssl_certificate_key /etc/nginx/ssl/nginx-demo.key;

    # SSL configuration
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    ssl_prefer_server_ciphers on;

    # Security headers
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;

    # Serve static files from frontend
    location / {
        root /usr/share/nginx/html;
        index index.html;
        try_files $uri $uri/ =404;
    }

    # Proxy API requests with caching
    location /api/ {
        proxy_pass http://backend_servers;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # Enable caching
        proxy_cache my_cache;
        proxy_cache_valid 200 5m;
        proxy_cache_key "$scheme$request_method$host$request_uri";
        add_header X-Cache-Status $upstream_cache_status;
    }
}
```

### Step 4: Generate SSL Certificates

```bash
cd docs/06-docker-compose
mkdir -p nginx/ssl
cd nginx/ssl

openssl genrsa -out nginx-demo.key 2048
openssl req -new -key nginx-demo.key -out nginx-demo.csr -subj "/CN=localhost"
openssl x509 -req -days 365 -in nginx-demo.csr -signkey nginx-demo.key -out nginx-demo.crt

rm nginx-demo.csr
chmod 600 nginx-demo.key
chmod 644 nginx-demo.crt
```

### Step 5: Create Docker Compose File

Create `docker-compose.yml`:
```yaml
version: '3.8'

services:
  # Backend services (3 instances for load balancing)
  backend1:
    build: ./backend
    container_name: flask-backend-1
    environment:
      - PORT=5000
    networks:
      - nginx-network

  backend2:
    build: ./backend
    container_name: flask-backend-2
    environment:
      - PORT=5000
    networks:
      - nginx-network

  backend3:
    build: ./backend
    container_name: flask-backend-3
    environment:
      - PORT=5000
    networks:
      - nginx-network

  # Frontend service
  frontend:
    build: ./frontend
    container_name: nginx-frontend
    volumes:
      - ./frontend/static:/usr/share/nginx/html:ro
    networks:
      - nginx-network

  # nginx reverse proxy and load balancer
  nginx:
    image: nginx:alpine
    container_name: nginx-proxy
    ports:
      - "8080:80"
      - "8443:443"
    volumes:
      - ./nginx/nginx.conf:/etc/nginx/nginx.conf:ro
      - ./nginx/ssl:/etc/nginx/ssl:ro
      - ./frontend/static:/usr/share/nginx/html:ro
      - nginx-cache:/var/cache/nginx
    depends_on:
      - backend1
      - backend2
      - backend3
      - frontend
    networks:
      - nginx-network
    command: >
      sh -c "nginx -g 'daemon off;'"

volumes:
  nginx-cache:

networks:
  nginx-network:
    driver: bridge
```

Note: The nginx.conf above uses `include /etc/nginx/nginx.conf` syntax. For a complete config, create `nginx/nginx.conf` as:

```nginx
events {
    worker_connections 1024;
}

http {
    include /etc/nginx/mime.types;
    default_type application/octet-stream;

    # Cache zone
    proxy_cache_path /var/cache/nginx levels=1:2 keys_zone=my_cache:10m max_size=100m 
                     inactive=60m use_temp_path=off;

    # Upstream backend servers
    upstream backend_servers {
        server backend1:5000;
        server backend2:5000;
        server backend3:5000;
    }

    # HTTP server - redirect to HTTPS
    server {
        listen 80;
        server_name localhost;
        
        return 301 https://$server_name$request_uri;
    }

    # HTTPS server
    server {
        listen 443 ssl http2;
        server_name localhost;

        # SSL certificates
        ssl_certificate /etc/nginx/ssl/nginx-demo.crt;
        ssl_certificate_key /etc/nginx/ssl/nginx-demo.key;

        # SSL configuration
        ssl_protocols TLSv1.2 TLSv1.3;
        ssl_ciphers HIGH:!aNULL:!MD5;
        ssl_prefer_server_ciphers on;

        # Security headers
        add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
        add_header X-Frame-Options "SAMEORIGIN" always;
        add_header X-Content-Type-Options "nosniff" always;

        # Serve static files from frontend
        location / {
            root /usr/share/nginx/html;
            index index.html;
            try_files $uri $uri/ =404;
        }

        # Proxy API requests with caching
        location /api/ {
            proxy_pass http://backend_servers;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
            
            # Enable caching
            proxy_cache my_cache;
            proxy_cache_valid 200 5m;
            proxy_cache_key "$scheme$request_method$host$request_uri";
            add_header X-Cache-Status $upstream_cache_status;
        }
    }
}
```

## Running the Application

1. Navigate to the project directory:
```bash
cd docs/06-docker-compose
```

2. Build and start all services:
```bash
docker-compose up --build
```

Or run in detached mode:
```bash
docker-compose up -d --build
```

3. Check running containers:
```bash
docker-compose ps
```

4. View logs:
```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f nginx
docker-compose logs -f backend1
```

## Testing

1. Test HTTP redirect:
```bash
curl -L http://localhost:8080
```

2. Test HTTPS endpoint:
```bash
curl -k https://localhost:8443
```

3. Test load balancing:
```bash
for i in {1..10}; do
    echo "Request $i:"
    curl -k -s https://localhost:8443/api/data | grep hostname
    sleep 0.5
done
```

4. Test caching:
```bash
# First request (cache miss)
curl -k -v https://localhost:8443/api/data | grep X-Cache-Status

# Second request (cache hit)
curl -k -v https://localhost:8443/api/data | grep X-Cache-Status
```

5. Open in browser:
```
https://localhost:8443
```
(Accept the security warning for self-signed certificate)

## Managing the Application

### Stop services:
```bash
docker-compose down
```

### Stop and remove volumes:
```bash
docker-compose down -v
```

### Restart a specific service:
```bash
docker-compose restart nginx
```

### Scale backend instances:
```bash
docker-compose up -d --scale backend1=2 --scale backend2=2 --scale backend3=2
```

### Execute commands in containers:
```bash
docker-compose exec nginx nginx -t
docker-compose exec backend1 python -c "import flask; print(flask.__version__)"
```

## Simplified Example (HTTP Only)

For a simpler example without SSL, create `docker-compose.simple.yml`:

```yaml
version: '3.8'

services:
  backend1:
    build: ./backend
    environment:
      - PORT=5000

  backend2:
    build: ./backend
    environment:
      - PORT=5000

  backend3:
    build: ./backend
    environment:
      - PORT=5000

  nginx:
    image: nginx:alpine
    ports:
      - "8080:80"
    volumes:
      - ./nginx/nginx-simple.conf:/etc/nginx/nginx.conf:ro
      - ./frontend/static:/usr/share/nginx/html:ro
    depends_on:
      - backend1
      - backend2
      - backend3
```

## Benefits of Docker Compose

- Easy environment setup
- Consistent deployments
- Isolated services
- Simple scaling
- Network management
- Volume management
- Development and production parity

## Cleanup

```bash
# Stop and remove containers, networks
docker-compose down

# Remove volumes as well
docker-compose down -v

# Remove images
docker-compose down --rmi all
```

## Next Steps

- Add environment variables for configuration
- Implement health checks
- Add monitoring and logging
- Set up CI/CD pipelines
- Deploy to production environments
