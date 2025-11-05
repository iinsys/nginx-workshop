# Introduction to nginx

## What is nginx?

nginx (pronounced "engine-x") is a high-performance web server, reverse proxy server, and load balancer. It was created by Igor Sysoev and first released in 2004. nginx is designed to handle high concurrency with low memory usage.

## Why nginx?

### Performance
- Event-driven, asynchronous architecture
- Handles thousands of concurrent connections with minimal memory
- Efficient resource utilization

### Flexibility
- Can serve as web server, reverse proxy, load balancer
- Extensive configuration options
- Modular architecture with third-party modules

### Reliability
- Stable and production-tested
- Handles high traffic loads
- Excellent error handling and logging

### Popular Use Cases
- Serving static content
- Reverse proxying to application servers
- Load balancing across multiple backends
- SSL/TLS termination
- Content caching
- API gateway

## nginx vs Other Web Servers

### nginx vs Apache

**nginx:**
- Event-driven model
- Lower memory usage per connection
- Better at handling static content
- Simpler configuration for reverse proxy

**Apache:**
- Process/thread-based model
- More modules available
- .htaccess support (per-directory config)
- Better for complex server-side processing

### When to Use nginx

- High-traffic websites
- Static content serving
- Reverse proxy/load balancing needs
- Resource-constrained environments
- Modern web applications (API-first)

## Core Features

### 1. Web Server
Serve static files (HTML, CSS, JavaScript, images, etc.) directly to clients.

### 2. Reverse Proxy
Forward client requests to backend servers and return responses.

### 3. Load Balancer
Distribute incoming requests across multiple backend servers.

### 4. SSL Termination
Handle HTTPS connections, decrypting traffic before forwarding to backends.

### 5. Caching
Store frequently accessed content to reduce backend load and improve response times.

## nginx Architecture

### Master-Worker Process Model

nginx uses a master process that manages one or more worker processes:

- **Master Process:** Reads configuration, manages worker processes
- **Worker Processes:** Handle actual request processing
- Each worker can handle thousands of concurrent connections
- Workers are independent and don't share memory

### Event-Driven Architecture

- Uses epoll (Linux), kqueue (BSD), or select (fallback)
- Non-blocking I/O operations
- Efficient connection handling
- Low memory footprint

## Installation Overview

nginx can be installed on various platforms:

- **Linux:** Package managers (apt, yum, dnf)
- **macOS:** Homebrew
- **Windows:** Official binaries available
- **Docker:** Official nginx images

Specific installation instructions are provided in each demonstration project.

## Configuration Overview

nginx configuration is stored in text files, typically:
- Main config: `/etc/nginx/nginx.conf`
- Site configs: `/etc/nginx/sites-available/` and `/etc/nginx/sites-enabled/`
- Module configs: `/etc/nginx/conf.d/`

Configuration syntax is:
- Directive-based
- Context-based (http, server, location blocks)
- Simple and readable

## Next Steps

Now that you understand what nginx is, you can:

1. Read about [nginx Architecture](./02-architecture.md)
2. Learn [Configuration Basics](./03-configuration.md)
3. Start with [Demo 1: Serving Files](../01-serving-files/)
