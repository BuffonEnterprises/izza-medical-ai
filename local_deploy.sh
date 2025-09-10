#!/bin/bash

# Izza Medical AI - Local Deployment Script
# This script helps you run the application locally or deploy to alternative platforms

set -e

echo "🚀 Izza Medical AI - Deployment Options"
echo "========================================"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Check for .env file
if [ ! -f ".env" ]; then
    echo -e "${YELLOW}⚠️  Creating .env file template...${NC}"
    cat > .env << EOF
# REQUIRED: Anthropic API Configuration
ANTHROPIC_API_KEY=your_anthropic_api_key_here

# Optional: Model configuration
ANTHROPIC_MODEL=claude-opus-4-1-20250805
ANTHROPIC_FALLBACK_MODEL=claude-3-5-sonnet-20240620

# Optional: Enhanced features API keys
OPENAI_API_KEY=
AZURE_SPEECH_KEY=
AZURE_SPEECH_REGION=eastus

# Performance Settings (defaults are fine)
MAX_OUTPUT_TOKENS=2048
MAX_OUTPUT_TOKENS_EXTENDED=4096
MAX_HISTORY_MESSAGES=12
EOF
    echo -e "${RED}⚠️  Please edit .env file and add your ANTHROPIC_API_KEY!${NC}"
    echo -e "${YELLOW}Get your API key from: https://console.anthropic.com/settings/keys${NC}"
    exit 1
fi

echo ""
echo "Choose deployment option:"
echo "1) Run locally with Docker"
echo "2) Run locally with Python"
echo "3) Deploy to Heroku (free tier available)"
echo "4) Deploy to Railway.app"
echo "5) Deploy to Render.com"
echo "6) Generate deployment files only"
echo ""
read -p "Enter your choice (1-6): " choice

case $choice in
    1)
        echo -e "${YELLOW}🐳 Running with Docker...${NC}"
        
        # Build Docker image
        echo "Building Docker image..."
        docker build -t izza-medical-ai:latest .
        
        # Run container
        echo "Starting container..."
        docker run -d \
            --name izza-medical-ai \
            -p 8080:8080 \
            --env-file .env \
            --restart unless-stopped \
            izza-medical-ai:latest
        
        echo -e "${GREEN}✅ Application is running!${NC}"
        echo -e "${GREEN}🌐 Access at: http://localhost:8080${NC}"
        echo ""
        echo "Docker commands:"
        echo "  Stop:    docker stop izza-medical-ai"
        echo "  Start:   docker start izza-medical-ai"
        echo "  Logs:    docker logs -f izza-medical-ai"
        echo "  Remove:  docker rm -f izza-medical-ai"
        ;;
        
    2)
        echo -e "${YELLOW}🐍 Running with Python...${NC}"
        
        # Check Python version
        python_cmd="python3"
        if ! command -v python3 &> /dev/null; then
            python_cmd="python"
        fi
        
        # Create virtual environment if it doesn't exist
        if [ ! -d "venv" ]; then
            echo "Creating virtual environment..."
            $python_cmd -m venv venv
        fi
        
        # Activate virtual environment
        echo "Activating virtual environment..."
        source venv/bin/activate
        
        # Install dependencies
        echo "Installing dependencies..."
        pip install -r requirements.txt
        
        # Run the application
        echo -e "${GREEN}✅ Starting application...${NC}"
        streamlit run op.py --server.port 8080
        ;;
        
    3)
        echo -e "${YELLOW}🚀 Deploying to Heroku...${NC}"
        
        # Create Procfile for Heroku
        cat > Procfile << EOF
web: sh setup.sh && streamlit run op.py --server.port \$PORT --server.address 0.0.0.0
EOF
        
        # Create setup.sh for Heroku
        cat > setup.sh << EOF
mkdir -p ~/.streamlit/
echo "\
[server]\\n\
port = \$PORT\\n\
enableCORS = false\\n\
headless = true\\n\
\\n\
" > ~/.streamlit/config.toml
EOF
        
        # Create runtime.txt
        echo "python-3.11.0" > runtime.txt
        
        echo -e "${GREEN}✅ Heroku files created!${NC}"
        echo ""
        echo "To deploy to Heroku:"
        echo "1. Install Heroku CLI: https://devcenter.heroku.com/articles/heroku-cli"
        echo "2. Run these commands:"
        echo "   heroku create izza-medical-ai"
        echo "   heroku config:set ANTHROPIC_API_KEY=your_key_here"
        echo "   git add ."
        echo "   git commit -m 'Deploy to Heroku'"
        echo "   git push heroku main"
        ;;
        
    4)
        echo -e "${YELLOW}🚂 Deploying to Railway...${NC}"
        
        # Create railway.json
        cat > railway.json << EOF
{
  "build": {
    "builder": "DOCKERFILE"
  },
  "deploy": {
    "startCommand": "streamlit run op.py --server.port \$PORT --server.address 0.0.0.0",
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10
  }
}
EOF
        
        echo -e "${GREEN}✅ Railway configuration created!${NC}"
        echo ""
        echo "To deploy to Railway:"
        echo "1. Install Railway CLI: npm install -g @railway/cli"
        echo "2. Run: railway login"
        echo "3. Run: railway init"
        echo "4. Run: railway add"
        echo "5. Set environment variables in Railway dashboard"
        echo "6. Run: railway up"
        ;;
        
    5)
        echo -e "${YELLOW}🎨 Deploying to Render...${NC}"
        
        # Create render.yaml
        cat > render.yaml << EOF
services:
  - type: web
    name: izza-medical-ai
    env: docker
    dockerfilePath: ./Dockerfile
    envVars:
      - key: PORT
        value: 8080
      - key: ANTHROPIC_API_KEY
        sync: false
EOF
        
        echo -e "${GREEN}✅ Render configuration created!${NC}"
        echo ""
        echo "To deploy to Render:"
        echo "1. Push your code to GitHub"
        echo "2. Go to https://render.com"
        echo "3. Create a new Web Service"
        echo "4. Connect your GitHub repo"
        echo "5. Set environment variables in dashboard"
        ;;
        
    6)
        echo -e "${YELLOW}📁 Generating deployment files...${NC}"
        
        # Create docker-compose.yml
        cat > docker-compose.yml << EOF
version: '3.8'

services:
  izza-medical-ai:
    build: .
    ports:
      - "8080:8080"
    env_file:
      - .env
    restart: unless-stopped
    volumes:
      - ./data:/app/data
EOF
        
        # Create nginx.conf for reverse proxy
        cat > nginx.conf << EOF
server {
    listen 80;
    server_name your-domain.com;
    
    location / {
        proxy_pass http://localhost:8080;
        proxy_http_version 1.1;
        proxy_set_header Upgrade \$http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host \$host;
        proxy_cache_bypass \$http_upgrade;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }
}
EOF
        
        echo -e "${GREEN}✅ Deployment files generated!${NC}"
        echo ""
        echo "Files created:"
        echo "  - docker-compose.yml (for Docker Compose deployment)"
        echo "  - nginx.conf (for reverse proxy setup)"
        echo "  - Dockerfile (already exists)"
        echo "  - requirements.txt (already exists)"
        echo ""
        echo "To deploy with Docker Compose:"
        echo "  docker-compose up -d"
        ;;
        
    *)
        echo -e "${RED}Invalid choice!${NC}"
        exit 1
        ;;
esac

echo ""
echo -e "${BLUE}📚 Documentation:${NC}"
echo "  - Make sure ANTHROPIC_API_KEY is set in .env"
echo "  - Optional: Add other API keys for enhanced features"
echo "  - The app will be available on port 8080"
echo "  - Check logs for any errors during startup"