# Topic 1: Serving Files with nginx

This section demonstrates how to use nginx as a simple web server to serve static files.

## Learning Objectives

- Understand nginx basic configuration
- Learn how to serve static files
- Configure nginx to listen on specific ports
- Set up document root and index files

## Installation

### Ubuntu/Debian
```bash
sudo apt update
sudo apt install nginx -y
```

### CentOS/RHEL
```bash
sudo yum install nginx -y
```

### macOS
```bash
brew install nginx
```

### Start nginx Service
```bash
# Ubuntu/Debian
sudo systemctl start nginx
sudo systemctl enable nginx

# macOS
sudo nginx
```

## Configuration

1. Create a directory for our static files:
```bash
mkdir -p ~/nginx-demo/static
cd ~/nginx-demo/static
```

2. Create a simple HTML file:
```bash
cat > index.html << 'EOF'
<!DOCTYPE html>
<html>
<head>
    <title>nginx Static File Server</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 800px;
            margin: 50px auto;
            padding: 20px;
            background-color: #f4f4f4;
        }
        h1 {
            color: #333;
        }
        .info {
            background-color: white;
            padding: 20px;
            border-radius: 5px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }
    </style>
</head>
<body>
    <div class="info">
        <h1>Welcome to nginx Static File Server</h1>
        <p>This page is being served directly by nginx!</p>
        <p>nginx is serving static files from the document root.</p>
    </div>
</body>
</html>
EOF
```

3. Create nginx configuration:
```bash
sudo nano /etc/nginx/sites-available/static-demo
```

Add the following configuration:
```nginx
server {
    listen 8080;
    server_name localhost;
    
    root /home/YOUR_USERNAME/nginx-demo/static;
    index index.html;
    
    location / {
        try_files $uri $uri/ =404;
    }
}
```

Note: Replace `YOUR_USERNAME` with your actual username.

4. Enable the site (Ubuntu/Debian):
```bash
sudo ln -s /etc/nginx/sites-available/static-demo /etc/nginx/sites-enabled/
```

5. Test nginx configuration:
```bash
sudo nginx -t
```

6. Reload nginx:
```bash
sudo nginx -s reload
# or
sudo systemctl reload nginx
```

## Testing

Open your browser and navigate to:
```
http://localhost:8080
```

You should see the HTML page we created.

## Understanding the Configuration

- `listen 8080`: nginx listens on port 8080
- `server_name localhost`: Server name for this virtual host
- `root /path/to/files`: Directory containing files to serve
- `index index.html`: Default file to serve for directory requests
- `location /`: Block that handles all requests
- `try_files $uri $uri/ =404`: Try to serve the requested file, or return 404

## Exercises

1. Create additional HTML files and access them via browser
2. Create subdirectories and serve files from them
3. Change the port number and test
4. Modify the index file and see changes after reloading

## Cleanup

To remove this demo configuration:
```bash
sudo rm /etc/nginx/sites-enabled/static-demo
sudo nginx -s reload
```
