---
marp: true
theme: default
paginate: true
header: 'nginx Workshop'
footer: '© 2024 nginx Workshop'
style: |
  section {
    font-size: 28px;
  }
  h1 {
    color: #d73027;
    font-size: 48px;
  }
  h2 {
    color: #4575b4;
    font-size: 36px;
  }
  code {
    background-color: #f5f5f5;
    padding: 2px 6px;
    border-radius: 3px;
  }
  .columns {
    display: grid;
    grid-template-columns: repeat(2, minmax(0, 1fr));
    gap: 1rem;
  }
---

# nginx Workshop
## Comprehensive Guide to Web Server, Reverse Proxy & Load Balancing

**Presenter:** [Your Name]
**Date:** [Date]
**Duration:** ~2.5-3 hours

---

## Workshop Overview

- **Format:** Theory + Hands-on Demos
- **Duration:** ~2.5-3 hours
- **Structure:** 
  - Part 1: Theory (15-20 min)
  - Part 2: 6 Practical Demos (2-2.5 hours)
  - Q&A (15-20 min)

**What You'll Learn:**
- nginx fundamentals
- Reverse proxy configuration
- Load balancing
- SSL/TLS termination
- Caching strategies
- Docker containerization

---

## Repository Structure

```
nginx-workshop/
├── docs/              # Educational documentation
│   ├── 01-introduction.md
│   ├── 02-architecture.md
│   ├── 03-configuration.md
│   └── 04-concepts.md
│
└── 01-06/             # Hands-on demos
    ├── 01-serving-files/
    ├── 02-reverse-proxy/
    ├── 03-load-balancer/
    ├── 04-ssl-termination/
    ├── 05-caching/
    └── 06-docker-compose/
```

**Key Point:** Clone the repo - all files are ready to use!

---

## What is nginx?

**nginx** (pronounced "engine-x")
- High-performance web server
- Reverse proxy server
- Load balancer
- Created by Igor Sysoev (2004)
- Handles high concurrency with low memory

**Market Share:**
- Powers ~33% of all websites
- Used by Netflix, Dropbox, GitHub, WordPress.com

---

## Why nginx?

<div class="columns">

<div>

**Performance**
- Event-driven architecture
- Handles thousands of connections
- Low memory footprint
- Fast static file serving

</div>

<div>

**Flexibility**
- Web server
- Reverse proxy
- Load balancer
- SSL terminator
- Cache server

</div>

</div>

**Reliability**
- Production-tested
- Stable under high load
- Excellent error handling

---

## nginx Architecture

**Master-Worker Process Model**

```
Master Process
  ├── Worker 1 (handles connections)
  ├── Worker 2 (handles connections)
  └── Worker N (handles connections)
```

**Key Features:**
- One master process manages workers
- Each worker handles thousands of connections
- Event-driven, non-blocking I/O
- Efficient resource utilization

---

## Workshop Flow - Part 1: Theory

**Read Documentation** (15-20 min)

1. **Introduction to nginx** (`docs/01-introduction.md`)
   - What is nginx?
   - Why use nginx?
   - Installation overview

2. **Architecture** (`docs/02-architecture.md`)
   - Master-worker model
   - Event-driven architecture
   - Configuration structure

3. **Configuration Basics** (`docs/03-configuration.md`)
   - Directives and contexts
   - Server blocks
   - Location blocks

4. **Core Concepts** (`docs/04-concepts.md`)
   - Reverse proxy
   - Load balancing
   - SSL/TLS
   - Caching

---

## Workshop Flow - Part 2: Hands-on

**6 Practical Demonstrations**

1. **Serving Files** (15-20 min) - Basic setup
2. **Reverse Proxy** (20-25 min) - Flask integration
3. **Load Balancer** (25-30 min) - Multiple backends
4. **SSL Termination** (20-25 min) - HTTPS setup
5. **Caching** (20-25 min) - Performance optimization
6. **Docker Compose** (30-35 min) - Complete stack

**Break:** 10-15 min after Demo 3

---

## Demo 1: Serving Files
### Basic nginx Setup

**Location:** `01-serving-files/`

**What You'll Learn:**
- Basic nginx configuration
- Static file serving
- Configuration structure
- Symbolic links

**Port:** 8080

**Key Commands:**
```bash
sudo nginx -t          # Test configuration
sudo systemctl reload nginx  # Reload
```

---

## Demo 2: Reverse Proxy
### Frontend + Backend Integration

**Location:** `02-reverse-proxy/`

**What You'll Learn:**
- Flask backend setup
- `proxy_pass` directive
- Proxy headers (`X-Real-IP`, `X-Forwarded-For`)
- Frontend calling backend API

**Prerequisites:**
- Python 3.x, pip, Flask
- Use: `pip3 install -r requirements.txt`

**Port:** 8080

**Architecture:** Client → nginx → Flask Backend

---

## Demo 3: Load Balancer
### Multiple Backend Instances

**Location:** `03-load-balancer/`

**What You'll Learn:**
- Multiple Flask instances (3 backends)
- `upstream` block configuration
- Load balancing algorithms
- Interactive frontend visualization

**Port:** 8080

**Verification:**
- Command-line: `curl` with `jq`
- Interactive HTML: `http://localhost:8080`
- Watch requests distribute across backends

---

## Demo 4: SSL Termination
### HTTPS Configuration

**Location:** `04-ssl-termination/`

**What You'll Learn:**
- OpenSSL certificate generation
- HTTPS configuration
- HTTP → HTTPS redirect
- Security headers

**Prerequisites:** OpenSSL installed

**Ports:**
- HTTP: 8080 (redirects)
- HTTPS: 8443

**Key Point:** Generate certificates first!

---

## Demo 5: Caching
### Performance Optimization

**Location:** `05-caching/`

**What You'll Learn:**
- Cache zone setup
- Cache directives
- Cache status monitoring
- Performance comparison

**Port:** 8080

**Testing:**
- First request: `X-Cache-Status: MISS`
- Second request: `X-Cache-Status: HIT`
- Compare response times

**Analogy:** Library (cache) vs Bookstore (origin server)

---

## Demo 6: Docker Compose
### Complete Stack Deployment

**Location:** `06-docker-compose/`

**What You'll Learn:**
- Container orchestration
- Multi-service application
- Combining all concepts
- Production-like setup

**Prerequisites:**
- Docker installed
- Docker Compose v2 (`docker compose`, not `docker-compose`)

**Ports:**
- HTTP: **8087** (redirects to HTTPS)
- HTTPS: **8443** (main access)

---

## Demo 6: Critical Step
### Generate SSL Certificates First!

```bash
cd 06-docker-compose
mkdir -p nginx/ssl
cd nginx/ssl

# Generate private key
openssl genrsa -out nginx-demo.key 2048

# Generate certificate
openssl req -new -key nginx-demo.key \
  -out nginx-demo.csr -subj "/CN=localhost"

# Self-sign certificate
openssl x509 -req -days 365 \
  -in nginx-demo.csr -signkey nginx-demo.key \
  -out nginx-demo.crt

# Clean up and set permissions
rm nginx-demo.csr
chmod 600 nginx-demo.key
chmod 644 nginx-demo.crt
```

**IMPORTANT: Without certificates, nginx will fail to start!**

---

## Port Reference

| Demo | HTTP | HTTPS | Notes |
|------|------|-------|-------|
| 01 - Serving Files | 8080 | - | - |
| 02 - Reverse Proxy | 8080 | - | - |
| 03 - Load Balancer | 8080 | - | Interactive frontend |
| 04 - SSL Termination | 8080 | 8443 | Redirects HTTP→HTTPS |
| 05 - Caching | 8080 | - | - |
| 06 - Docker Compose | **8087** | **8443** | Different port |

**Note:** Demo 6 uses port 8087 to avoid conflicts

---

## Prerequisites Checklist

**Before Starting:**

- [ ] Repository cloned
- [ ] nginx installed
- [ ] Python 3.x installed
- [ ] pip/pip3 installed
- [ ] Flask (via `requirements.txt`)
- [ ] Docker installed (Demo 6)
- [ ] Docker Compose v2 (Demo 6)
- [ ] OpenSSL installed (Demo 4 & 6)

**All files are in the repository - no manual creation needed!**

---

## Common Commands

### nginx Management
```bash
sudo nginx -t              # Test configuration
sudo systemctl reload nginx # Reload config
sudo systemctl status nginx # Check status
```

### Python/Flask
```bash
pip3 install -r requirements.txt
python3 app.py
```

### Docker Compose (v2)
```bash
docker compose up --build
docker compose logs -f
docker compose down
```

**IMPORTANT: Use `docker compose` (space), not `docker-compose` (hyphen)**

---

## Troubleshooting: Port Conflicts

**Error:** `address already in use`

**Solution 1:** Stop conflicting service
```bash
sudo lsof -i :8080
sudo systemctl stop nginx
```

**Solution 2:** Change port in configuration
```yaml
# docker-compose.yml
ports:
  - "8090:80"  # Use different port
```

**Solution 3:** Disable specific nginx sites
```bash
sudo rm /etc/nginx/sites-enabled/ssl-demo
sudo systemctl reload nginx
```

---

## Troubleshooting: Missing Certificates

**Error:** `cannot load certificate: No such file or directory`

**Solution:** Generate SSL certificates first!

**For Demo 4:**
```bash
cd 04-ssl-termination/ssl/certs/
# Generate certificates (see README)
```

**For Demo 6:**
```bash
cd 06-docker-compose/nginx/ssl/
# Generate certificates (see previous slide)
```

---

## Testing Your Setup

### HTTP Endpoint
```bash
curl http://localhost:8080
curl -v http://localhost:8080  # Verbose headers
```

### HTTPS Endpoint
```bash
curl -k https://localhost:8443  # -k ignores cert warning
```

### Load Balancing
```bash
for i in {1..10}; do
  curl -s http://localhost:8080/api/data | jq
done
```

### Cache Status
```bash
curl -v http://localhost:8080/api/data | grep X-Cache-Status
```

---

## Key Concepts Summary

**Reverse Proxy:**
- Client → nginx → Backend Server
- Benefits: Security, SSL termination, load distribution

**Load Balancing:**
- Distribute requests across multiple backends
- Algorithms: round-robin, least_conn, ip_hash

**SSL Termination:**
- nginx handles SSL/TLS encryption
- Backend servers don't need SSL certificates

**Caching:**
- Store responses for faster delivery
- Reduces backend load
- Status: MISS, HIT, BYPASS

---

## Real-World Use Cases

**nginx is used by:**
- **Netflix** - Content delivery
- **GitHub** - Web serving and load balancing
- **WordPress.com** - Hosting millions of sites
- **Dropbox** - File serving
- **Cloudflare** - CDN and DDoS protection

**Common Scenarios:**
- API Gateway
- Microservices routing
- Static asset serving
- SSL termination
- Rate limiting

---

## Best Practices

**Configuration:**
- Test before reloading: `sudo nginx -t`
- Use symbolic links for site management
- Keep configurations organized
- Document custom configurations

**Security:**
- Use HTTPS in production
- Keep nginx updated
- Implement security headers
- Restrict access when needed

**Performance:**
- Enable caching for static content
- Use gzip compression
- Optimize worker processes
- Monitor performance metrics

---

## Time Management

| Section | Duration |
|---------|----------|
| Theory (docs/) | 15-20 min |
| Demo 1: Serving Files | 15-20 min |
| Demo 2: Reverse Proxy | 20-25 min |
| Demo 3: Load Balancer | 25-30 min |
| **Break** | **10-15 min** |
| Demo 4: SSL Termination | 20-25 min |
| Demo 5: Caching | 20-25 min |
| Demo 6: Docker Compose | 30-35 min |
| Q&A | 15-20 min |
| **Total** | **~2.5-3 hours** |

**Flexibility:** Demo 6 can be optional if time is limited

---

## Resources

**Official Documentation:**
- [nginx Documentation](https://nginx.org/en/docs/)
- [nginx Beginner's Guide](https://nginx.org/en/docs/beginners_guide.html)
- [Docker Compose Docs](https://docs.docker.com/compose/)

**Installation Guides:**
- Python: [python.org/downloads](https://www.python.org/downloads/)
- Flask: [flask.palletsprojects.com](https://flask.palletsprojects.com/)
- Docker: [docs.docker.com/engine/install](https://docs.docker.com/engine/install/)

**Workshop Repository:**
- Clone and follow along
- All files included
- Complete READMEs in each demo

---

## Key Takeaways

1. **nginx is versatile**
   - Web server, reverse proxy, load balancer, cache

2. **Configuration is simple**
   - Directive-based, readable syntax

3. **Production-ready**
   - Used by major companies worldwide

4. **Hands-on practice**
   - All demos are runnable and modifiable

5. **Real-world applicable**
   - Concepts translate to production environments

---

## Q&A Session

**Questions?**

**Contact:**
- Repository: [GitHub URL]
- Documentation: See `docs/` directory
- Presenter Guide: `PRESENTER_GUIDE.md`

**Follow-up:**
- Share repository link
- Provide additional resources
- Offer support for setup issues

---

## Thank You!

**Happy Learning!**

**Remember:**
- All files are in the repository
- Follow the READMEs step-by-step
- Experiment and modify configurations
- Practice makes perfect!

**Questions? Let's dive in!**

