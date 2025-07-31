# Finance Management System - Docker Setup

This document provides instructions for running the Finance Management System using Docker.

## Prerequisites

- Docker installed on your system
- Docker Compose (usually comes with Docker Desktop)

## Quick Start

### Development Environment

1. **Build and run using Docker Compose:**
   ```bash
   docker-compose up --build
   ```

2. **Access the application:**
   - Open your browser and go to `http://localhost:5000`
   - Register a new account to get started

### Production Environment

1. **Set environment variables (optional):**
   ```bash
   export SECRET_KEY="your-secure-secret-key-here"
   ```

2. **Build and run using production Docker Compose:**
   ```bash
   docker-compose -f docker-compose.prod.yml up --build
   ```

## Manual Docker Commands

### Development Build
```bash
# Build the image
docker build -t finance-app .

# Run the container
docker run -p 5000:5000 -v $(pwd)/instance:/app/instance finance-app
```

### Production Build
```bash
# Build the production image
docker build -f Dockerfile.prod -t finance-app-prod .

# Run the production container
docker run -p 5000:5000 -v $(pwd)/instance:/app/instance finance-app-prod
```

## Docker Files Overview

- **`Dockerfile`** - Development Dockerfile using Flask's built-in server
- **`Dockerfile.prod`** - Production Dockerfile using Gunicorn WSGI server
- **`docker-compose.yml`** - Development environment with Docker Compose
- **`docker-compose.prod.yml`** - Production environment with Docker Compose
- **`.dockerignore`** - Excludes unnecessary files from Docker build context

## Features

### Security
- Non-root user execution
- Minimal base image (Python slim)
- Proper file permissions

### Performance
- Multi-stage build optimization
- Layer caching for faster builds
- Gunicorn for production (multiple workers)

### Monitoring
- Health checks included
- Proper logging configuration
- Resource limits in production

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `FLASK_APP` | Flask application entry point | `app.py` |
| `FLASK_ENV` | Flask environment | `production` |
| `SECRET_KEY` | Flask secret key | `your-secret-key-change-in-production` |
| `SQLALCHEMY_DATABASE_URI` | Database connection string | `sqlite:///finance.db` |

## Database Persistence

The SQLite database is stored in the `./instance` directory and is mounted as a volume to persist data between container restarts.

## Troubleshooting

### Common Issues

1. **Port already in use:**
   ```bash
   # Check what's using port 5000
   lsof -i :5000
   
   # Use a different port
   docker run -p 5001:5000 finance-app
   ```

2. **Permission issues:**
   ```bash
   # Ensure instance directory exists and has proper permissions
   mkdir -p instance
   chmod 755 instance
   ```

3. **Build failures:**
   ```bash
   # Clean up Docker cache
   docker system prune -a
   
   # Rebuild without cache
   docker-compose build --no-cache
   ```

### Logs
```bash
# View container logs
docker-compose logs finance-app

# Follow logs in real-time
docker-compose logs -f finance-app
```

## Stopping the Application

```bash
# Stop and remove containers
docker-compose down

# Stop and remove containers with volumes (WARNING: This will delete the database)
docker-compose down -v
```

## Production Deployment

For production deployment, consider:

1. **Environment Variables:** Set proper `SECRET_KEY` and other sensitive values
2. **Database:** Consider using PostgreSQL or MySQL instead of SQLite
3. **Reverse Proxy:** Use Nginx or Apache as a reverse proxy
4. **SSL/TLS:** Configure HTTPS certificates
5. **Monitoring:** Set up proper logging and monitoring solutions
6. **Backup:** Implement database backup strategies

## Example Production Setup with Nginx

```yaml
# docker-compose.prod.yml (extended)
version: '3.8'

services:
  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./ssl:/etc/nginx/ssl
    depends_on:
      - finance-app
    restart: unless-stopped

  finance-app:
    build:
      context: .
      dockerfile: Dockerfile.prod
    expose:
      - "5000"
    environment:
      - FLASK_APP=app.py
      - FLASK_ENV=production
      - SECRET_KEY=${SECRET_KEY}
    volumes:
      - ./instance:/app/instance
    restart: unless-stopped
```

This setup provides a complete Docker solution for both development and production environments for your Finance Management System. 