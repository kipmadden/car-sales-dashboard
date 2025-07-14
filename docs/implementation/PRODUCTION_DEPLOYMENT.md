# Production Deployment Guide

This guide provides comprehensive instructions for deploying the Car Sales Dashboard to production environments.

## 🎯 Quick Start

### Prerequisites
- Docker & Docker Compose installed
- 2GB+ RAM available
- 10GB+ disk space
- Network access to ports 80, 443, 3000, 8000, 6379

### 1-Minute Deployment
```bash
# Clone repository
git clone https://github.com/kipmadden/car-sales-dashboard.git
cd car-sales-dashboard

# Configure environment
cp .env.production.template .env.production
# Edit .env.production with your settings

# Deploy
./deploy.sh
```

Windows users: Use `deploy.bat` instead.

## 🔧 Configuration

### Environment Variables (.env.production)
Copy `.env.production.template` to `.env.production` and customize:

```env
# Required Settings
SECRET_KEY=your-secure-secret-key-here
CORS_ALLOWED_ORIGINS=["https://yourdomain.com"]
ALLOWED_HOSTS=["yourdomain.com", "localhost"]

# Optional Settings
SENTRY_DSN=your-sentry-dsn-for-error-tracking
REDIS_URL=redis://localhost:6379/0
LOG_LEVEL=INFO
```

### SSL/TLS Setup
1. Place SSL certificates in `./ssl/` directory:
   - `server.crt` - SSL certificate
   - `server.key` - Private key

2. Update `config/nginx.conf` with your domain names

3. Enable production profile:
   ```bash
   docker-compose --profile production up -d
   ```

## 🚀 Deployment Options

### Option 1: Standard Deployment (Recommended)
```bash
./deploy.sh
```
- Includes: App + Redis
- Ports: 3000 (frontend), 8000 (backend), 6379 (redis)
- Best for: Development, testing, simple production

### Option 2: Production with Nginx
```bash
docker-compose --profile production up -d
```
- Includes: App + Redis + Nginx reverse proxy
- Ports: 80 (HTTP), 443 (HTTPS), 6379 (redis)
- Best for: Production with SSL termination

### Option 3: Manual Docker Commands
```bash
# Build
docker-compose build

# Start services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

## 📊 Monitoring & Health Checks

### Health Endpoints
- **Simple**: `GET /health` → Returns "OK"
- **Detailed**: `GET /healthz` → Returns system status, timestamp, version

### Monitoring Integration
The application supports:
- **Sentry** for error tracking
- **Prometheus** metrics (via `/metrics` endpoint)
- **Structured logging** to files and stdout

### Log Files
- General logs: `./logs/dashboard.log`
- Error logs: `./logs/dashboard_errors.log`
- Deployment logs: `./logs/deployment.log`

## 🔍 Troubleshooting

### Common Issues

#### 1. SSL Certificate Errors
```bash
# Fix SSL_CERT_FILE path
export SSL_CERT_FILE=$(python -c "import certifi; print(certifi.where())")
```

#### 2. Port Already in Use
```bash
# Check what's using the port
netstat -tulpn | grep :3000

# Stop conflicting services
sudo systemctl stop apache2  # or nginx, etc.
```

#### 3. Memory Issues
```bash
# Check memory usage
docker stats

# Restart with more memory
docker-compose down
docker-compose up -d
```

#### 4. Redis Connection Issues
```bash
# Check Redis status
docker-compose exec redis redis-cli ping

# Restart Redis
docker-compose restart redis
```

### Debug Mode
Enable debug logging:
```bash
# In .env.production
LOG_LEVEL=DEBUG
DEBUG=True
```

### Service Status
```bash
# Check all services
./deploy.sh status

# Check specific service
docker-compose ps app
```

## 🔄 Updates & Maintenance

### Updating the Application
```bash
# Pull latest changes
git pull origin main

# Backup current deployment
./deploy.sh backup

# Deploy updates
./deploy.sh
```

### Database Migrations
```bash
# If using external database
docker-compose exec app python -m alembic upgrade head
```

### Backup Data
```bash
# Manual backup
mkdir -p backups/$(date +%Y%m%d)
cp -r data logs backups/$(date +%Y%m%d)/

# Automated backup (add to cron)
0 2 * * * /path/to/car-sales-dashboard/deploy.sh backup
```

## 🛡️ Security Considerations

### Production Checklist
- [ ] Change default `SECRET_KEY`
- [ ] Set proper `ALLOWED_HOSTS`
- [ ] Configure CORS origins
- [ ] Enable SSL/TLS certificates
- [ ] Set up firewall rules
- [ ] Enable fail2ban (if applicable)
- [ ] Regular security updates
- [ ] Monitor error logs
- [ ] Set up automated backups

### Network Security
```bash
# Recommended firewall rules (ufw example)
sudo ufw allow 22    # SSH
sudo ufw allow 80    # HTTP
sudo ufw allow 443   # HTTPS
sudo ufw deny 3000   # Block direct frontend access
sudo ufw deny 8000   # Block direct backend access
sudo ufw deny 6379   # Block direct Redis access
sudo ufw enable
```

## 📈 Performance Optimization

### Resource Limits
Adjust in `docker-compose.yml`:
```yaml
services:
  app:
    deploy:
      resources:
        limits:
          memory: 1G
          cpus: '0.5'
        reservations:
          memory: 512M
          cpus: '0.25'
```

### Scaling
```bash
# Scale application instances
docker-compose up -d --scale app=3

# Load balance with nginx
# (configure upstream servers in nginx.conf)
```

## 🌐 Cloud Deployment

### AWS ECS/Fargate
1. Push image to ECR
2. Create ECS task definition
3. Deploy to Fargate cluster

### Azure Container Instances
```bash
az container create \
  --resource-group myResourceGroup \
  --name car-sales-dashboard \
  --image myregistry.azurecr.io/car-sales-dashboard:latest
```

### Google Cloud Run
```bash
gcloud run deploy car-sales-dashboard \
  --image gcr.io/project-id/car-sales-dashboard \
  --platform managed
```

## 📞 Support

### Getting Help
1. Check logs: `docker-compose logs -f`
2. Verify health: `curl http://localhost:3000/health`
3. Review configuration: `.env.production`
4. Check system resources: `docker stats`

### Reporting Issues
Include in your report:
- Deployment method used
- Operating system and versions
- Error logs from `./logs/`
- Docker/Docker Compose versions
- Hardware specifications

---

**Last Updated**: July 13, 2025  
**Version**: 1.0.0
