# Docker Deployment Guide

## Quick Start

### Using Pre-built Image (PyPI)

```bash
# Pull and run admin panel only
docker run -d \
  -p 5000:5000 \
  -v $(pwd)/config.json:/app/config.json \
  -v $(pwd)/logs:/app/logs \
  --name ept-mx-admin \
  ghcr.io/eptllc/ept-mx-adm:latest
```

### Full Stack (Admin Panel + Synapse + PostgreSQL)

```bash
# Clone repository
git clone https://github.com/EPTLLC/EPT-MX-ADM.git
cd EPT-MX-ADM

# Start all services
docker-compose up -d

# Check status
docker-compose ps

# View logs
docker-compose logs -f admin-panel

# Access admin panel
open http://localhost:5000
```

## Configuration

### Synapse Initial Setup

First time running Synapse requires generating configuration:

```bash
# Generate Synapse config
docker run -it --rm \
  -v $(pwd)/docker/synapse:/data \
  -e SYNAPSE_SERVER_NAME=localhost \
  -e SYNAPSE_REPORT_STATS=no \
  matrixdotorg/synapse:latest generate

# Create admin user
docker exec -it ept-mx-synapse \
  register_new_matrix_user \
  -u admin \
  -p your_password \
  -a \
  -c /data/homeserver.yaml \
  http://localhost:8008
```

### Admin Panel Configuration

Edit `config.json`:

```json
{
  "matrix_server": "http://synapse:8008",
  "debug": false,
  "language": "en"
}
```

## Services

| Service | Port | URL |
|---------|------|-----|
| Admin Panel | 5000 | http://localhost:5000 |
| Synapse API | 8008 | http://localhost:8008 |
| Synapse Federation | 8448 | https://localhost:8448 |

## Environment Variables

### Admin Panel

| Variable | Default | Description |
|----------|---------|-------------|
| `SYNAPSE_URL` | http://synapse:8008 | Synapse server URL |
| `FLASK_ENV` | production | Flask environment |
| `DEBUG` | false | Debug mode |

### Synapse

| Variable | Default | Description |
|----------|---------|-------------|
| `SYNAPSE_SERVER_NAME` | localhost | Server domain |
| `SYNAPSE_REPORT_STATS` | no | Report statistics |

### PostgreSQL

| Variable | Default | Description |
|----------|---------|-------------|
| `POSTGRES_USER` | synapse | Database user |
| `POSTGRES_PASSWORD` | synapse_password | Database password |
| `POSTGRES_DB` | synapse | Database name |

## Volumes

```yaml
volumes:
  postgres_data:       # PostgreSQL data
  ./docker/synapse:/data  # Synapse configuration
  ./config.json:/app/config.json  # Admin panel config
  ./logs:/app/logs     # Application logs
```

## Health Checks

All services have health checks configured:

```bash
# Check all services
docker-compose ps

# Check specific service
docker inspect --format='{{json .State.Health}}' ept-mx-admin | jq
```

## Useful Commands

```bash
# Start services
docker-compose up -d

# Stop services
docker-compose down

# Stop and remove volumes
docker-compose down -v

# Restart service
docker-compose restart admin-panel

# View logs
docker-compose logs -f

# Update images
docker-compose pull
docker-compose up -d

# Enter container
docker exec -it ept-mx-admin /bin/bash

# Check resource usage
docker stats

# Backup database
docker exec ept-mx-postgres pg_dump -U synapse synapse > backup.sql

# Restore database
docker exec -i ept-mx-postgres psql -U synapse synapse < backup.sql
```

## Production Deployment

### Security Recommendations

1. **Use strong passwords**
   ```yaml
   environment:
     POSTGRES_PASSWORD: $(openssl rand -base64 32)
   ```

2. **Use secrets management**
   ```yaml
   secrets:
     postgres_password:
       external: true
   ```

3. **Enable HTTPS**
   - Use reverse proxy (Nginx/Traefik)
   - Add SSL certificates
   - Update `SYNAPSE_URL` to use `https://`

4. **Restrict network access**
   ```yaml
   networks:
     matrix-network:
       internal: true
   ```

5. **Set resource limits**
   ```yaml
   deploy:
     resources:
       limits:
         cpus: '2'
         memory: 2G
       reservations:
         cpus: '0.5'
         memory: 512M
   ```

### Reverse Proxy Example (Nginx)

```nginx
server {
    listen 443 ssl http2;
    server_name admin.example.com;

    ssl_certificate /etc/ssl/certs/cert.pem;
    ssl_certificate_key /etc/ssl/private/key.pem;

    location / {
        proxy_pass http://localhost:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

## Troubleshooting

### Admin panel can't connect to Synapse

```bash
# Check if Synapse is running
docker-compose logs synapse

# Check network connectivity
docker exec ept-mx-admin curl http://synapse:8008/health

# Verify config
docker exec ept-mx-admin cat config.json
```

### Database connection errors

```bash
# Check PostgreSQL
docker-compose logs postgres

# Verify connection
docker exec ept-mx-postgres psql -U synapse -c "SELECT 1"
```

### Permission issues

```bash
# Fix ownership
docker exec -u root ept-mx-admin chown -R matrix-admin:matrix-admin /app/logs
```

## Monitoring

### Prometheus Metrics

Add to `docker-compose.yml`:

```yaml
  prometheus:
    image: prom/prometheus
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml
    ports:
      - "9090:9090"

  grafana:
    image: grafana/grafana
    ports:
      - "3000:3000"
    depends_on:
      - prometheus
```

## Building Custom Image

```bash
# Build
docker build -t ept-mx-adm:custom .

# Build with specific version
docker build -t ept-mx-adm:1.0.1 .

# Build with no cache
docker build --no-cache -t ept-mx-adm:latest .
```

## Multi-stage Build (Optimization)

For production, consider multi-stage build:

```dockerfile
FROM python:3.10-slim as builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

FROM python:3.10-slim
WORKDIR /app
COPY --from=builder /root/.local /root/.local
COPY . .
ENV PATH=/root/.local/bin:$PATH
CMD ["gunicorn", "app:app"]
```

---

**Documentation:**
- [Docker Documentation](https://docs.docker.com/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [Synapse Docker Documentation](https://matrix-org.github.io/synapse/latest/setup/installation.html#docker)

