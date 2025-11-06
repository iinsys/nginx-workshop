# Topic 3: nginx as Load Balancer

This section demonstrates how to configure nginx as a load balancer to distribute traffic across multiple backend instances.

## Learning Objectives

- Understand load balancing concepts
- Configure nginx upstream blocks
- Implement different load balancing algorithms
- Run multiple instances of the same application
- Monitor request distribution

## Prerequisites

- Python 3.x and pip installed (see Topic 2 for installation)
- Flask installed
- Basic understanding of reverse proxy (Topic 2)

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
cd 03-load-balancer
pip3 install -r requirements.txt
```

## Running Multiple Backend Instances

Open three separate terminal windows and run (you should already be in the `03-load-balancer` directory):

**Terminal 1:**
```bash
cd 03-load-balancer
SERVER_ID=server-1 python3 app.py 5001
```

**Terminal 2:**
```bash
cd 03-load-balancer
SERVER_ID=server-2 python3 app.py 5002
```

**Terminal 3:**
```bash
cd 03-load-balancer
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

    # Serve static files from frontend
    # Replace /path/to/nginx-workshop with the actual path to your cloned repository
    location / {
        root /path/to/nginx-workshop/03-load-balancer/static;
        index index.html;
        try_files $uri $uri/ =404;
    }

    # Proxy API requests to load balanced backends
    location /api/ {
        proxy_pass http://backend_servers;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

**Configuration Explanation:**
- `location /`: Serves static files (frontend HTML) from the `static` directory
- `location /api/`: Proxies API requests to the load-balanced backend servers
- The `root` directive points to your static files directory
- Replace `/path/to/nginx-workshop` with your actual repository path

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

### Method 1: Command Line (Recommended)

Test the load balancer and see which server responds (use `/api/` endpoint):
```bash
# Make multiple requests and see server_id in response
for i in {1..10}; do
    echo -n "Request $i: "
    curl -s http://localhost:8080/api/ | python3 -m json.tool | grep server_id
    sleep 0.3
done
```

**Expected output:**
```
Request 1:     "server_id": "server-1",
Request 2:     "server_id": "server-2",
Request 3:     "server_id": "server-3",
Request 4:     "server_id": "server-1",
...
```

**Note:** Use `/api/` endpoint for API requests. The root `/` serves static files (frontend).

### Method 2: Simple curl with jq (if installed)

```bash
for i in {1..10}; do
    echo -n "Request $i: "
    curl -s http://localhost:8080/api/ | jq -r '.server_id'
    sleep 0.3
done
```

### Method 3: Count Distribution

Count how many requests each server handles:
```bash
for i in {1..30}; do
    curl -s http://localhost:8080/api/ | python3 -m json.tool | grep server_id
    sleep 0.1
done | sort | uniq -c
```

**Expected output:**
```
     10 "server_id": "server-1",
     10 "server_id": "server-2",
     10 "server_id": "server-3",
```

### Method 4: Direct Backend Testing

Verify each backend is running and responding:
```bash
echo "Testing backends directly:"
curl -s http://localhost:5001 | python3 -m json.tool | grep server_id
curl -s http://localhost:5002 | python3 -m json.tool | grep server_id
curl -s http://localhost:5003 | python3 -m json.tool | grep server_id
```

**Expected output:**
```
    "server_id": "server-1",
    "server_id": "server-2",
    "server_id": "server-3",
```

### Verification Checklist

✅ **Load balancing is working if:**
- Requests show different `server_id` values (server-1, server-2, server-3)
- Requests are distributed across all three servers
- Each backend responds correctly when tested directly
- nginx returns responses without errors

❌ **If you see issues:**
- All requests show the same server → Check if all backends are running
- Connection refused → Verify nginx is running and config is correct
- No response → Check nginx error logs: `sudo tail -f /var/log/nginx/error.log`

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

An interactive HTML page is included in `static/index.html` to visualize load balancing in real-time.

The frontend features:
- **Real-time statistics**: Live counters showing request distribution across all 3 servers
- **Visual request tracking**: Color-coded requests with timestamps
- **Interactive controls**: Send single requests, batches, or continuous auto-requests
- **Live updates**: Watch requests distribute in real-time as you interact

To use the frontend:
1. The `static/index.html` file is already in the repository
2. Configure nginx to serve static files (see configuration below)
3. Open `http://localhost:8080` in your browser
4. Click buttons to send requests and watch load balancing in action!

Update nginx config to serve static files:

**Update the system nginx configuration file:**
```bash
sudo nano /etc/nginx/sites-available/load-balancer-demo
```

Replace the content with:
```nginx
upstream backend_servers {
    server 127.0.0.1:5001;
    server 127.0.0.1:5002;
    server 127.0.0.1:5003;
}

server {
    listen 8080;
    server_name localhost;

    # Serve static files
    # Replace /path/to/nginx-workshop with the actual path to your cloned repository
    location / {
        root /path/to/nginx-workshop/03-load-balancer/static;
        index index.html;
        try_files $uri $uri/ =404;
    }

    # Proxy API requests to load balanced backends
    location /api/ {
        proxy_pass http://backend_servers;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
```

**Note:** The configuration file is located at `/etc/nginx/sites-available/load-balancer-demo`.

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
