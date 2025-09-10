#!/bin/bash

# ULTRA DEPLOY - Complete Deployment Solution for Izza Medical AI
# This script handles ALL deployment scenarios automatically

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m'

echo -e "${PURPLE}╔══════════════════════════════════════════════════════════════╗${NC}"
echo -e "${PURPLE}║        🚀 ULTRA DEPLOY - IZZA MEDICAL AI 🚀                 ║${NC}"
echo -e "${PURPLE}║        Automatic Multi-Platform Deployment System            ║${NC}"
echo -e "${PURPLE}╚══════════════════════════════════════════════════════════════╝${NC}"
echo ""

# Function to check command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to create .env if not exists
create_env_file() {
    if [ ! -f ".env" ]; then
        echo -e "${YELLOW}📝 Creating .env file...${NC}"
        cat > .env << 'EOF'
# REQUIRED - Get from https://console.anthropic.com/
ANTHROPIC_API_KEY=

# Optional - Enhanced features
OPENAI_API_KEY=
AZURE_SPEECH_KEY=
AZURE_SPEECH_REGION=eastus

# Model Configuration
ANTHROPIC_MODEL=claude-opus-4-1-20250805
ANTHROPIC_FALLBACK_MODEL=claude-3-5-sonnet-20240620

# Performance Settings
MAX_OUTPUT_TOKENS=2048
MAX_OUTPUT_TOKENS_EXTENDED=4096
MAX_HISTORY_MESSAGES=12
MAX_HISTORY_CHARS=16000
EOF
        echo -e "${RED}⚠️  IMPORTANT: Edit .env and add your ANTHROPIC_API_KEY!${NC}"
        echo -e "${YELLOW}Opening .env in default editor...${NC}"
        ${EDITOR:-nano} .env
    fi
}

# Function to try different GCP projects
try_gcp_projects() {
    echo -e "${CYAN}🔍 Checking available GCP projects...${NC}"
    
    PROJECTS=("model-union-469912-h2" "snappy-airway-469911-t7" "ordinal-ember-468522-c9" "mystic-keel-092sd" "primeversion-468523")
    
    for PROJECT in "${PROJECTS[@]}"; do
        echo -e "${YELLOW}Testing project: $PROJECT${NC}"
        
        # Try to set project
        if gcloud config set project "$PROJECT" 2>/dev/null; then
            # Check if billing is enabled
            if gcloud services list --enabled 2>/dev/null | grep -q "cloudresourcemanager"; then
                echo -e "${GREEN}✅ Project $PROJECT is active!${NC}"
                
                # Enable required services
                echo -e "${YELLOW}Enabling services...${NC}"
                gcloud services enable \
                    cloudbuild.googleapis.com \
                    run.googleapis.com \
                    containerregistry.googleapis.com \
                    artifactregistry.googleapis.com 2>/dev/null || true
                
                # Try to deploy
                echo -e "${YELLOW}Attempting deployment to $PROJECT...${NC}"
                if deploy_to_cloud_run "$PROJECT"; then
                    return 0
                fi
            else
                echo -e "${RED}❌ Project $PROJECT has billing issues${NC}"
            fi
        fi
    done
    
    return 1
}

# Function to deploy to Cloud Run
deploy_to_cloud_run() {
    local PROJECT_ID=$1
    local SERVICE_NAME="izza-medical-ai"
    local REGION="us-central1"
    
    echo -e "${CYAN}🚀 Deploying to Cloud Run (Project: $PROJECT_ID)...${NC}"
    
    # Build with Cloud Build (trying with minimal build)
    echo -e "${YELLOW}Building container...${NC}"
    
    # Try using gcloud run deploy directly with source
    if gcloud run deploy $SERVICE_NAME \
        --source . \
        --region $REGION \
        --platform managed \
        --allow-unauthenticated \
        --memory 2Gi \
        --cpu 2 \
        --timeout 900 \
        --max-instances 10 \
        --port 8080 \
        --set-env-vars "STREAMLIT_SERVER_HEADLESS=true,STREAMLIT_SERVER_PORT=8080" \
        --project $PROJECT_ID 2>/dev/null; then
        
        # Get service URL
        SERVICE_URL=$(gcloud run services describe $SERVICE_NAME \
            --region $REGION \
            --format 'value(status.url)' \
            --project $PROJECT_ID)
        
        echo -e "${GREEN}✅ Deployment successful!${NC}"
        echo -e "${GREEN}🌐 URL: $SERVICE_URL${NC}"
        return 0
    fi
    
    return 1
}

# Function to deploy locally with Docker
deploy_docker_local() {
    echo -e "${CYAN}🐳 Setting up Docker deployment...${NC}"
    
    if ! command_exists docker; then
        echo -e "${YELLOW}Docker not found. Installing Docker...${NC}"
        
        if [[ "$OSTYPE" == "darwin"* ]]; then
            echo "Please install Docker Desktop from: https://www.docker.com/products/docker-desktop"
            return 1
        else
            curl -fsSL https://get.docker.com -o get-docker.sh
            sudo sh get-docker.sh
        fi
    fi
    
    echo -e "${YELLOW}Building Docker image...${NC}"
    docker build -t izza-medical:latest . || {
        echo -e "${RED}Docker build failed. Trying alternative...${NC}"
        # Create simpler Dockerfile
        create_simple_dockerfile
        docker build -t izza-medical:latest .
    }
    
    echo -e "${YELLOW}Running container...${NC}"
    docker stop izza-medical 2>/dev/null || true
    docker rm izza-medical 2>/dev/null || true
    
    docker run -d \
        --name izza-medical \
        -p 8080:8080 \
        --env-file .env \
        --restart unless-stopped \
        izza-medical:latest
    
    echo -e "${GREEN}✅ Docker deployment successful!${NC}"
    echo -e "${GREEN}🌐 Access at: http://localhost:8080${NC}"
    return 0
}

# Function to create simple Dockerfile
create_simple_dockerfile() {
    cat > Dockerfile.simple << 'EOF'
FROM python:3.9-slim
WORKDIR /app
RUN apt-get update && apt-get install -y gcc && rm -rf /var/lib/apt/lists/*
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY op.py .
COPY .env .
EXPOSE 8080
CMD ["streamlit", "run", "op.py", "--server.port=8080", "--server.address=0.0.0.0"]
EOF
    mv Dockerfile.simple Dockerfile
}

# Function to deploy with Python directly
deploy_python_local() {
    echo -e "${CYAN}🐍 Setting up Python deployment...${NC}"
    
    # Check Python
    PYTHON_CMD=""
    if command_exists python3; then
        PYTHON_CMD="python3"
    elif command_exists python; then
        PYTHON_CMD="python"
    else
        echo -e "${RED}Python not found!${NC}"
        return 1
    fi
    
    # Create virtual environment
    echo -e "${YELLOW}Creating virtual environment...${NC}"
    $PYTHON_CMD -m venv venv || {
        echo -e "${YELLOW}Installing venv...${NC}"
        $PYTHON_CMD -m pip install --user virtualenv
        $PYTHON_CMD -m virtualenv venv
    }
    
    # Activate and install
    echo -e "${YELLOW}Installing dependencies...${NC}"
    source venv/bin/activate
    pip install --upgrade pip
    pip install -r requirements.txt
    
    # Run application
    echo -e "${GREEN}✅ Starting application...${NC}"
    streamlit run op.py --server.port 8080 --server.address 0.0.0.0 &
    
    echo -e "${GREEN}🌐 Access at: http://localhost:8080${NC}"
    return 0
}

# Function to deploy to free platforms
deploy_free_platforms() {
    echo -e "${CYAN}☁️ Setting up free cloud deployments...${NC}"
    
    # Create Render configuration
    cat > render.yaml << 'EOF'
services:
  - type: web
    name: izza-medical-ai
    runtime: python
    buildCommand: pip install -r requirements.txt
    startCommand: streamlit run op.py --server.port $PORT --server.address 0.0.0.0
    envVars:
      - key: PYTHON_VERSION
        value: 3.9.18
EOF
    
    # Create Heroku files
    cat > Procfile << 'EOF'
web: sh setup.sh && streamlit run op.py --server.port $PORT --server.address 0.0.0.0
EOF
    
    cat > setup.sh << 'EOF'
mkdir -p ~/.streamlit/
echo "[server]\nport = $PORT\nenableCORS = false\nheadless = true\n" > ~/.streamlit/config.toml
EOF
    
    echo "python-3.9.18" > runtime.txt
    
    # Create Railway configuration
    cat > railway.json << 'EOF'
{
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "startCommand": "streamlit run op.py --server.port $PORT --server.address 0.0.0.0",
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10
  }
}
EOF
    
    echo -e "${GREEN}✅ Free platform configurations created!${NC}"
    echo ""
    echo -e "${YELLOW}Deploy to Render.com:${NC}"
    echo "1. Push to GitHub"
    echo "2. Go to https://render.com"
    echo "3. New > Web Service > Connect repo"
    echo ""
    echo -e "${YELLOW}Deploy to Railway:${NC}"
    echo "1. Install: npm i -g @railway/cli"
    echo "2. Run: railway login && railway up"
    echo ""
    echo -e "${YELLOW}Deploy to Heroku:${NC}"
    echo "1. heroku create izza-medical"
    echo "2. git push heroku main"
}

# Function to fix permissions
fix_permissions() {
    echo -e "${YELLOW}🔧 Fixing permissions...${NC}"
    chmod +x *.sh 2>/dev/null || true
    chmod 644 *.py 2>/dev/null || true
    chmod 644 requirements.txt 2>/dev/null || true
    chmod 644 Dockerfile 2>/dev/null || true
}

# Main execution
main() {
    echo -e "${CYAN}🔍 Running system checks...${NC}"
    
    # Fix permissions first
    fix_permissions
    
    # Create .env file
    create_env_file
    
    # Check if API key is set
    if ! grep -q "ANTHROPIC_API_KEY=sk-" .env 2>/dev/null; then
        echo -e "${RED}⚠️  ANTHROPIC_API_KEY not set in .env file!${NC}"
        echo -e "${YELLOW}Please add your API key to .env file first.${NC}"
        exit 1
    fi
    
    echo ""
    echo -e "${CYAN}🚀 Starting Ultra Deployment Process...${NC}"
    echo ""
    
    # Try GCP deployment first
    if command_exists gcloud; then
        echo -e "${BLUE}Option 1: Trying Google Cloud deployment...${NC}"
        if try_gcp_projects; then
            echo -e "${GREEN}✅ GCP deployment successful!${NC}"
            exit 0
        else
            echo -e "${YELLOW}GCP deployment failed. Trying alternatives...${NC}"
        fi
    fi
    
    # Try Docker deployment
    echo ""
    echo -e "${BLUE}Option 2: Trying Docker deployment...${NC}"
    if deploy_docker_local; then
        echo -e "${GREEN}✅ Docker deployment successful!${NC}"
        deploy_free_platforms
        exit 0
    fi
    
    # Try Python deployment
    echo ""
    echo -e "${BLUE}Option 3: Trying Python deployment...${NC}"
    if deploy_python_local; then
        echo -e "${GREEN}✅ Python deployment successful!${NC}"
        deploy_free_platforms
        exit 0
    fi
    
    # If all fails, provide manual instructions
    echo ""
    echo -e "${RED}Automated deployment failed. Here are manual options:${NC}"
    echo ""
    deploy_free_platforms
    
    echo ""
    echo -e "${YELLOW}📋 Manual deployment instructions created in:${NC}"
    echo "  - render.yaml (for Render.com)"
    echo "  - Procfile (for Heroku)"
    echo "  - railway.json (for Railway)"
    echo ""
    echo -e "${GREEN}Choose any free platform above and follow their instructions!${NC}"
}

# Run main function
main "$@"