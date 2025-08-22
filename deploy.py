#!/usr/bin/env python3
"""
Sahay AI - Quick Deployment Script
Automates the deployment process for different platforms
"""

import os
import sys
import subprocess
import argparse
from pathlib import Path

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e.stderr}")
        return None

def check_prerequisites():
    """Check if all prerequisites are installed"""
    print("🔍 Checking prerequisites...")
    
    # Check Python version
    python_version = sys.version_info
    if python_version.major < 3 or (python_version.major == 3 and python_version.minor < 8):
        print("❌ Python 3.8+ is required")
        return False
    
    print(f"✅ Python {python_version.major}.{python_version.minor}.{python_version.micro}")
    
    # Check if we're in the right directory
    if not Path("manage.py").exists():
        print("❌ manage.py not found. Please run this script from the project root.")
        return False
    
    print("✅ Project structure looks good")
    return True

def setup_environment():
    """Setup environment variables"""
    print("🔧 Setting up environment...")
    
    env_file = Path(".env")
    if not env_file.exists():
        env_content = """DEBUG=True
SECRET_KEY=your-secret-key-change-this-in-production
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_URL=sqlite:///db.sqlite3
"""
        env_file.write_text(env_content)
        print("✅ Created .env file")
    else:
        print("✅ .env file already exists")

def install_dependencies():
    """Install Python dependencies"""
    return run_command("pip install -r requirements.txt", "Installing dependencies")

def setup_database():
    """Setup database"""
    run_command("python manage.py makemigrations", "Creating migrations")
    run_command("python manage.py migrate", "Running migrations")

def collect_static():
    """Collect static files"""
    return run_command("python manage.py collectstatic --noinput", "Collecting static files")

def test_application():
    """Test the application"""
    print("🧪 Testing application...")
    
    # Check Django settings
    result = run_command("python manage.py check --deploy", "Checking Django deployment settings")
    if result is None:
        return False
    
    # Test database connection
    result = run_command("python manage.py check", "Checking Django configuration")
    if result is None:
        return False
    
    print("✅ Application tests passed")
    return True

def deploy_heroku():
    """Deploy to Heroku"""
    print("🚀 Deploying to Heroku...")
    
    # Check if Heroku CLI is installed
    if run_command("heroku --version", "Checking Heroku CLI") is None:
        print("❌ Heroku CLI not found. Please install it first.")
        print("   Visit: https://devcenter.heroku.com/articles/heroku-cli")
        return False
    
    # Create Procfile if it doesn't exist
    procfile = Path("Procfile")
    if not procfile.exists():
        procfile.write_text("web: gunicorn career_mentor_web.wsgi --log-file -")
        print("✅ Created Procfile")
    
    # Add gunicorn to requirements if not present
    requirements = Path("requirements.txt").read_text()
    if "gunicorn" not in requirements:
        with open("requirements.txt", "a") as f:
            f.write("\ngunicorn==21.2.0\nwhitenoise==6.6.0\ndj-database-url==2.1.0\npsycopg2-binary==2.9.9\n")
        print("✅ Added production dependencies")
    
    # Deploy commands
    commands = [
        ("git add .", "Adding files to git"),
        ("git commit -m 'Deploy to Heroku'", "Committing changes"),
        ("git push heroku main", "Pushing to Heroku"),
        ("heroku run python manage.py migrate", "Running migrations on Heroku"),
    ]
    
    for command, description in commands:
        if run_command(command, description) is None:
            return False
    
    print("✅ Heroku deployment completed!")
    print("🌐 Your app should be available at: https://your-app-name.herokuapp.com")
    return True

def deploy_railway():
    """Deploy to Railway"""
    print("🚂 Deploying to Railway...")
    
    # Check if Railway CLI is installed
    if run_command("railway --version", "Checking Railway CLI") is None:
        print("❌ Railway CLI not found. Please install it first.")
        print("   Run: npm install -g @railway/cli")
        return False
    
    # Create railway.json if it doesn't exist
    railway_config = Path("railway.json")
    if not railway_config.exists():
        config = """{
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "startCommand": "gunicorn career_mentor_web.wsgi --log-file -",
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10
  }
}"""
        railway_config.write_text(config)
        print("✅ Created railway.json")
    
    # Deploy
    if run_command("railway up", "Deploying to Railway") is None:
        return False
    
    print("✅ Railway deployment completed!")
    return True

def run_local():
    """Run the application locally"""
    print("🏠 Running application locally...")
    
    if not check_prerequisites():
        return False
    
    setup_environment()
    install_dependencies()
    setup_database()
    collect_static()
    
    if test_application():
        print("🚀 Starting development server...")
        print("🌐 Access your application at: http://127.0.0.1:8000")
        print("⏹️  Press Ctrl+C to stop the server")
        
        try:
            subprocess.run("python manage.py runserver", shell=True)
        except KeyboardInterrupt:
            print("\n👋 Server stopped")
    
    return True

def main():
    """Main deployment function"""
    parser = argparse.ArgumentParser(description="Sahay AI Deployment Script")
    parser.add_argument("--platform", choices=["local", "heroku", "railway"], 
                       default="local", help="Deployment platform")
    parser.add_argument("--skip-tests", action="store_true", 
                       help="Skip application tests")
    
    args = parser.parse_args()
    
    print("🚀 Sahay AI - Deployment Script")
    print("=" * 50)
    
    if args.platform == "local":
        run_local()
    elif args.platform == "heroku":
        if not args.skip_tests and not test_application():
            print("❌ Application tests failed. Use --skip-tests to bypass.")
            return
        deploy_heroku()
    elif args.platform == "railway":
        if not args.skip_tests and not test_application():
            print("❌ Application tests failed. Use --skip-tests to bypass.")
            return
        deploy_railway()
    
    print("\n🎉 Deployment process completed!")
    print("📚 Check DEPLOYMENT_GUIDE.md for detailed instructions")

if __name__ == "__main__":
    main() 