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

**Ubuntu/Debian:**
```bash
# Update package index
sudo apt update

# Install Docker
sudo apt install docker.io -y

# Start and enable Docker service
sudo systemctl start docker
sudo systemctl enable docker

# Add your user to docker group (to run without sudo)
sudo usermod -aG docker $USER

# Log out and log back in for group changes to take effect
```

**Alternative method (official script):**
```bash
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER
```

**CentOS/RHEL:**
```bash
sudo yum install docker -y
sudo systemctl start docker
sudo systemctl enable docker
sudo usermod -aG docker $USER
```

**macOS:**
```bash
# Install Docker Desktop from: https://www.docker.com/products/docker-desktop
# Or use Homebrew:
brew install --cask docker
```

### Install Docker Compose

**Docker Compose v2** is the recommended version and is included with newer Docker installations as a plugin.

**Ubuntu/Debian:**
```bash
# Install Docker Compose v2 plugin
sudo apt update
sudo apt install docker-compose-plugin -y
```

**CentOS/RHEL:**
```bash
# Install Docker Compose v2 plugin
sudo yum install docker-compose-plugin -y
```

**macOS:**
Docker Compose is included with Docker Desktop.

**Verify installation:**
```bash
docker --version
docker compose version
```

**Important Notes:**
- Use `docker compose` (with space, v2) instead of `docker-compose` (with hyphen, v1)
- The v2 plugin is the recommended version and works better with newer Docker versions
- If you see errors with `docker-compose`, use `docker compose` instead
- After adding user to docker group, you may need to log out and log back in

**Official Documentation:**
- [Docker Installation Guide](https://docs.docker.com/engine/install/)
- [Docker Compose Installation](https://docs.docker.com/compose/install/)

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

This example combines all concepts from previous topics:
- Multiple Flask backend instances (load balancing)
- nginx as reverse proxy and load balancer
- SSL termination
- Caching
- Static file serving

All files are already in the repository. The project structure is:

```
06-docker-compose/
├── docker-compose.yml
├── backend/
│   ├── app.py
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/
│   ├── Dockerfile
│   └── static/
│       └── index.html
└── nginx/
    ├── nginx.conf
    └── ssl/          (SSL certificates will be generated here)
```

### Step 1: Generate SSL Certificates (Required)

**Important:** You must generate SSL certificates before running Docker Compose, otherwise nginx will fail to start.

Navigate to the workshop directory and generate SSL certificates:
```bash
cd 06-docker-compose
mkdir -p nginx/ssl
cd nginx/ssl

# Generate private key
openssl genrsa -out nginx-demo.key 2048

# Generate certificate (use defaults or press Enter for all prompts)
openssl req -new -key nginx-demo.key -out nginx-demo.csr -subj "/CN=localhost"

# Generate self-signed certificate
openssl x509 -req -days 365 -in nginx-demo.csr -signkey nginx-demo.key -out nginx-demo.crt

# Clean up and set permissions
rm nginx-demo.csr
chmod 600 nginx-demo.key
chmod 644 nginx-demo.crt
```

### Step 2: Review Configuration Files

All configuration files are already in the repository:

- **`docker-compose.yml`**: Defines all services (3 backends, frontend, nginx)
- **`backend/Dockerfile`**: Builds Flask application container
- **`frontend/Dockerfile`**: Builds static file server
- **`nginx/nginx.conf`**: nginx configuration with load balancing, SSL, and caching

You can review these files to understand the setup. The `nginx/nginx.conf` includes:
- Cache zone configuration
- Upstream backend servers (3 instances)
- HTTP to HTTPS redirect
- SSL termination
- Load balancing
- Caching for API endpoints

## Running the Application

### Access Ports

After starting the application, you can access it using:

- **HTTP (Port 8087)**: `http://localhost:8087` - Will automatically redirect to HTTPS
- **HTTPS (Port 8443)**: `https://localhost:8443` - Main access point (use this in your browser)

**Note:** You'll need to accept the security warning for the self-signed certificate when accessing via HTTPS.

1. Navigate to the workshop directory:
```bash
cd 06-docker-compose
```

2. Build and start all services:
```bash
docker compose up --build
```

Or run in detached mode:
```bash
docker compose up -d --build
```

3. Check running containers:
```bash
docker compose ps
```

4. View logs:
```bash
# All services
docker compose logs -f

# Specific service
docker compose logs -f nginx
docker compose logs -f backend1
```

## Testing

1. Test HTTP redirect (will redirect to HTTPS):
```bash
curl -L http://localhost:8087
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
# HTTP (will redirect to HTTPS)
http://localhost:8087

# HTTPS (main access point)
https://localhost:8443
```
(Accept the security warning for self-signed certificate)

## Managing the Application

### Stop services:
```bash
docker compose down
```

### Stop and remove volumes:
```bash
docker compose down -v
```

### Restart a specific service:
```bash
docker compose restart nginx
```

### Scale backend instances:
```bash
docker compose up -d --scale backend1=2 --scale backend2=2 --scale backend3=2
```

### Execute commands in containers:
```bash
docker compose exec nginx nginx -t
docker compose exec backend1 python -c "import flask; print(flask.__version__)"
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
      - "8087:80"
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

## Troubleshooting

### Port Already in Use

If you get an error like `address already in use` for port 8087 or 8443:

**Option 1: Stop conflicting nginx services**
```bash
# Check what's using the port
sudo lsof -i :8087
sudo lsof -i :8443

# Stop system nginx (if running from previous workshop sections)
sudo systemctl stop nginx
# Or disable specific sites:
sudo rm /etc/nginx/sites-enabled/ssl-demo
sudo rm /etc/nginx/sites-enabled/caching-demo
sudo systemctl reload nginx
```

**Option 2: Change ports in docker-compose.yml**
```yaml
ports:
  - "8090:80"    # Change 8087 to 8090
  - "8444:443"   # Change 8443 to 8444
```

Then update your test commands to use the new ports.

**Option 3: Use different ports for Docker Compose**
If you're running multiple workshop sections simultaneously, use different ports:
- Section 02-05: Use port 8080
- Section 06 (Docker Compose): Use port 8087 (HTTP) and 8443 (HTTPS)

### Container Won't Start

1. Check logs:
```bash
docker compose logs nginx
docker compose logs backend1
```

2. Verify SSL certificates exist:
```bash
ls -la nginx/ssl/
# Should show nginx-demo.crt and nginx-demo.key
```

3. Test nginx configuration:
```bash
docker compose exec nginx nginx -t
```

### Backend Services Not Responding

1. Check if backends are running:
```bash
docker compose ps
```

2. Test backend directly:
```bash
docker compose exec backend1 curl http://localhost:5000/api/data
```

3. Check network connectivity:
```bash
docker compose exec nginx ping backend1
```

## Cleanup

```bash
# Stop and remove containers, networks
docker compose down

# Remove volumes as well
docker compose down -v

# Remove images
docker compose down --rmi all
```

## Next Steps

- Add environment variables for configuration
- Implement health checks
- Add monitoring and logging
- Set up CI/CD pipelines
- Deploy to production environments
