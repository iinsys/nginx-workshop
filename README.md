# nginx Workshop

A comprehensive workshop on nginx covering fundamental concepts and practical implementations. This repository contains both educational documentation and hands-on demonstration projects.

## Workshop Overview

This workshop is designed to introduce nginx step by step, from basic file serving to advanced configurations including reverse proxying, load balancing, SSL termination, and caching.

## Structure

This repository is organized into two main parts:

### Documentation (`docs/`)
Educational content covering nginx concepts, architecture, and best practices:
- [Introduction to nginx](./docs/01-introduction.md)
- [nginx Architecture](./docs/02-architecture.md)
- [Configuration Basics](./docs/03-configuration.md)
- [Core Concepts](./docs/04-concepts.md)

### Hands-on Demonstrations (Root Level)
Practical, runnable projects that you can clone and follow along:

1. **[01-serving-files](./01-serving-files/)** - Serve static files using nginx
2. **[02-reverse-proxy](./02-reverse-proxy/)** - Configure nginx as reverse proxy
3. **[03-load-balancer](./03-load-balancer/)** - Set up nginx as load balancer
4. **[04-ssl-termination](./04-ssl-termination/)** - Enable HTTPS with SSL termination
5. **[05-caching](./05-caching/)** - Implement caching strategies
6. **[06-docker-compose](./06-docker-compose/)** - Complete Docker Compose setup

## Getting Started

### Prerequisites

- Basic understanding of web servers and HTTP
- Command line familiarity
- nginx installed (instructions in each demo)
- Docker and Docker Compose installed (for demo 06)
- Python 3.x installed (for Flask backend applications)

### Quick Start

1. **Clone this repository:**
   ```bash
   git clone <repository-url>
   cd nginx-workshop
   ```

2. **Read the documentation:**
   Start with the [Introduction to nginx](./docs/01-introduction.md) to understand the fundamentals.

3. **Follow along with demos:**
   Each numbered directory contains a complete, runnable demonstration:
   ```bash
   cd 01-serving-files
   # Follow the README instructions
   ```

## Workshop Flow

1. **Read the docs** - Start with the documentation in `docs/` to understand concepts
2. **Try the demos** - Work through each numbered project to see nginx in action
3. **Experiment** - Modify configurations and see how nginx behaves

## Each Demo Includes

- Complete README with step-by-step instructions
- All necessary code files (Flask apps, HTML, etc.)
- nginx configuration files
- Installation commands
- Testing instructions
- Cleanup steps

## Topics Covered

- Static file serving
- Reverse proxy configuration
- Load balancing algorithms
- SSL/TLS termination
- Caching strategies
- Docker containerization

## Additional Resources

- [Presenter Guide](./PRESENTER_GUIDE.md) - Quick reference for workshop presenters
- [Official nginx Documentation](https://nginx.org/en/docs/)
- [nginx Beginner's Guide](https://nginx.org/en/docs/beginners_guide.html)

## Contributing

Feel free to fork this repository and customize it for your own workshops or learning purposes.

## License

See [LICENSE](./LICENSE) file for details.
