# nginx Workshop - Presenter Guide

Quick reference for conducting the nginx workshop. Use this guide as your presentation notes.

---

## SLIDE 1: Workshop Overview

**Key Points:**
- Comprehensive nginx workshop covering fundamentals to advanced topics
- Hands-on demonstrations with real, runnable code
- Repository structure: `docs/` (theory) + numbered demos (practice)

**Duration:** ~2.5-3 hours
**Format:** Theory (15-20 min) + 6 Hands-on Demos

---

## SLIDE 2: Repository Structure

```
nginx-workshop/
├── docs/              # Educational documentation
│   ├── 01-introduction.md
│   ├── 02-architecture.md
│   ├── 03-configuration.md
│   └── 04-concepts.md
│
└── 01-06/             # Hands-on demonstration projects
    ├── 01-serving-files/
    ├── 02-reverse-proxy/
    ├── 03-load-balancer/
    ├── 04-ssl-termination/
    ├── 05-caching/
    └── 06-docker-compose/
```

**Key Point:** Audience will clone this repository and work directly with existing files.

---

## SLIDE 3: Workshop Flow

### Part 1: Theory (15-20 min)
**Start with documentation in `docs/`:**
- Introduction to nginx
- Architecture overview
- Configuration basics
- Core concepts

### Part 2: Hands-on Demos (2-2.5 hours)
1. Serving Files (15-20 min)
2. Reverse Proxy (20-25 min)
3. Load Balancer (25-30 min)
4. SSL Termination (20-25 min)
5. Caching (20-25 min)
6. Docker Compose (30-35 min)

**Break:** 10-15 minutes after Demo 3
**Q&A:** 15-20 minutes at the end

---

## SLIDE 4: Preparation Checklist

**Before the workshop, verify:**

- [ ] Repository cloned: `git clone <repo-url> && cd nginx-workshop`
- [ ] nginx installed on demo machine
- [ ] Python 3.x installed
- [ ] pip/pip3 installed
- [ ] Flask installed (or use `requirements.txt` in each demo)
- [ ] Docker installed (for Demo 6)
- [ ] Docker Compose v2 installed (use `docker compose`, not `docker-compose`)
- [ ] OpenSSL installed (for Demo 4 & 6)
- [ ] All demos tested beforehand
- [ ] Backup demo machine/VM prepared (if possible)
- [ ] Audience can clone/fork the repository

**Key Point:** All files are in the repository - no manual file creation needed!

---

## SLIDE 5: Demo 1 - Serving Files (15-20 min)

**Location:** `01-serving-files/`

**Key Concepts:**
- Basic nginx setup
- Static file serving
- Configuration structure
- Symbolic links (`ln -s`)

**Port:** 8080 (or as configured)

**Talking Points:**
- Explain what a web server does
- Show nginx configuration structure
- Demonstrate symbolic links for enabling sites

---

## SLIDE 6: Demo 2 - Reverse Proxy (20-25 min)

**Location:** `02-reverse-proxy/`

**Key Concepts:**
- Flask backend setup
- `proxy_pass` directive
- Proxy headers (`X-Real-IP`, `X-Forwarded-For`, etc.)
- Frontend + Backend integration
- Architecture diagram (Mermaid)

**Prerequisites:**
- Python 3.x, pip, Flask (installation instructions in README)
- Use `pip3 install -r requirements.txt`

**Port:** 8080

**Configuration File:** `/etc/nginx/sites-available/reverse-proxy-demo`

**Talking Points:**
- Why reverse proxy? (Security, load distribution, SSL termination)
- Show architecture diagram
- Explain proxy headers and their purpose
- Demonstrate frontend calling backend API

---

## SLIDE 7: Demo 3 - Load Balancer (25-30 min)

**Location:** `03-load-balancer/`

**Key Concepts:**
- Multiple backend instances (3 Flask apps)
- `upstream` block configuration
- Load balancing algorithms (round-robin, least_conn, ip_hash)
- Interactive frontend visualization
- Real-time request distribution

**Port:** 8080

**Configuration File:** `/etc/nginx/sites-available/load-balancer-demo`

**Verification Methods:**
- Command-line: `curl` with `jq` or `python3 -m json.tool`
- Interactive HTML frontend: `http://localhost:8080`
- Watch server hostnames change with each request

**Talking Points:**
- Why load balancing? (High availability, scalability)
- Show requests being distributed across backends
- Demonstrate failover (stop one backend)

---

## SLIDE 8: Demo 4 - SSL Termination (20-25 min)

**Location:** `04-ssl-termination/`

**Key Concepts:**
- OpenSSL certificate generation
- HTTPS configuration
- HTTP to HTTPS redirect
- Security headers
- Self-signed certificates

**Prerequisites:**
- OpenSSL installed (installation instructions in README)

**Ports:**
- HTTP: 8080 (redirects to HTTPS)
- HTTPS: 8443

**Configuration File:** `/etc/nginx/sites-available/ssl-demo`

**Important Steps:**
1. Generate SSL certificates in `04-ssl-termination/ssl/certs/`
2. Update nginx config with **absolute paths** to certificates
3. Use `sudo nano /etc/nginx/sites-available/ssl-demo` to edit

**Talking Points:**
- What is SSL/TLS? Why HTTPS?
- Explain self-signed vs CA-signed certificates
- Show security headers and their purpose

---

## SLIDE 9: Demo 5 - Caching (20-25 min)

**Location:** `05-caching/`

**Key Concepts:**
- Cache zone setup (`proxy_cache_path`)
- Cache directives (`proxy_cache`, `proxy_cache_valid`)
- Cache status monitoring (`X-Cache-Status` header)
- Cache states: MISS, HIT, BYPASS
- Performance comparison

**Port:** 8080

**Configuration File:** `/etc/nginx/sites-available/caching-demo`

**Testing:**
- First request: `X-Cache-Status: MISS`
- Second request: `X-Cache-Status: HIT`
- Show response time difference

**Talking Points:**
- What is caching? (Analogy: library vs bookstore)
- When to cache? (Static content, API responses)
- Show performance improvement with caching

---

## SLIDE 10: Demo 6 - Docker Compose (30-35 min)

**Location:** `06-docker-compose/`

**Key Concepts:**
- Container orchestration
- Multi-service application
- Combining all concepts (reverse proxy, load balancing, SSL, caching)
- Docker Compose v2 commands

**Prerequisites:**
- Docker installed
- Docker Compose v2 installed (`docker compose`, not `docker-compose`)

**Ports:**
- HTTP: **8087** (redirects to HTTPS)
- HTTPS: **8443** (main access point)

**CRITICAL STEP - Generate SSL Certificates First:**
```bash
cd 06-docker-compose
mkdir -p nginx/ssl
cd nginx/ssl
openssl genrsa -out nginx-demo.key 2048
openssl req -new -key nginx-demo.key -out nginx-demo.csr -subj "/CN=localhost"
openssl x509 -req -days 365 -in nginx-demo.csr -signkey nginx-demo.key -out nginx-demo.crt
rm nginx-demo.csr
chmod 600 nginx-demo.key
chmod 644 nginx-demo.crt
```

**Configuration Files:**
- `docker-compose.yml` - Service definitions
- `nginx/nginx.conf` - nginx configuration
- All files already in repository

**Commands:**
```bash
# Start services
docker compose up --build

# View logs
docker compose logs -f

# Stop services
docker compose down
```

**Talking Points:**
- Benefits of containerization
- Service isolation and networking
- Complete production-like setup

---

## SLIDE 11: Common Commands Quick Reference

### nginx Management
```bash
# Test configuration
sudo nginx -t

# Reload configuration
sudo systemctl reload nginx

# Check status
sudo systemctl status nginx

# View error logs
sudo tail -f /var/log/nginx/error.log
```

### Python/Flask
```bash
# Install dependencies
pip3 install -r requirements.txt

# Run Flask app
python3 app.py

# Run on specific port
PORT=5001 python3 app.py
```

### Testing
```bash
# Test HTTP endpoint
curl http://localhost:8080

# Test with verbose headers
curl -v http://localhost:8080

# Test HTTPS (with self-signed cert)
curl -k https://localhost:8443

# Multiple requests for load balancing
for i in {1..10}; do curl -s http://localhost:8080/api/data | jq; done
```

### Docker Compose (v2)
```bash
# Start services
docker compose up --build

# Start in detached mode
docker compose up -d --build

# View logs
docker compose logs -f

# Stop services
docker compose down

# Stop and remove volumes
docker compose down -v
```

**IMPORTANT:** Use `docker compose` (space, v2) not `docker-compose` (hyphen, v1)

---

## SLIDE 12: Common Issues and Solutions

### Port Already in Use
```bash
# Find process using port
sudo lsof -i :8080
sudo lsof -i :8087  # For Docker Compose

# Stop system nginx
sudo systemctl stop nginx

# Or disable specific sites
sudo rm /etc/nginx/sites-enabled/ssl-demo
sudo systemctl reload nginx
```

### Permission Denied
```bash
# Fix permissions
sudo chown -R www-data:www-data /var/www/
sudo chmod -R 755 /var/www/
```

### Configuration Syntax Error
```bash
# Test configuration
sudo nginx -t

# Check error log
sudo tail -f /var/log/nginx/error.log
```

### Docker Containers Not Starting
```bash
# Check logs
docker compose logs nginx

# Rebuild containers
docker compose up --build --force-recreate

# Verify SSL certificates exist
ls -la 06-docker-compose/nginx/ssl/
```

### Missing SSL Certificates (Demo 6)
**Error:** `cannot load certificate: No such file or directory`

**Solution:** Generate certificates first (see Demo 6 slide)

---

## SLIDE 13: Demo Tips & Best Practices

**Live Coding:**
- Show configuration changes in real-time
- Use `sudo nginx -t` before reloading
- Show before/after comparisons

**Visual Demonstrations:**
- Use browser developer tools to show headers
- Show `X-Cache-Status` header changes
- Display load balancing in action (frontend visualization)

**Load Testing:**
- Use curl loops: `for i in {1..10}; do curl ...; done`
- Show requests being distributed across backends
- Demonstrate failover by stopping one backend

**Cache Demonstration:**
- First request: Show `X-Cache-Status: MISS`
- Second request: Show `X-Cache-Status: HIT`
- Compare response times

**Engagement:**
- Ask questions: "Why do we need a reverse proxy?"
- Show practical benefits: performance, security, scalability
- Relate to real-world scenarios

---

## SLIDE 14: Port Reference

| Demo | HTTP Port | HTTPS Port | Notes |
|------|-----------|------------|-------|
| 01 - Serving Files | 8080 | - | - |
| 02 - Reverse Proxy | 8080 | - | - |
| 03 - Load Balancer | 8080 | - | Interactive frontend |
| 04 - SSL Termination | 8080 | 8443 | Redirects HTTP→HTTPS |
| 05 - Caching | 8080 | - | - |
| 06 - Docker Compose | **8087** | **8443** | Different port to avoid conflicts |

**Key Point:** Demo 6 uses port 8087 to avoid conflicts with other demos.

---

## SLIDE 15: Resources for Participants

**Official Documentation:**
- [nginx Documentation](https://nginx.org/en/docs/)
- [nginx Beginner's Guide](https://nginx.org/en/docs/beginners_guide.html)
- [Docker Compose Documentation](https://docs.docker.com/compose/)

**Installation Guides:**
- Python 3.x: [python.org/downloads](https://www.python.org/downloads/)
- pip: [pip.pypa.io](https://pip.pypa.io/en/stable/installation/)
- Flask: [flask.palletsprojects.com](https://flask.palletsprojects.com/)
- Docker: [docs.docker.com/engine/install](https://docs.docker.com/engine/install/)
- OpenSSL: Included in most Linux distributions

**Workshop Repository:**
- Clone and follow along
- All files included - no manual creation needed
- Each demo has complete README with instructions

---

## SLIDE 16: Time Management

**Total Workshop:** ~2.5-3 hours

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

**Flexibility:**
- Demo 6 (Docker Compose) can be optional if time is limited
- Can skip some demos and focus on specific topics
- Adjust timing based on audience level

---

## SLIDE 17: Audience Engagement Tips

**Opening Questions:**
- "Who has used nginx before?"
- "What problems does a reverse proxy solve?"
- "Why do we need load balancing?"

**During Demos:**
- Encourage hands-on participation
- Have audience follow along on their machines
- Pause for questions after each demo
- Show real-world use cases

**Interactive Elements:**
- Load balancer frontend visualization
- Browser developer tools for headers
- Live configuration changes
- Performance comparisons

**Closing:**
- Summarize key concepts
- Provide repository link
- Offer follow-up support
- Collect feedback

---

## SLIDE 18: Post-Workshop Checklist

- [ ] Provide repository link to participants
- [ ] Share any additional slides/resources
- [ ] Offer follow-up support (email, chat, etc.)
- [ ] Collect feedback (what worked, what didn't)
- [ ] Share solutions to any issues encountered
- [ ] Provide certificate of completion (if applicable)

---

## Key Takeaways for Audience

1. **nginx is versatile:** Web server, reverse proxy, load balancer, SSL terminator, cache
2. **Configuration is simple:** Directive-based, readable syntax
3. **Production-ready:** Used by major companies worldwide
4. **Hands-on practice:** All demos are runnable and modifiable
5. **Real-world applicable:** Concepts translate directly to production environments

---

## Support & Contact

**During Workshop:**
- Monitor for common issues (ports, permissions, certificates)
- Have troubleshooting commands ready
- Keep backup demo machine ready if possible

**After Workshop:**
- Provide repository access
- Answer follow-up questions
- Share additional resources

---

**Last Updated:** Based on latest repository changes
**Version:** Includes Docker Compose v2, updated ports, certificate generation requirements
