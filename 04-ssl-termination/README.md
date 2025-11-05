# Topic 4: SSL Termination with nginx

This section demonstrates how to configure SSL/TLS termination in nginx to enable HTTPS.

## Learning Objectives

- Understand SSL/TLS termination concept
- Generate self-signed certificates for testing
- Configure nginx to serve HTTPS traffic
- Redirect HTTP to HTTPS
- Understand certificate management

## Prerequisites

- OpenSSL installed (usually pre-installed on Linux/macOS)
- Understanding of reverse proxy (Topic 2)
- Flask application from previous topics

## Installation

### Install nginx
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install nginx -y
```

### Verify OpenSSL
```bash
openssl version
```

## Generate Self-Signed Certificate

For production, you would use certificates from a Certificate Authority (CA) like Let's Encrypt. For demonstration purposes, we'll create a self-signed certificate.

1. Create directory for certificates:
```bash
mkdir -p ~/nginx-demo/ssl/certs
cd ~/nginx-demo/ssl/certs
```

2. Generate private key:
```bash
openssl genrsa -out nginx-demo.key 2048
```

3. Generate certificate signing request (CSR):
```bash
openssl req -new -key nginx-demo.key -out nginx-demo.csr
```

When prompted, you can use defaults or enter:
- Country Name: (your country code, e.g., US)
- State: (your state)
- Locality: (your city)
- Organization: nginx-demo
- Organizational Unit: IT
- Common Name: localhost (IMPORTANT for testing)
- Email: (your email)
- Challenge password: (leave empty)
- Optional company name: (leave empty)

4. Generate self-signed certificate:
```bash
openssl x509 -req -days 365 -in nginx-demo.csr -signkey nginx-demo.key -out nginx-demo.crt
```

5. Set appropriate permissions:
```bash
chmod 600 nginx-demo.key
chmod 644 nginx-demo.crt
```

## Flask Backend Setup

Use the Flask application from Topic 2 (Reverse Proxy):

```bash
mkdir -p ~/nginx-demo/ssl-demo
cd ~/nginx-demo/ssl-demo

cat > app.py << 'EOF'
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({
        'message': 'Hello from Flask Backend!',
        'protocol': 'HTTPS via nginx SSL Termination',
        'status': 'running'
    })

@app.route('/api/data')
def get_data():
    return jsonify({
        'data': [1, 2, 3, 4, 5],
        'count': 5
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
EOF
```

Start the Flask application:
```bash
python3 app.py
```

## nginx SSL Configuration

1. Create nginx configuration:
```bash
sudo nano /etc/nginx/sites-available/ssl-demo
```

Add the following configuration:
```nginx
# Redirect HTTP to HTTPS
server {
    listen 8080;
    server_name localhost;
    
    # Redirect all HTTP requests to HTTPS
    return 301 https://$server_name:8443$request_uri;
}

# HTTPS server
server {
    listen 8443 ssl;
    server_name localhost;

    # SSL certificate paths
    ssl_certificate /home/YOUR_USERNAME/nginx-demo/ssl/certs/nginx-demo.crt;
    ssl_certificate_key /home/YOUR_USERNAME/nginx-demo/ssl/certs/nginx-demo.key;

    # SSL configuration
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    ssl_prefer_server_ciphers on;

    # Security headers
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;

    # Proxy to Flask backend
    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_set_header X-Forwarded-Port $server_port;
    }

    location /api/ {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

Note: Replace `YOUR_USERNAME` with your actual username.

2. Enable the site:
```bash
sudo ln -s /etc/nginx/sites-available/ssl-demo /etc/nginx/sites-enabled/
```

3. Test and reload nginx:
```bash
sudo nginx -t
sudo nginx -s reload
```

## Testing SSL Termination

1. Test HTTPS connection:
```bash
curl -k https://localhost:8443
```

The `-k` flag is needed because we're using a self-signed certificate (not trusted by default).

2. Test HTTP redirect:
```bash
curl -L http://localhost:8080
```

3. Browser testing:
   - Navigate to `https://localhost:8443`
   - Your browser will show a security warning (expected with self-signed certificates)
   - Click "Advanced" and "Proceed to localhost" to continue
   - You should see the Flask backend response

## Understanding SSL Configuration

- `listen 8443 ssl`: Listen on port 8443 with SSL enabled
- `ssl_certificate`: Path to SSL certificate file
- `ssl_certificate_key`: Path to private key file
- `ssl_protocols`: Allowed SSL/TLS protocols
- `ssl_ciphers`: Allowed cipher suites
- `ssl_prefer_server_ciphers`: Use server's preferred ciphers

## Security Headers

- `Strict-Transport-Security (HSTS)`: Forces browsers to use HTTPS
- `X-Frame-Options`: Prevents clickjacking attacks
- `X-Content-Type-Options`: Prevents MIME type sniffing

## Using Let's Encrypt (Production)

For production environments, use Let's Encrypt with certbot:

```bash
# Install certbot
sudo apt install certbot python3-certbot-nginx -y

# Obtain certificate
sudo certbot --nginx -d yourdomain.com

# Auto-renewal is set up automatically
```

## Mixed Configuration (HTTP and HTTPS)

If you want to serve both HTTP and HTTPS:

```nginx
# HTTP server
server {
    listen 8080;
    server_name localhost;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}

# HTTPS server
server {
    listen 8443 ssl;
    server_name localhost;

    ssl_certificate /path/to/cert.crt;
    ssl_certificate_key /path/to/key.key;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

## Benefits of SSL Termination

- Encrypts data in transit
- Offloads SSL processing from backend servers
- Centralized certificate management
- Better performance (nginx is optimized for SSL)
- Compliance with security standards

## Troubleshooting

1. Certificate permission errors:
```bash
sudo chmod 644 /path/to/cert.crt
sudo chmod 600 /path/to/key.key
```

2. Check nginx error logs:
```bash
sudo tail -f /var/log/nginx/error.log
```

3. Verify certificate:
```bash
openssl x509 -in nginx-demo.crt -text -noout
```

## Cleanup

```bash
# Stop Flask app (Ctrl+C)
sudo rm /etc/nginx/sites-enabled/ssl-demo
sudo nginx -s reload
```
