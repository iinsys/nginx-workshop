# Topic 5: Caching with nginx

This section demonstrates how to implement caching in nginx to improve performance and reduce backend load.

## Learning Objectives

- Understand caching concepts in nginx
- Configure proxy cache
- Set cache keys and zones
- Implement cache invalidation
- Understand cache headers and directives

## Prerequisites

- Python 3.x and pip installed (see Topic 2 for installation)
- Understanding of reverse proxy (Topic 2)

## Installation

### Install nginx
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install nginx -y
```

### Install Python Dependencies

Navigate to the workshop directory and install dependencies:
```bash
cd 05-caching
pip3 install -r requirements.txt
```

## Backend Application Setup

1. Navigate to the workshop directory:
```bash
cd 05-caching
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

## What is Caching?

**Caching** is storing frequently accessed data in a fast storage location (memory or disk) so it can be retrieved quickly without going to the original source.

### Real-World Analogy:
Think of a library:
- **Without cache**: Every time you need a book, you go to the library (backend server) - slow!
- **With cache**: Popular books are kept at the front desk (cache) - fast!

### How nginx Caching Works:

1. **First Request (Cache MISS)**:
   ```
   Client → nginx → Backend Server → Response → nginx stores in cache → Client
   ```
   - nginx fetches from backend
   - Stores response in cache
   - Returns to client
   - Status: `X-Cache-Status: MISS`

2. **Subsequent Requests (Cache HIT)**:
   ```
   Client → nginx (checks cache) → Found! → Returns cached response → Client
   ```
   - nginx finds response in cache
   - Returns immediately (no backend call)
   - Much faster!
   - Status: `X-Cache-Status: HIT`

### Benefits:
- **Faster responses**: Cached content served instantly
- **Reduced backend load**: Backend doesn't process every request
- **Better scalability**: Can handle more users
- **Lower bandwidth**: Less data transfer

### When to Cache:
- ✅ Static content (images, CSS, JS)
- ✅ API responses that don't change often
- ✅ Public data that's the same for all users
- ❌ User-specific data (personal info)
- ❌ Real-time data (stock prices, chat messages)
- ❌ Data that changes frequently

## nginx Caching Configuration

1. Create cache directory:
```bash
sudo mkdir -p /var/cache/nginx
sudo chown www-data:www-data /var/cache/nginx
```

2. Create nginx configuration file:
```bash
sudo nano /etc/nginx/sites-available/caching-demo
```

**Note:** The configuration file is located at `/etc/nginx/sites-available/caching-demo`. This is the system nginx configuration file, not the `nginx.conf` file in the workshop directory.

3. Add the following configuration to `/etc/nginx/sites-available/caching-demo`:
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

4. Enable the site:
```bash
sudo ln -s /etc/nginx/sites-available/caching-demo /etc/nginx/sites-enabled/
```

5. Test and reload nginx:
```bash
sudo nginx -t
sudo nginx -s reload
```

## Testing Caching

### Step-by-Step Verification

#### Test 1: Verify Cache MISS (First Request)

Make your first request to a cached endpoint:
```bash
curl -v http://localhost:8080/api/data 2>&1 | grep -E "(X-Cache-Status|timestamp|random)"
```

**Expected Output:**
```
< X-Cache-Status: MISS
"timestamp": 1234567890.123
"random": 456
```

**What this means:**
- `X-Cache-Status: MISS` = Cache was empty, fetched from backend
- `timestamp` and `random` values = Fresh data from Flask

#### Test 2: Verify Cache HIT (Second Request)

Make the same request again immediately:
```bash
curl -v http://localhost:8080/api/data 2>&1 | grep -E "(X-Cache-Status|timestamp|random)"
```

**Expected Output:**
```
< X-Cache-Status: HIT
"timestamp": 1234567890.123    ← Same timestamp as before!
"random": 456                   ← Same random number!
```

**What this means:**
- `X-Cache-Status: HIT` = Response served from cache
- Same `timestamp` and `random` = Same data (not fresh from backend)
- **This proves caching is working!**

#### Test 3: Compare Response Times

See the speed difference:
```bash
echo "First request (cache MISS - slower):"
time curl -s http://localhost:8080/api/data > /dev/null

echo -e "\nSecond request (cache HIT - faster):"
time curl -s http://localhost:8080/api/data > /dev/null
```

**Expected Output:**
```
First request (cache MISS - slower):
real    0m0.105s    ← Includes backend processing time

Second request (cache HIT - faster):
real    0m0.002s    ← Much faster! Served from cache
```

#### Test 4: Verify Uncached Endpoint

Test an endpoint that should never be cached:
```bash
echo "Request 1:"
curl -s http://localhost:8080/api/uncached | python3 -m json.tool | grep -E "(X-Cache-Status|random)"

echo -e "\nRequest 2 (should have different random number):"
curl -s http://localhost:8080/api/uncached | python3 -m json.tool | grep -E "(X-Cache-Status|random)"
```

**Expected Output:**
```
Request 1:
"random": 1234

Request 2 (should have different random number):
"random": 5678    ← Different! Not cached
```

**What this means:**
- Different `random` values = Each request hits the backend
- Caching is disabled for this endpoint

#### Test 5: Visual Cache Status Comparison

See all cache statuses at once:
```bash
echo "=== Testing /api/data (CACHED) ==="
for i in {1..3}; do
    echo "Request $i:"
    curl -s -w "\nX-Cache-Status: %{header_x-cache-status}\n\n" http://localhost:8080/api/data | head -3
    sleep 1
done

echo -e "\n=== Testing /api/uncached (NOT CACHED) ==="
for i in {1..3}; do
    echo "Request $i:"
    curl -s -w "\nX-Cache-Status: %{header_x-cache-status}\n\n" http://localhost:8080/api/uncached | head -3
    sleep 1
done
```

**Expected Output:**
```
=== Testing /api/data (CACHED) ===
Request 1:
X-Cache-Status: MISS    ← First time, cache miss

Request 2:
X-Cache-Status: HIT     ← Cached! Much faster

Request 3:
X-Cache-Status: HIT     ← Still cached

=== Testing /api/uncached (NOT CACHED) ===
Request 1:
X-Cache-Status: BYPASS  ← Caching disabled

Request 2:
X-Cache-Status: BYPASS  ← Still bypassed

Request 3:
X-Cache-Status: BYPASS  ← Always bypassed
```

### Quick Verification Checklist

✅ **Caching is working if:**
- First request shows `X-Cache-Status: MISS`
- Second request shows `X-Cache-Status: HIT`
- Second request has same data (same timestamp/random)
- Second request is faster (check with `time` command)

❌ **If you see issues:**
- Always `MISS` → Check nginx config, cache directory permissions
- Always `BYPASS` → Check if endpoint has `proxy_cache off`
- No `X-Cache-Status` header → Check nginx config has `add_header X-Cache-Status`

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
