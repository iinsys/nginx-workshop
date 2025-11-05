# nginx Configuration Basics

## Configuration File Structure

nginx configuration files use a simple, declarative syntax:

- **Directives:** Configuration commands ending with semicolons
- **Contexts:** Blocks that group related directives
- **Comments:** Lines starting with `#`

## Configuration Files Location

Typical locations:

- **Main config:** `/etc/nginx/nginx.conf`
- **Site configs:** `/etc/nginx/sites-available/` (available sites)
- **Enabled sites:** `/etc/nginx/sites-enabled/` (symlinks to sites-available)
- **Module configs:** `/etc/nginx/conf.d/`
- **MIME types:** `/etc/nginx/mime.types`

## Basic Configuration Structure

```nginx
# Main context
user www-data;
worker_processes auto;
error_log /var/log/nginx/error.log;

events {
    # Events context
    worker_connections 1024;
}

http {
    # HTTP context
    include /etc/nginx/mime.types;
    default_type application/octet-stream;
    
    server {
        # Server context (virtual host)
        listen 80;
        server_name example.com;
        
        location / {
            # Location context
            root /var/www/html;
            index index.html;
        }
    }
}
```

## Common Directives

### Main Context Directives

```nginx
user www-data;              # Run workers as this user
worker_processes 4;         # Number of worker processes
error_log /path/to/error.log;  # Error log location
pid /var/run/nginx.pid;     # PID file location
```

### Events Context Directives

```nginx
events {
    worker_connections 1024;  # Max connections per worker
    use epoll;                # Event method (auto-detected)
    multi_accept on;          # Accept multiple connections at once
}
```

### HTTP Context Directives

```nginx
http {
    include /etc/nginx/mime.types;
    default_type application/octet-stream;
    
    # Logging
    access_log /var/log/nginx/access.log;
    log_format main '$remote_addr - $remote_user [$time_local] "$request" '
                    '$status $body_bytes_sent "$http_referer" ';
    
    # Performance
    sendfile on;
    tcp_nopush on;
    tcp_nodelay on;
    keepalive_timeout 65;
    
    # Compression
    gzip on;
    gzip_types text/plain text/css application/json;
}
```

## Server Blocks (Virtual Hosts)

Server blocks define how nginx responds to requests for different domains or IP addresses:

```nginx
server {
    listen 80;
    server_name example.com www.example.com;
    
    root /var/www/example;
    index index.html;
    
    location / {
        try_files $uri $uri/ =404;
    }
}
```

### Server Block Matching

nginx selects server block based on:
1. Exact `server_name` match
2. Leading wildcard: `*.example.com`
3. Trailing wildcard: `example.*`
4. Regex match: `~^www\.example\.com$`
5. Default server (first or `default_server`)

## Location Blocks

Location blocks define how to process requests for different URIs:

```nginx
location / {
    # Process all requests
}

location /api/ {
    # Process /api/ and sub-paths
}

location = /exact {
    # Exact match only
}

location ~ \.php$ {
    # Regex match for .php files
}

location ~* \.(jpg|png)$ {
    # Case-insensitive regex match
}
```

### Location Matching Priority

1. Exact match (`=`)
2. Prefix match (longest first)
3. Regex match (`~`, `~*`) in order
4. Generic prefix match (`/`)

## Important Directives

### File Serving

```nginx
root /var/www/html;        # Document root directory
index index.html;          # Default index file
try_files $uri $uri/ =404; # Try to serve file, then directory, else 404
```

### Proxy Directives

```nginx
proxy_pass http://backend;
proxy_set_header Host $host;
proxy_set_header X-Real-IP $remote_addr;
proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
proxy_set_header X-Forwarded-Proto $scheme;
```

### Variables

nginx provides many built-in variables:

- `$host` - Request host header
- `$request_uri` - Full request URI
- `$uri` - Request URI without arguments
- `$args` - Query string arguments
- `$remote_addr` - Client IP address
- `$status` - Response status code
- `$body_bytes_sent` - Response body size

## Configuration Best Practices

### 1. Test Before Reloading

Always test configuration before applying:
```bash
sudo nginx -t
```

### 2. Use Includes

Organize configuration with includes:
```nginx
http {
    include /etc/nginx/conf.d/*.conf;
    include /etc/nginx/sites-enabled/*;
}
```

### 3. Separate Site Configs

Use `sites-available` and `sites-enabled`:
```bash
# Create config
sudo nano /etc/nginx/sites-available/my-site

# Enable site
sudo ln -s /etc/nginx/sites-available/my-site /etc/nginx/sites-enabled/

# Disable site
sudo rm /etc/nginx/sites-enabled/my-site
```

### 4. Use Meaningful Comments

Document your configuration:
```nginx
# Serve static files from /var/www/html
location / {
    root /var/www/html;
    index index.html;
}
```

### 5. Security Headers

Always add security headers:
```nginx
add_header X-Frame-Options "SAMEORIGIN" always;
add_header X-Content-Type-Options "nosniff" always;
```

## Configuration Testing

### Syntax Check

```bash
sudo nginx -t
```

### Dry Run (if supported)

```bash
sudo nginx -T  # Print full configuration
```

### Reload Configuration

```bash
# Graceful reload (no downtime)
sudo nginx -s reload
# or
sudo systemctl reload nginx
```

## Common Configuration Patterns

### Static File Server

```nginx
server {
    listen 80;
    server_name example.com;
    root /var/www/html;
    index index.html;
    
    location / {
        try_files $uri $uri/ =404;
    }
}
```

### Reverse Proxy

```nginx
server {
    listen 80;
    server_name api.example.com;
    
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### Load Balancer

```nginx
upstream backend {
    server 127.0.0.1:8001;
    server 127.0.0.1:8002;
    server 127.0.0.1:8003;
}

server {
    listen 80;
    
    location / {
        proxy_pass http://backend;
    }
}
```

## Troubleshooting Configuration

### Check Error Logs

```bash
sudo tail -f /var/log/nginx/error.log
```

### Common Errors

1. **Semicolon missing:** `directive "proxy_pass" has no closing ";"`
2. **Unknown directive:** Check if module is loaded
3. **Permission denied:** Check file/directory permissions
4. **Port already in use:** Change port or stop conflicting service

## Next Steps

- Understand [Core Concepts](./04-concepts.md)
- Try the hands-on demos:
  - [Demo 1: Serving Files](../01-serving-files/)
  - [Demo 2: Reverse Proxy](../02-reverse-proxy/)
