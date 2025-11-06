# Topic 4: SSL Termination with nginx

This section demonstrates how to configure SSL/TLS termination in nginx to enable HTTPS.

## Learning Objectives

- Understand SSL/TLS termination concept
- Generate self-signed certificates for testing
- Configure nginx to serve HTTPS traffic
- Redirect HTTP to HTTPS
- Understand certificate management

## Prerequisites

- Python 3.x and pip installed (see Topic 2 for installation)
- OpenSSL installed (usually pre-installed on Linux/macOS)
- Understanding of reverse proxy (Topic 2)

## Installation

### Install nginx
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install nginx -y
```

### Install OpenSSL

OpenSSL is usually pre-installed on Linux/macOS, but if needed:

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install openssl -y
```

**CentOS/RHEL:**
```bash
sudo yum install openssl -y
```

**macOS:**
```bash
brew install openssl
```

### Verify OpenSSL Installation
```bash
openssl version
```

### Install Python Dependencies

Navigate to the workshop directory and install dependencies:
```bash
cd 04-ssl-termination
pip3 install -r requirements.txt
```

## What is OpenSSL?

**OpenSSL** is an open-source toolkit that provides cryptographic functions for secure communication over networks. It's used for:

- **SSL/TLS protocols**: Enables HTTPS (secure HTTP) connections
- **Certificate management**: Creates, signs, and manages SSL certificates
- **Encryption**: Encrypts data in transit between client and server
- **Key generation**: Generates public/private key pairs for secure communication

In this workshop, we use OpenSSL to:
1. Generate a private key for our SSL certificate
2. Create a self-signed certificate for testing HTTPS locally
3. Enable secure (encrypted) communication between browsers and nginx

**Note:** For production, you'd use certificates from trusted Certificate Authorities (like Let's Encrypt) instead of self-signed certificates.

## Generate Self-Signed Certificate

For production, you would use certificates from a Certificate Authority (CA) like Let's Encrypt. For demonstration purposes, we'll create a self-signed certificate.

1. Create directory for certificates in the workshop directory:
```bash
cd 04-ssl-termination
mkdir -p ssl/certs
cd ssl/certs
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

1. Navigate to the workshop directory:
```bash
cd 04-ssl-termination
```

2. Install Python dependencies (if not already done):
```bash
pip3 install -r requirements.txt
```

3. Start the Flask application:
```bash
python3 app.py
```

The Flask app will run on `http://localhost:5000`. Keep this terminal open.

## nginx SSL Configuration

1. Create nginx configuration file:
```bash
sudo nano /etc/nginx/sites-available/ssl-demo
```

**Note:** The configuration file is located at `/etc/nginx/sites-available/ssl-demo`. This is the system nginx configuration file, not the `nginx.conf` file in the workshop directory.

2. Add the following configuration to `/etc/nginx/sites-available/ssl-demo`:
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
    # Replace /path/to/nginx-workshop with the actual path to your cloned repository
    # Example: /home/username/nginx-workshop/04-ssl-termination/ssl/certs/nginx-demo.crt
    ssl_certificate /path/to/nginx-workshop/04-ssl-termination/ssl/certs/nginx-demo.crt;
    ssl_certificate_key /path/to/nginx-workshop/04-ssl-termination/ssl/certs/nginx-demo.key;

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

**Important Notes:**
- **Configuration file location**: `/etc/nginx/sites-available/ssl-demo` (system nginx config, not the workshop `nginx.conf`)
- Replace `/path/to/nginx-workshop` with the actual path to your cloned repository
- Example: If your repo is at `/home/username/nginx-workshop`, the certificate path would be:
  - `/home/username/nginx-workshop/04-ssl-termination/ssl/certs/nginx-demo.crt`
- Make sure the `ssl/certs/` directory exists and contains the certificate files before starting nginx

3. Update the configuration file with your actual paths:
```bash
sudo nano /etc/nginx/sites-available/ssl-demo
```

Replace `/path/to/nginx-workshop` with your actual repository path, then save and exit (Ctrl+X, then Y, then Enter).

4. Enable the site:
```bash
sudo ln -s /etc/nginx/sites-available/ssl-demo /etc/nginx/sites-enabled/
```

5. Test and reload nginx:
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
