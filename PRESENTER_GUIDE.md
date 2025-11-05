# nginx Workshop - Presenter Guide

Quick reference for conducting the nginx workshop.

## Repository Structure

- **`docs/`** - Educational documentation about nginx concepts
- **Root level numbered directories** - Hands-on demonstration projects

## Workshop Flow

### Part 1: Theory (15-20 min)
Start with documentation in `docs/`:
- Introduction to nginx
- Architecture overview
- Configuration basics
- Core concepts

### Part 2: Hands-on Demos

1. **Demo 1: Serving Files** (15-20 min)
   - Basic nginx setup
   - Static file serving
   - Configuration structure
   - Located in: `01-serving-files/`

2. **Demo 2: Reverse Proxy** (20-25 min)
   - Flask backend setup
   - Proxy configuration
   - Frontend + Backend integration
   - Located in: `02-reverse-proxy/`

3. **Demo 3: Load Balancer** (25-30 min)
   - Multiple backend instances
   - Upstream configuration
   - Load balancing algorithms
   - Failover demonstration
   - Located in: `03-load-balancer/`

4. **Demo 4: SSL Termination** (20-25 min)
   - Certificate generation
   - HTTPS configuration
   - HTTP to HTTPS redirect
   - Security headers
   - Located in: `04-ssl-termination/`

5. **Demo 5: Caching** (20-25 min)
   - Cache zone setup
   - Cache directives
   - Cache status monitoring
   - Performance comparison
   - Located in: `05-caching/`

6. **Demo 6: Docker Compose** (30-35 min)
   - Container orchestration
   - Complete stack deployment
   - Combining all concepts
   - Located in: `06-docker-compose/`

## Preparation Checklist

Before the workshop:
- [ ] Clone the repository: `git clone <repo-url> && cd nginx-workshop`
- [ ] Verify nginx is installed on demo machine
- [ ] Verify Python 3 and Flask are installed
- [ ] Verify Docker and Docker Compose are installed (for Demo 6)
- [ ] Test each demo project beforehand
- [ ] Prepare backup demo machine or VM if possible
- [ ] Review documentation in `docs/` directory
- [ ] Ensure audience can clone/fork the repository

## Common Commands Quick Reference

### nginx Management
```bash
# Test configuration
sudo nginx -t

# Reload configuration
sudo nginx -s reload
# or
sudo systemctl reload nginx

# Check status
sudo systemctl status nginx

# View error logs
sudo tail -f /var/log/nginx/error.log
```

### Flask Application
```bash
# Install Flask
pip3 install flask

# Run Flask app
python3 app.py

# Run on specific port
python3 app.py 5001
```

### Testing
```bash
# Test HTTP endpoint
curl http://localhost:8080

# Test with verbose headers
curl -v http://localhost:8080

# Test HTTPS (with self-signed cert)
curl -k https://localhost:8443

# Multiple requests for load balancing demo
for i in {1..10}; do curl -s http://localhost:8080; done
```

### Docker Compose
```bash
# Start services
docker-compose up -d --build

# View logs
docker-compose logs -f

# Stop services
docker-compose down

# Scale services
docker-compose up -d --scale backend1=3
```

## Common Issues and Solutions

### Port Already in Use
```bash
# Find process using port
sudo lsof -i :8080
# or
sudo netstat -tulpn | grep 8080

# Kill process
sudo kill -9 <PID>
```

### Permission Denied for nginx
```bash
# Check nginx user
ps aux | grep nginx

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
docker-compose logs

# Rebuild containers
docker-compose up --build --force-recreate

# Remove and recreate
docker-compose down -v
docker-compose up --build
```

## Demo Tips

1. **Live Coding**: Show configuration changes in real-time
2. **Before/After**: Compare response times, headers, etc.
3. **Visual Demos**: Use browser developer tools to show headers
4. **Load Testing**: Use curl loops to demonstrate load balancing
5. **Failover Demo**: Stop one backend and show nginx handling it
6. **Cache Demo**: Show MISS vs HIT in response headers

## Time Management

- Total workshop: ~2.5-3 hours
- Include 10-15 minute break after Topic 3
- Leave 15-20 minutes for Q&A at the end
- Topic 6 (Docker Compose) can be optional if time is limited

## Audience Engagement

- Ask questions: "Why do we need a reverse proxy?"
- Show practical benefits: performance, security, scalability
- Relate to real-world scenarios
- Encourage hands-on participation
- Provide time for exercises

## Resources for Participants

- Official nginx documentation: https://nginx.org/en/docs/
- nginx beginners guide: https://nginx.org/en/docs/beginners_guide.html
- Docker Compose documentation: https://docs.docker.com/compose/

## Post-Workshop

- Provide repository link
- Share slides (if any)
- Offer follow-up support
- Collect feedback
