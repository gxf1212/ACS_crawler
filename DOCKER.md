# Docker Deployment Guide

This guide explains how to run ACS Paper Crawler using Docker.

## Quick Start

```bash
# Clone the repository
git clone https://github.com/gxf1212/ACS_crawler.git
cd ACS_crawler

# Start with Docker Compose
docker-compose up -d

# Access the application
open http://localhost:8000
```

## Prerequisites

- **Docker**: 20.10 or higher ([Install Docker](https://docs.docker.com/get-docker/))
- **Docker Compose**: 2.0 or higher (included with Docker Desktop)

## Deployment Options

### Option 1: Docker Compose (Recommended)

Docker Compose provides the easiest deployment with automatic configuration.

**Start the application:**

```bash
docker-compose up -d
```

**View logs:**

```bash
docker-compose logs -f
```

**Stop the application:**

```bash
docker-compose down
```

**Restart after code changes:**

```bash
docker-compose up -d --build
```

### Option 2: Docker CLI

**Build the image:**

```bash
docker build -t acs-crawler:latest .
```

**Run the container:**

```bash
docker run -d \
  --name acs-crawler \
  -p 8000:8000 \
  -v $(pwd)/data:/app/data \
  -v $(pwd)/logs:/app/logs \
  --restart unless-stopped \
  acs-crawler:latest
```

**Manage the container:**

```bash
# View logs
docker logs -f acs-crawler

# Stop
docker stop acs-crawler

# Start
docker start acs-crawler

# Remove
docker rm -f acs-crawler
```

### Option 3: Pull from GitHub Container Registry

Once published, you can pull pre-built images:

```bash
# Pull latest image
docker pull ghcr.io/gxf1212/acs_crawler:latest

# Run container
docker run -d \
  --name acs-crawler \
  -p 8000:8000 \
  -v $(pwd)/data:/app/data \
  -v $(pwd)/logs:/app/logs \
  ghcr.io/gxf1212/acs_crawler:latest
```

## Configuration

### Environment Variables

Customize container behavior:

```bash
docker run -d \
  -e PYTHONUNBUFFERED=1 \
  -e CHROME_BIN=/usr/bin/google-chrome \
  -p 8000:8000 \
  acs-crawler:latest
```

### Port Configuration

Change the host port if 8000 is already in use:

```bash
# Use port 8080 instead
docker run -d -p 8080:8000 acs-crawler:latest
```

Or edit `docker-compose.yml`:

```yaml
ports:
  - "8080:8000"
```

### Volume Mounts

- `./data:/app/data` - Persist database
- `./logs:/app/logs` - Persist log files

### Resource Limits

Adjust in `docker-compose.yml`:

```yaml
deploy:
  resources:
    limits:
      cpus: '2'
      memory: 2G
    reservations:
      cpus: '1'
      memory: 1G
```

## Data Persistence

All data is stored in mounted volumes:

```
ACS_crawler/
├── data/              # Database (SQLite)
│   └── acs_papers.db
└── logs/              # Application logs
    └── acs_crawler.log
```

**Backup your data:**

```bash
# Backup database
cp data/acs_papers.db data/acs_papers.db.backup

# Or use Docker
docker exec acs-crawler sqlite3 /app/data/acs_papers.db ".backup '/app/data/backup.db'"
```

## Troubleshooting

### Container exits immediately

Check logs for errors:

```bash
docker logs acs-crawler
```

### Port already in use

Change the port mapping:

```bash
docker run -d -p 8080:8000 acs-crawler:latest
```

### Permission denied on data directory

Fix permissions:

```bash
sudo chown -R 1000:1000 data logs
```

### Chrome not working

Ensure you're using the provided Dockerfile which includes all Chrome dependencies.

### Out of memory

Increase memory limit in `docker-compose.yml`:

```yaml
deploy:
  resources:
    limits:
      memory: 4G
```

### Rebuild after code changes

```bash
# With docker-compose
docker-compose up -d --build

# With Docker CLI
docker build -t acs-crawler:latest . --no-cache
docker stop acs-crawler
docker rm acs-crawler
docker run -d --name acs-crawler -p 8000:8000 -v $(pwd)/data:/app/data acs-crawler:latest
```

## GitHub Container Registry Setup

To publish images to GHCR:

### 1. Enable GitHub Actions

The workflow file `.github/workflows/docker-publish.yml` is already configured.

### 2. Enable Package Permissions

1. Go to your repository on GitHub
2. Settings → Actions → General
3. Under "Workflow permissions", select:
   - ✅ Read and write permissions
   - ✅ Allow GitHub Actions to create and approve pull requests

### 3. Publish an Image

**Option A: Push to main branch**

```bash
git push origin main
```

**Option B: Create a release tag**

```bash
git tag v1.0.0
git push origin v1.0.0
```

The GitHub Action will automatically:
- Build the Docker image
- Push to `ghcr.io/gxf1212/acs_crawler:latest`
- Tag with version (if pushing a tag)

### 4. Make Package Public (Optional)

1. Go to https://github.com/gxf1212?tab=packages
2. Click on `acs_crawler` package
3. Package settings → Change visibility → Public

### 5. Pull the Published Image

```bash
docker pull ghcr.io/gxf1212/acs_crawler:latest
```

## Image Details

### Base Image
- Python 3.9 slim (Debian-based)
- Google Chrome (latest stable)
- ChromeDriver (auto-managed)

### Included Dependencies
- FastAPI
- Selenium
- BeautifulSoup4
- SQLite
- Uvicorn
- openpyxl

### Image Size
- Approximate size: ~1.2GB (compressed)
- Includes Chrome and all system dependencies

### Security
- Runs as non-root user (UID 1000)
- Minimal attack surface (slim base image)
- No unnecessary packages

### Health Check
- Endpoint: `http://localhost:8000/`
- Interval: 30s
- Timeout: 10s
- Retries: 3

## Production Deployment

### Using Docker Swarm

```bash
docker stack deploy -c docker-compose.yml acs-crawler
```

### Using Kubernetes

Create a deployment (example):

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: acs-crawler
spec:
  replicas: 1
  selector:
    matchLabels:
      app: acs-crawler
  template:
    metadata:
      labels:
        app: acs-crawler
    spec:
      containers:
      - name: acs-crawler
        image: ghcr.io/gxf1212/acs_crawler:latest
        ports:
        - containerPort: 8000
        volumeMounts:
        - name: data
          mountPath: /app/data
        - name: logs
          mountPath: /app/logs
      volumes:
      - name: data
        persistentVolumeClaim:
          claimName: acs-crawler-data
      - name: logs
        persistentVolumeClaim:
          claimName: acs-crawler-logs
```

### Reverse Proxy (Nginx)

```nginx
server {
    listen 80;
    server_name crawler.example.com;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

## Development

### Build for Development

```bash
docker build -t acs-crawler:dev .
docker run -d \
  --name acs-crawler-dev \
  -p 8000:8000 \
  -v $(pwd)/src:/app/src \
  -v $(pwd)/data:/app/data \
  acs-crawler:dev
```

### Interactive Shell

```bash
docker exec -it acs-crawler bash
```

### Run Tests

```bash
docker exec acs-crawler python -m pytest tests/
```

## Support

- 📚 [Full Documentation](https://acs-crawler.readthedocs.io/)
- 🐛 [Report Issues](https://github.com/gxf1212/ACS_crawler/issues)
- 💬 [Discussions](https://github.com/gxf1212/ACS_crawler/discussions)
