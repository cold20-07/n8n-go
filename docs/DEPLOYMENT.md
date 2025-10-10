# Deployment Guide

## Quick Deployment Options

### 1. Vercel (Recommended for Frontend)
```bash
# Install Vercel CLI
npm i -g vercel

# Deploy
vercel --prod
```

### 2. Docker
```bash
# Build image
docker build -t n8n-generator .

# Run container
docker run -p 5000:5000 --env-file .env.production n8n-generator
```

### 3. Traditional Server
```bash
# Install dependencies
pip install -r requirements.txt
npm install

# Set environment
export FLASK_ENV=production

# Run with Gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

## Detailed Deployment Instructions

### Prerequisites
- Python 3.8+
- Node.js 14+
- Redis (for production caching/rate limiting)
- SSL certificate (for HTTPS)

### Environment Setup

1. **Copy environment file**:
   ```bash
   cp .env.production .env
   ```

2. **Configure environment variables**:
   ```bash
   # Required
   SECRET_KEY=your-super-secure-secret-key
   GEMINI_API_KEY=your-gemini-api-key
   
   # Optional but recommended
   OPENAI_API_KEY=your-openai-api-key
   CLAUDE_API_KEY=your-claude-api-key
   REDIS_URL=redis://localhost:6379
   ```

### Vercel Deployment

1. **Install Vercel CLI**:
   ```bash
   npm install -g vercel
   ```

2. **Configure vercel.json** (already included):
   ```json
   {
     "functions": {
       "app.py": {
         "runtime": "python3.9"
       }
     },
     "routes": [
       { "src": "/api/(.*)", "dest": "/app.py" },
       { "src": "/(.*)", "dest": "/public/$1" }
     ]
   }
   ```

3. **Deploy**:
   ```bash
   vercel --prod
   ```

4. **Set environment variables** in Vercel dashboard

### Docker Deployment

1. **Build image**:
   ```bash
   docker build -t n8n-generator .
   ```

2. **Run with Docker Compose**:
   ```bash
   docker-compose -f docker-compose.yml up -d
   ```

3. **Or run standalone**:
   ```bash
   docker run -d \
     --name n8n-generator \
     -p 5000:5000 \
     --env-file .env.production \
     n8n-generator
   ```

### Traditional Server Deployment

1. **Install system dependencies**:
   ```bash
   # Ubuntu/Debian
   sudo apt update
   sudo apt install python3 python3-pip nodejs npm redis-server nginx
   
   # CentOS/RHEL
   sudo yum install python3 python3-pip nodejs npm redis nginx
   ```

2. **Install application dependencies**:
   ```bash
   pip3 install -r requirements.txt
   npm install
   ```

3. **Configure Nginx** (optional but recommended):
   ```nginx
   server {
       listen 80;
       server_name yourdomain.com;
       
       location / {
           proxy_pass http://127.0.0.1:5000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
       }
       
       location /static/ {
           alias /path/to/your/app/static/;
           expires 1y;
           add_header Cache-Control "public, immutable";
       }
   }
   ```

4. **Create systemd service**:
   ```ini
   [Unit]
   Description=N8N Workflow Generator
   After=network.target
   
   [Service]
   Type=exec
   User=www-data
   WorkingDirectory=/path/to/your/app
   Environment=PATH=/path/to/your/app/venv/bin
   ExecStart=/path/to/your/app/venv/bin/gunicorn -w 4 -b 127.0.0.1:5000 app:app
   Restart=always
   
   [Install]
   WantedBy=multi-user.target
   ```

5. **Start services**:
   ```bash
   sudo systemctl enable n8n-generator
   sudo systemctl start n8n-generator
   sudo systemctl enable nginx
   sudo systemctl start nginx
   ```

### AWS Deployment

1. **EC2 Instance**:
   - Launch Ubuntu 20.04 LTS instance
   - Configure security groups (ports 80, 443, 22)
   - Follow traditional server deployment

2. **Elastic Beanstalk**:
   ```bash
   # Install EB CLI
   pip install awsebcli
   
   # Initialize and deploy
   eb init
   eb create production
   eb deploy
   ```

3. **Lambda + API Gateway** (serverless):
   - Use Zappa or Serverless framework
   - Configure API Gateway routes
   - Set up CloudFront for static assets

### Google Cloud Platform

1. **App Engine**:
   ```yaml
   # app.yaml
   runtime: python39
   
   env_variables:
     FLASK_ENV: production
     SECRET_KEY: your-secret-key
   
   automatic_scaling:
     min_instances: 1
     max_instances: 10
   ```

2. **Deploy**:
   ```bash
   gcloud app deploy
   ```

### Monitoring & Maintenance

1. **Health Checks**:
   ```bash
   # Add to crontab
   */5 * * * * curl -f http://localhost:5000/api/health || systemctl restart n8n-generator
   ```

2. **Log Rotation**:
   ```bash
   # /etc/logrotate.d/n8n-generator
   /path/to/logs/*.log {
       daily
       missingok
       rotate 30
       compress
       notifempty
       create 644 www-data www-data
   }
   ```

3. **Backup Strategy**:
   ```bash
   # Backup configuration and logs
   tar -czf backup-$(date +%Y%m%d).tar.gz config/ logs/ .env
   ```

### SSL/HTTPS Setup

1. **Let's Encrypt with Certbot**:
   ```bash
   sudo apt install certbot python3-certbot-nginx
   sudo certbot --nginx -d yourdomain.com
   ```

2. **Manual SSL Certificate**:
   ```nginx
   server {
       listen 443 ssl;
       ssl_certificate /path/to/certificate.crt;
       ssl_certificate_key /path/to/private.key;
       # ... rest of config
   }
   ```

### Performance Optimization

1. **Enable Gzip**:
   ```nginx
   gzip on;
   gzip_types text/plain text/css application/json application/javascript;
   ```

2. **Static File Caching**:
   ```nginx
   location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg)$ {
       expires 1y;
       add_header Cache-Control "public, immutable";
   }
   ```

3. **Redis Configuration**:
   ```bash
   # /etc/redis/redis.conf
   maxmemory 256mb
   maxmemory-policy allkeys-lru
   ```

### Troubleshooting

1. **Check logs**:
   ```bash
   tail -f logs/n8n_generator_prod.log
   journalctl -u n8n-generator -f
   ```

2. **Test endpoints**:
   ```bash
   curl -X GET http://localhost:5000/api/health
   curl -X POST http://localhost:5000/api/generate -H "Content-Type: application/json" -d '{"description":"test"}'
   ```

3. **Common issues**:
   - Port conflicts: Check if port 5000 is available
   - Permission errors: Ensure correct file permissions
   - Memory issues: Monitor RAM usage, adjust worker count
   - Rate limiting: Check Redis connection

### Security Checklist

- [ ] HTTPS enabled
- [ ] Security headers configured
- [ ] Rate limiting active
- [ ] Input validation enabled
- [ ] Secrets stored securely
- [ ] Regular security updates
- [ ] Firewall configured
- [ ] Access logs monitored

### Scaling Considerations

1. **Horizontal Scaling**:
   - Use load balancer (nginx, HAProxy)
   - Multiple application instances
   - Shared Redis for session storage

2. **Vertical Scaling**:
   - Increase server resources
   - Optimize database queries
   - Enable caching layers

3. **CDN Integration**:
   - CloudFlare, AWS CloudFront
   - Cache static assets
   - Global distribution