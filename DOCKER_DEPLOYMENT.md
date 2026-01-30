# Flask Portfolio Site - Docker Deployment Guide

## Overview
This project uses Docker, Nginx, and Gunicorn to run a production-ready Flask portfolio application.

### Components
- **Flask**: Web application framework
- **Gunicorn**: WSGI application server (4 workers for concurrent requests)
- **Nginx**: Reverse proxy and static file server (port 8000)
- **Docker**: Container orchestration

## Quick Start

### Build the Docker Image
```bash
docker build -t flask-portfolio:latest .
```

### Run with Docker Compose (Recommended)
```bash
docker-compose up -d
```

### Run with Docker CLI
```bash
docker run -d \
  --name flask_portfolio \
  -p 8000:8000 \
  -v $(pwd)/submissions.json:/app/submissions.json \
  -v $(pwd)/static:/app/static \
  -v $(pwd)/templates:/app/templates \
  --restart unless-stopped \
  flask-portfolio:latest
```

## Accessing the Application
- **Portfolio Site**: http://localhost:8000
- **Health Check**: http://localhost:8000/health
- **Contact Submissions**: http://localhost:8000/admin/submissions

## Configuration

### Environment Variables
Set these before building or running:
```bash
export FLASK_ENV=production
export FLASK_APP=main.py
```

### Nginx Configuration
The nginx config (`nginx.conf`) includes:
- Rate limiting (10 req/s general, 30 req/s API)
- Gzip compression
- Security headers (X-Frame-Options, X-Content-Type-Options, etc.)
- Static file caching (30 days)
- SSL-ready (uncomment for HTTPS in production)

### Gunicorn Configuration
- **Workers**: 4 (adjust based on CPU cores: `2 * cores + 1`)
- **Worker Type**: sync (suitable for I/O-bound tasks)
- **Bind Address**: 127.0.0.1:8001 (internal, proxied by nginx)
- **Timeout**: 60 seconds

## Logs
View application logs:
```bash
# With Docker Compose
docker-compose logs -f web

# With Docker CLI
docker logs -f flask_portfolio
```

Access logs:
```bash
docker exec flask_portfolio tail -f /var/log/nginx/access.log
docker exec flask_portfolio tail -f /var/log/nginx/error.log
docker exec flask_portfolio tail -f /var/log/nginx/gunicorn_access.log
```

## Production Deployment

### Enable HTTPS (SSL/TLS)
1. Uncomment the HTTP→HTTPS redirect in `nginx.conf`
2. Add SSL certificates to your Docker image or mount them as volumes
3. Update nginx config to listen on port 443 with ssl certificates

Example:
```bash
# Mount SSL certs
docker run -d \
  -p 80:80 \
  -p 443:443 \
  -v /path/to/cert.pem:/etc/nginx/cert.pem:ro \
  -v /path/to/key.pem:/etc/nginx/key.pem:ro \
  flask-portfolio:latest
```

### Scaling
To increase capacity, modify `docker-compose.yml` or adjust gunicorn workers:
```bash
# In Dockerfile CMD, change --workers=4 to --workers=8
```

### Database Integration
If adding a database:
1. Add service to `docker-compose.yml`
2. Update Flask app to connect
3. Mount data volumes for persistence

## Maintenance

### Stop the Container
```bash
docker-compose down
```

### Update Application
```bash
docker-compose down
docker build -t flask-portfolio:latest .
docker-compose up -d
```

### Clean Up
```bash
docker-compose down -v  # Remove volumes too
docker image rm flask-portfolio:latest
```

## Troubleshooting

### Port Already in Use
```bash
# Find process using port 8000
lsof -i :8000
# Kill it
kill -9 <PID>
```

### Permission Denied
The container runs as non-root user (uid 1000). Ensure volumes have correct permissions:
```bash
sudo chown -R 1000:1000 ./submissions.json
```

### Out of Memory
Increase Docker memory limit:
```bash
docker update --memory 2g flask_portfolio
```

## Performance Tuning

### Increase Gunicorn Workers
Recommended: `2 * CPU_CORES + 1`
```bash
# In Dockerfile CMD, update --workers=4
--workers=8  # for 4-core machine
```

### Nginx Caching
Adjust in nginx.conf:
```nginx
proxy_cache_valid 200 60m;  # Cache successful responses for 1 hour
```

### Load Balancing (Multiple Containers)
Use Docker Swarm or Kubernetes to run multiple instances behind a load balancer.

## Security Notes
- Never expose submissions API in production (add authentication)
- Use environment variables for sensitive config
- Run containers as non-root user (already configured)
- Enable HTTPS/SSL in production
- Consider using secrets management tools (Docker Secrets, HashiCorp Vault)

## Support
For issues or questions, check logs and ensure:
1. Docker daemon is running
2. Port 8000 is available
3. Required volumes exist and are readable
4. Flask app syntax is valid
