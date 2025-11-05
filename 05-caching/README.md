# Topic 5: Caching with nginx

This section demonstrates how to implement caching in nginx to improve performance and reduce backend load.

## Learning Objectives

- Understand caching concepts in nginx
- Configure proxy cache
- Set cache keys and zones
- Implement cache invalidation
- Understand cache headers and directives

## Prerequisites

- Understanding of reverse proxy (Topic 2)
- Flask application from previous topics

## Installation

### Install nginx
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install nginx -y
```

## Backend Application Setup

Create a Flask application that includes cache-control headers:

```bash
mkdir -p ~/nginx-demo/caching
cd ~/nginx-demo/caching

cat > app.py << 'EOF'
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
EOF
```

Start the Flask application:
```bash
python3 app.py
```

## nginx Caching Configuration

1. Create cache directory:
```bash
sudo mkdir -p /var/cache/nginx
sudo chown www-data:www-data /var/cache/nginx
```

2. Create nginx configuration:
```bash
sudo nano /etc/nginx/sites-available/caching-demo
```

Add the following configuration:
```nginx
# Define cache zone
proxy_cache_path /var/cache/nginx levels=1:2 keys_zone=my_cache:10m max_size=100m 
                 inactive=60m use_temp_path=off;

server {
    listen 8080;
    server_name localhost;

    # Enable caching for this server
    proxy_cache my_cache;
    proxy_cache_valid 200 302 10m;  # Cache 200 and 302 responses for 10 minutes
    proxy_cache_valid 404 1m;       # Cache 404 responses for 1 minute
    proxy_cache_use_stale error timeout updating http_500 http_502 http_503 http_504;
    proxy_cache_background_update on;
    proxy_cache_lock on;

    # Cache key includes full URL and query string
    proxy_cache_key "$scheme$request_method$host$request_uri";

    # Add cache status header for debugging
    add_header X-Cache-Status $upstream_cache_status;

    # Cache specific endpoints
    location /api/data {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        
        # Cache this endpoint for 5 minutes
        proxy_cache_valid 200 5m;
        proxy_cache_valid 404 1m;
    }

    # Cache static content for longer
    location /api/static {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        
        # Cache for 1 hour
        proxy_cache_valid 200 1h;
    }

    # No caching for this endpoint
    location /api/uncached {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        
        # Disable caching
        proxy_cache off;
        add_header Cache-Control "no-cache, no-store, must-revalidate";
    }

    # Default location
    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        
        # No caching by default
        proxy_cache off;
    }
}
```

3. Enable the site:
```bash
sudo ln -s /etc/nginx/sites-available/caching-demo /etc/nginx/sites-enabled/
```

4. Test and reload nginx:
```bash
sudo nginx -t
sudo nginx -s reload
```

## Testing Caching

1. Test cached endpoint (first request):
```bash
curl -v http://localhost:8080/api/data
```

Look for `X-Cache-Status: MISS` in headers - cache miss, response fetched from backend.

2. Test again immediately (second request):
```bash
curl -v http://localhost:8080/api/data
```

Look for `X-Cache-Status: HIT` in headers - cache hit, response served from cache.

3. Test uncached endpoint:
```bash
curl -v http://localhost:8080/api/uncached
```

Multiple requests will show `X-Cache-Status: BYPASS` - caching is disabled.

4. Compare response times:
```bash
# First request (cache miss)
time curl -s http://localhost:8080/api/data > /dev/null

# Second request (cache hit - should be much faster)
time curl -s http://localhost:8080/api/data > /dev/null
```

## Understanding Cache Directives

- `proxy_cache_path`: Defines cache zone location and settings
  - `levels=1:2`: Directory structure for cache files
  - `keys_zone=my_cache:10m`: Cache zone name and size in memory
  - `max_size=100m`: Maximum disk space for cache
  - `inactive=60m`: Remove files not accessed for 60 minutes

- `proxy_cache`: Enable caching for a location
- `proxy_cache_valid`: How long to cache responses by status code
- `proxy_cache_key`: Defines cache key (what makes responses unique)
- `add_header X-Cache-Status`: Shows cache status (MISS, HIT, BYPASS, etc.)

## Cache Status Values

- `MISS`: Request not found in cache, fetched from backend
- `HIT`: Response served from cache
- `BYPASS`: Cache was bypassed (e.g., Cache-Control: no-cache)
- `EXPIRED`: Cached entry expired, fetching fresh content
- `STALE`: Serving stale content (when backend is unavailable)
- `UPDATING`: Cache entry is being updated
- `REVALIDATED`: Cache entry was revalidated

## Cache Invalidation

### Method 1: Cache Purge (requires nginx cache purge module)

Install cache purge module:
```bash
# Ubuntu/Debian
sudo apt install nginx-module-http-cache-purge
```

Configure purge endpoint:
```nginx
location ~ /purge(/.*) {
    proxy_cache_purge my_cache $scheme$request_method$host$1;
}
```

### Method 2: Delete cache files manually

```bash
sudo rm -rf /var/cache/nginx/*
sudo nginx -s reload
```

### Method 3: Set short TTL

Use short `proxy_cache_valid` times for content that changes frequently.

## Advanced Caching Strategies

### Cache Based on Headers

```nginx
proxy_cache_key "$scheme$request_method$host$request_uri$http_accept_language";
```

### Conditional Caching

```nginx
location /api/ {
    proxy_pass http://127.0.0.1:5000;
    
    # Only cache GET and HEAD requests
    proxy_cache_methods GET HEAD;
    
    # Don't cache if backend sets no-cache
    proxy_ignore_headers "Cache-Control";
    proxy_cache_bypass $http_pragma $http_authorization;
}
```

### Cache Warming

Pre-populate cache by making requests:
```bash
curl http://localhost:8080/api/data
curl http://localhost:8080/api/static
```

## Monitoring Cache

Check cache directory size:
```bash
sudo du -sh /var/cache/nginx
```

List cache files:
```bash
sudo ls -lah /var/cache/nginx
```

Check nginx cache statistics (if configured):
```bash
curl http://localhost:8080/cache-stats
```

## Benefits of Caching

- Reduced backend load
- Faster response times
- Better user experience
- Lower bandwidth usage
- Improved scalability

## Best Practices

1. Cache static content aggressively
2. Use appropriate TTLs for different content types
3. Monitor cache hit rates
4. Implement cache invalidation strategies
5. Don't cache user-specific or sensitive data
6. Use cache headers from backend when appropriate

## Cleanup

```bash
# Stop Flask app (Ctrl+C)
sudo rm /etc/nginx/sites-enabled/caching-demo
sudo rm -rf /var/cache/nginx/*
sudo nginx -s reload
```
