# 🚀 Sahay AI - Deployment Guide
## Complete Guide to Deploy Your AI Career Mentor

---

## 📋 **Table of Contents**
1. [Prerequisites](#prerequisites)
2. [Local Development Setup](#local-development-setup)
3. [Production Deployment Options](#production-deployment-options)
4. [Heroku Deployment](#heroku-deployment)
5. [Railway Deployment](#railway-deployment)
6. [AWS Deployment](#aws-deployment)
7. [Docker Deployment](#docker-deployment)
8. [Environment Configuration](#environment-configuration)
9. [Database Setup](#database-setup)
10. [Static Files Configuration](#static-files-configuration)
11. [Security Considerations](#security-considerations)
12. [Monitoring & Maintenance](#monitoring--maintenance)
13. [Troubleshooting](#troubleshooting)

---

## 🔧 **Prerequisites**

### **System Requirements**
- **Python**: 3.8+ (recommended: 3.11+)
- **Memory**: Minimum 2GB RAM (4GB+ recommended for AI models)
- **Storage**: 1GB+ free space
- **OS**: Windows, macOS, or Linux

### **Required Accounts**
- **GitHub**: For code repository
- **Heroku/Railway/AWS**: For hosting (choose one)
- **Domain Name**: Optional (for custom domain)

---

## 💻 **Local Development Setup**

### **Step 1: Clone Repository**
```bash
git clone <your-repository-url>
cd Hackathon
```

### **Step 2: Create Virtual Environment**
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### **Step 3: Install Dependencies**
```bash
pip install -r requirements.txt
```

### **Step 4: Environment Variables**
Create `.env` file in project root:
```env
DEBUG=True
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_URL=sqlite:///db.sqlite3
```

### **Step 5: Database Setup**
```bash
python manage.py makemigrations
python manage.py migrate
```

### **Step 6: Create Superuser (Optional)**
```bash
python manage.py createsuperuser
```

### **Step 7: Run Development Server**
```bash
python manage.py runserver
```

**Access**: http://127.0.0.1:8000

---

## 🌐 **Production Deployment Options**

### **Recommended Platforms**

| Platform | Pros | Cons | Best For |
|----------|------|------|----------|
| **Heroku** | Easy setup, free tier | Limited resources | Prototypes, demos |
| **Railway** | Fast deployment, good free tier | Newer platform | Small to medium projects |
| **AWS** | Scalable, powerful | Complex setup, costs | Production, enterprise |
| **DigitalOcean** | Good performance, reasonable cost | Manual setup | Small businesses |
| **Vercel** | Fast, good for frontend | Limited backend support | Frontend-heavy apps |

---

## 🚀 **Heroku Deployment**

### **Step 1: Install Heroku CLI**
```bash
# Windows
# Download from: https://devcenter.heroku.com/articles/heroku-cli

# macOS
brew install heroku/brew/heroku

# Linux
curl https://cli-assets.heroku.com/install.sh | sh
```

### **Step 2: Login to Heroku**
```bash
heroku login
```

### **Step 3: Create Heroku App**
```bash
heroku create sahay-ai-career-mentor
```

### **Step 4: Add Buildpacks**
```bash
heroku buildpacks:add heroku/python
heroku buildpacks:add https://github.com/heroku/heroku-buildpack-apt
```

### **Step 5: Create Procfile**
Create `Procfile` in project root:
```
web: gunicorn career_mentor_web.wsgi --log-file -
```

### **Step 6: Update requirements.txt**
Add these lines to `requirements.txt`:
```
gunicorn==21.2.0
whitenoise==6.6.0
dj-database-url==2.1.0
psycopg2-binary==2.9.9
```

### **Step 7: Update settings.py**
Add to `career_mentor_web/settings.py`:
```python
import dj_database_url
import os

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = 'DEVELOPMENT' in os.environ

ALLOWED_HOSTS = ['your-app-name.herokuapp.com', 'localhost', '127.0.0.1']

# Database
DATABASES = {
    'default': dj_database_url.parse(os.environ.get('DATABASE_URL'))
}

# Static files
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Media files
MEDIA_ROOT = os.path.join(BASE_DIR, 'mediafiles')
```

### **Step 8: Deploy**
```bash
git add .
git commit -m "Deploy to Heroku"
git push heroku main

# Run migrations
heroku run python manage.py migrate

# Create superuser (optional)
heroku run python manage.py createsuperuser
```

### **Step 9: Configure Environment Variables**
```bash
heroku config:set SECRET_KEY=your-production-secret-key
heroku config:set DEBUG=False
heroku config:set ALLOWED_HOSTS=your-app-name.herokuapp.com
```

---

## 🚂 **Railway Deployment**

### **Step 1: Install Railway CLI**
```bash
npm install -g @railway/cli
```

### **Step 2: Login to Railway**
```bash
railway login
```

### **Step 3: Initialize Project**
```bash
railway init
```

### **Step 4: Create railway.json**
Create `railway.json` in project root:
```json
{
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "startCommand": "gunicorn career_mentor_web.wsgi --log-file -",
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10
  }
}
```

### **Step 5: Deploy**
```bash
railway up
```

### **Step 6: Configure Environment**
In Railway dashboard:
- Set `SECRET_KEY`
- Set `DEBUG=False`
- Set `ALLOWED_HOSTS`

---

## ☁️ **AWS Deployment**

### **Step 1: AWS Account Setup**
1. Create AWS account
2. Install AWS CLI
3. Configure credentials

### **Step 2: Create EC2 Instance**
```bash
# Launch Ubuntu instance
# t2.medium or larger for AI models
# Configure security groups for ports 22, 80, 443
```

### **Step 3: Connect and Setup**
```bash
ssh -i your-key.pem ubuntu@your-ec2-ip

# Update system
sudo apt update && sudo apt upgrade -y

# Install Python, Nginx, etc.
sudo apt install python3-pip python3-venv nginx git -y
```

### **Step 4: Deploy Application**
```bash
# Clone repository
git clone <your-repo>
cd Hackathon

# Setup virtual environment
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Setup environment variables
nano .env
```

### **Step 5: Configure Gunicorn**
Create `/etc/systemd/system/sahay-ai.service`:
```ini
[Unit]
Description=Sahay AI Gunicorn daemon
After=network.target

[Service]
User=ubuntu
Group=www-data
WorkingDirectory=/home/ubuntu/Hackathon
Environment="PATH=/home/ubuntu/Hackathon/venv/bin"
ExecStart=/home/ubuntu/Hackathon/venv/bin/gunicorn --workers 3 --bind unix:/home/ubuntu/Hackathon/sahay-ai.sock career_mentor_web.wsgi:application

[Install]
WantedBy=multi-user.target
```

### **Step 6: Configure Nginx**
Create `/etc/nginx/sites-available/sahay-ai`:
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location = /favicon.ico { access_log off; log_not_found off; }
    
    location /static/ {
        root /home/ubuntu/Hackathon;
    }

    location /media/ {
        root /home/ubuntu/Hackathon;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/home/ubuntu/Hackathon/sahay-ai.sock;
    }
}
```

### **Step 7: Start Services**
```bash
sudo systemctl start sahay-ai
sudo systemctl enable sahay-ai
sudo ln -s /etc/nginx/sites-available/sahay-ai /etc/nginx/sites-enabled
sudo systemctl restart nginx
```

---

## 🐳 **Docker Deployment**

### **Step 1: Create Dockerfile**
Create `Dockerfile` in project root:
```dockerfile
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . .

# Collect static files
RUN python manage.py collectstatic --noinput

# Run gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "career_mentor_web.wsgi:application"]
```

### **Step 2: Create docker-compose.yml**
```yaml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DEBUG=False
      - SECRET_KEY=your-secret-key
    volumes:
      - ./media:/app/media
      - ./staticfiles:/app/staticfiles
    depends_on:
      - db
  
  db:
    image: postgres:13
    environment:
      - POSTGRES_DB=sahay_ai
      - POSTGRES_USER=sahay_user
      - POSTGRES_PASSWORD=sahay_password
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

### **Step 3: Build and Run**
```bash
docker-compose up --build
```

---

## ⚙️ **Environment Configuration**

### **Production Settings**
Update `career_mentor_web/settings.py`:
```python
import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY', 'your-secret-key-here')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('DEBUG', 'False').lower() == 'true'

ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',')

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Use PostgreSQL in production
if not DEBUG:
    import dj_database_url
    DATABASES['default'] = dj_database_url.parse(os.environ.get('DATABASE_URL'))

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Security settings
if not DEBUG:
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    X_FRAME_OPTIONS = 'DENY'
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
```

---

## 🗄️ **Database Setup**

### **SQLite (Development)**
```bash
python manage.py makemigrations
python manage.py migrate
```

### **PostgreSQL (Production)**
```bash
# Install psycopg2
pip install psycopg2-binary

# Update requirements.txt
echo "psycopg2-binary==2.9.9" >> requirements.txt

# Run migrations
python manage.py migrate
```

### **Database Backup**
```bash
# Backup
python manage.py dumpdata > backup.json

# Restore
python manage.py loaddata backup.json
```

---

## 📁 **Static Files Configuration**

### **Development**
```bash
python manage.py collectstatic --noinput
```

### **Production with WhiteNoise**
Add to `MIDDLEWARE` in settings.py:
```python
MIDDLEWARE = [
    # ... other middleware
    'whitenoise.middleware.WhiteNoiseMiddleware',
    # ... other middleware
]

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
```

### **CDN Configuration (Optional)**
```python
# For AWS S3 or other CDN
STATIC_URL = 'https://your-cdn-domain.com/static/'
MEDIA_URL = 'https://your-cdn-domain.com/media/'
```

---

## 🔒 **Security Considerations**

### **Environment Variables**
```bash
# Never commit these to version control
SECRET_KEY=your-super-secret-key
DEBUG=False
ALLOWED_HOSTS=your-domain.com
DATABASE_URL=postgres://user:pass@host:port/db
```

### **Security Headers**
Add to `settings.py`:
```python
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
```

### **HTTPS Configuration**
```python
# Force HTTPS
SECURE_SSL_REDIRECT = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
```

---

## 📊 **Monitoring & Maintenance**

### **Logging Configuration**
Add to `settings.py`:
```python
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': 'django.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}
```

### **Health Check Endpoint**
Add to `career_advisor/views.py`:
```python
from django.http import JsonResponse

def health_check(request):
    return JsonResponse({'status': 'healthy'})
```

### **Performance Monitoring**
```bash
# Monitor CPU and memory
htop

# Monitor logs
tail -f django.log

# Monitor database
python manage.py dbshell
```

---

## 🔧 **Troubleshooting**

### **Common Issues**

#### **1. Static Files Not Loading**
```bash
python manage.py collectstatic --noinput
# Check STATIC_ROOT and STATICFILES_STORAGE settings
```

#### **2. Database Connection Issues**
```bash
# Check DATABASE_URL format
# Ensure database is running
# Check credentials
```

#### **3. AI Model Loading Issues**
```bash
# Check available memory
# Verify model files are downloaded
# Check internet connection for model downloads
```

#### **4. Upload Issues**
```bash
# Check MEDIA_ROOT permissions
# Ensure directory exists
# Check file size limits
```

### **Debug Commands**
```bash
# Check Django settings
python manage.py check --deploy

# Test database connection
python manage.py dbshell

# Check static files
python manage.py findstatic admin/css/base.css

# Monitor logs
tail -f /var/log/nginx/error.log
```

---

## 🎯 **Deployment Checklist**

### **Pre-Deployment**
- [ ] All tests passing
- [ ] Environment variables configured
- [ ] Database migrations ready
- [ ] Static files collected
- [ ] Security settings updated
- [ ] Logging configured

### **Deployment**
- [ ] Code pushed to repository
- [ ] Build successful
- [ ] Database migrated
- [ ] Static files served
- [ ] Health check passing
- [ ] SSL certificate installed

### **Post-Deployment**
- [ ] Application accessible
- [ ] All features working
- [ ] Performance acceptable
- [ ] Monitoring active
- [ ] Backup configured
- [ ] Documentation updated

---

## 🚀 **Quick Deploy Commands**

### **Heroku (Recommended for Hackathon)**
```bash
# One-command deployment
git add . && git commit -m "Deploy" && git push heroku main && heroku run python manage.py migrate
```

### **Railway**
```bash
# Deploy to Railway
railway up
```

### **Local Production Test**
```bash
# Test production settings locally
DEBUG=False python manage.py runserver
```

---

## 📞 **Support**

### **Useful Resources**
- [Django Deployment Checklist](https://docs.djangoproject.com/en/stable/howto/deployment/checklist/)
- [Heroku Python Guide](https://devcenter.heroku.com/articles/python)
- [Railway Documentation](https://docs.railway.app/)
- [AWS Django Deployment](https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/create-deploy-python-django.html)

### **Contact**
- **GitHub Issues**: Report bugs and feature requests
- **Documentation**: Check project README.md
- **Community**: Django forums and Stack Overflow

---

## 🎉 **Congratulations!**

Your Sahay AI application is now ready for deployment! Choose the platform that best fits your needs and follow the corresponding guide.

**Good luck with your hackathon presentation! 🚀**

---

*Built with ❤️ by Soham Tripathy* 