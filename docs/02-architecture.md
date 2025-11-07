# nginx Architecture

## Process Model

nginx uses a master-worker process architecture:

```mermaid
graph TB
    classDef control fill:#E8F1FC,stroke:#2F6CC0,color:#1A1A1A;
    classDef worker fill:#F4EFFF,stroke:#8256D8,color:#1A1A1A;
    classDef client fill:#EAF7F1,stroke:#4A9E6F,color:#1A1A1A;

    Master[Master Process<br/>- Reads configuration<br/>- Manages workers<br/>- Handles signals]
    
    Worker1[Worker Process 1<br/>Handles connections]
    Worker2[Worker Process 2<br/>Handles connections]
    Worker3[Worker Process 3<br/>Handles connections]
    WorkerN[Worker Process N<br/>Handles connections]
    
    Master --> Worker1
    Master --> Worker2
    Master --> Worker3
    Master --> WorkerN
    
    Client1[Client 1] --> Worker1
    Client2[Client 2] --> Worker1
    Client3[Client 3] --> Worker2
    Client4[Client 4] --> Worker2
    Client5[Client 5] --> Worker3
    ClientN[Client N] --> WorkerN

    class Master control;
    class Worker1,Worker2,Worker3,WorkerN worker;
    class Client1,Client2,Client3,Client4,Client5,ClientN client;
```


### Master Process

Responsibilities:
- Reads and validates configuration
- Opens socket listeners (ports 80, 443, etc.)
- Starts, stops, and manages worker processes
- Handles signals (reload, stop, reopen logs)
- Does NOT process client requests

### Worker Processes

Responsibilities:
- Handle client connections
- Process HTTP requests
- Serve static files
- Proxy requests to backends
- Execute load balancing logic

Key characteristics:
- Each worker is independent
- Workers share socket listeners (SO_REUSEPORT)
- Workers don't share memory (except shared memory zones)
- One worker can handle thousands of connections

## Event-Driven Model

### Traditional Process Model (Apache-like)

```
Connection → New Process/Thread → Process Request → Close
```

Problems:
- High memory usage (each connection = separate process/thread)
- Context switching overhead
- Limited scalability

### nginx Event Model

```mermaid
graph LR
    classDef legacy fill:#F5E8E7,stroke:#C75C5C,color:#1A1A1A;
    classDef modern fill:#E8F1FC,stroke:#2F6CC0,color:#1A1A1A;

    subgraph "Traditional Model (Apache-like)"
        Conn1[Connection 1]:::legacy --> Proc1[Process/Thread 1]:::legacy
        Conn2[Connection 2]:::legacy --> Proc2[Process/Thread 2]:::legacy
        Conn3[Connection 3]:::legacy --> Proc3[Process/Thread 3]:::legacy
        ConnN[Connection N]:::legacy --> ProcN[Process/Thread N]:::legacy
    end
    
    subgraph "nginx Event Model"
        Worker[Worker Process]:::modern
        EventLoop[Event Loop]:::modern
        
        ConnA[Connection 1<br/>non-blocking]:::modern --> EventLoop
        ConnB[Connection 2<br/>non-blocking]:::modern --> EventLoop
        ConnC[Connection 3<br/>non-blocking]:::modern --> EventLoop
        ConnD[Connection ...<br/>thousands]:::modern --> EventLoop
        
        EventLoop --> Worker
    end
```


Benefits:
- Single worker handles many connections
- Non-blocking I/O operations
- Efficient resource utilization
- High concurrency support

## Request Processing

### Request Lifecycle

```mermaid
graph TB
    classDef actor fill:#EAF7F1,stroke:#4A9E6F,color:#1A1A1A;
    classDef engine fill:#E8F1FC,stroke:#2F6CC0,color:#1A1A1A;
    classDef phase fill:#F8F1E3,stroke:#C29B27,color:#1A1A1A;
    classDef outcome fill:#F4EFFF,stroke:#8256D8,color:#1A1A1A;

    Client[Client Browser]:::actor -->|1. HTTP Request| Nginx[nginx Worker Process]:::engine
    
    Nginx -->|2. Read Headers| Phase1[POST_READ Phase]:::phase
    Phase1 -->|3. Server Rewrite| Phase2[SERVER_REWRITE Phase]:::phase
    Phase2 -->|4. Find Location| Phase3[FIND_CONFIG Phase]:::phase
    Phase3 -->|5. Location Rewrite| Phase4[REWRITE Phase]:::phase
    Phase4 -->|6. Access Control| Phase5[ACCESS Phase]:::phase
    Phase5 -->|7. Generate Content| Phase6[CONTENT Phase]:::phase
    
    Phase6 -->|8a. Serve Static File| Static[Static File Server]:::outcome
    Phase6 -->|8b. Proxy to Backend| Proxy[Backend Server]:::outcome
    Phase6 -->|8c. Load Balance| Upstream[Upstream Servers]:::outcome
    
    Static -->|9. Response| Nginx
    Proxy -->|9. Response| Nginx
    Upstream -->|9. Response| Nginx
    
    Nginx -->|10. Log Request| Phase7[LOG Phase]:::phase
    Phase7 -->|11. Send Response| Client:::actor
```


The request goes through these steps:
1. **Client connects** to nginx
2. **Worker accepts** connection (using event mechanism)
3. **Reads request** headers
4. **Processes request** based on configuration:
   - Serve static file
   - Proxy to backend
   - Apply caching logic
   - Load balancing decision
5. **Sends response** to client
6. **Closes connection** (or keeps alive for HTTP/1.1)

### Phases of Request Processing

nginx processes requests in phases:

1. **POST_READ:** Read client request headers
2. **SERVER_REWRITE:** Server-level URL rewriting
3. **FIND_CONFIG:** Find matching location block
4. **REWRITE:** Location-level URL rewriting
5. **POST_REWRITE:** After rewriting
6. **PREACCESS:** Before access control
7. **ACCESS:** Access control checks
8. **POST_ACCESS:** After access control
9. **PRECONTENT:** Before content generation
10. **CONTENT:** Generate content (serve file, proxy, etc.)
11. **LOG:** Log request

## Configuration Contexts

nginx configuration is organized in hierarchical contexts:

```mermaid
graph TD
    classDef root fill:#E8F1FC,stroke:#2F6CC0,color:#1A1A1A;
    classDef mid fill:#F4EFFF,stroke:#8256D8,color:#1A1A1A;
    classDef leaf fill:#EAF7F1,stroke:#4A9E6F,color:#1A1A1A;

    Main[Main Context<br/>Top-level configuration]:::root
    
    Events[Events Context<br/>Event model config]:::mid
    HTTP[HTTP Context<br/>HTTP server config]:::mid
    
    Upstream[Upstream Context<br/>Backend server groups]:::mid
    
    Server1[Server Block 1<br/>Virtual host 1]:::mid
    Server2[Server Block 2<br/>Virtual host 2]:::mid
    
    Loc1[Location /<br/>URL matching]:::leaf
    Loc2[Location /api/<br/>URL matching]:::leaf
    Loc3[Location /static/<br/>URL matching]:::leaf
    
    Main --> Events
    Main --> HTTP
    
    HTTP --> Upstream
    HTTP --> Server1
    HTTP --> Server2
    
    Server1 --> Loc1
    Server1 --> Loc2
    Server2 --> Loc3
```


Example structure:
```nginx
http {
    # HTTP-level directives
    
    upstream backend {
        # Upstream server definitions
    }
    
    server {
        # Server-level directives (virtual host)
        
        location / {
            # Location-level directives
        }
        
        location /api/ {
            # Another location block
        }
    }
}
```

### Context Types

- **Main:** Top-level configuration
- **Events:** Event model configuration
- **HTTP:** HTTP server configuration
- **Server:** Virtual host configuration
- **Location:** URL matching and processing
- **Upstream:** Backend server groups
- **Mail:** Mail proxy configuration (if enabled)
- **Stream:** TCP/UDP proxy configuration

## Connection Handling

### Connection Limits

- `worker_connections:` Maximum connections per worker
- Total connections = `worker_processes × worker_connections`

Example:
```nginx
worker_processes 4;
events {
    worker_connections 1024;
}
# Total: 4 × 1024 = 4096 connections
```

### Keep-Alive Connections

HTTP keep-alive allows multiple requests over a single connection:
- Reduces connection overhead
- Improves performance
- Controlled by `keepalive_timeout`

### Connection Queuing

When all workers are busy:
- New connections are queued
- Queue size: `listen` directive `backlog` parameter
- Default: Usually 511 connections

## Memory Management

### Memory Pools

nginx uses memory pools for efficient allocation:
- Allocations are grouped by request
- Entire pool freed when request completes
- Reduces memory fragmentation
- Fast allocation/deallocation

### Shared Memory

For data shared between workers:
- Cache zones
- Rate limiting zones
- Session storage
- Sticky sessions

## Performance Characteristics

### Why nginx is Fast

1. **Event-driven architecture:** Non-blocking I/O
2. **Efficient memory usage:** Memory pools, shared memory
3. **Optimized code:** Written in C
4. **Smart buffering:** Efficient data transfer
5. **Minimal context switching:** Single process per worker

### Typical Performance

- Can handle 10,000+ concurrent connections per worker
- Low memory usage: ~1-2 MB per 10,000 idle connections
- High throughput for static content
- Efficient reverse proxy performance

## Scalability

### Vertical Scaling

- Increase `worker_processes` (usually = CPU cores)
- Increase `worker_connections`
- Add more RAM

### Horizontal Scaling

- Run multiple nginx instances
- Use external load balancer
- DNS-based load balancing

## Security Architecture

### Process Isolation

- Workers run as unprivileged user
- Master process can run as root (for port binding)
- Workers dropped to non-root after startup

### Request Limits

- Connection limits per IP
- Request rate limiting
- Request size limits
- Timeout limits

## Next Steps

- Learn about [Configuration Basics](./03-configuration.md)
- Understand [Core Concepts](./04-concepts.md)
- Try [Demo 1: Serving Files](../01-serving-files/)
