#!/bin/bash

# DEPLOY ANYWHERE - Works without billing issues
# Automatic deployment to multiple free platforms

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
WHITE='\033[1;37m'
NC='\033[0m'

clear

echo -e "${PURPLE}╔════════════════════════════════════════════════════════════════╗${NC}"
echo -e "${PURPLE}║         🚀 UNIVERSAL DEPLOYMENT SYSTEM 🚀                     ║${NC}"
echo -e "${PURPLE}║         Deploy to ANY platform - No billing required          ║${NC}"
echo -e "${PURPLE}╚════════════════════════════════════════════════════════════════╝${NC}"
echo ""

# Check for .env
if [ ! -f .env ]; then
    echo -e "${RED}Creating .env file...${NC}"
    cat > .env << 'EOF'
ANTHROPIC_API_KEY=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
OPENAI_API_KEY=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
EOF
fi

echo -e "${CYAN}Select deployment platform:${NC}"
echo "1) Docker (Local)"
echo "2) Streamlit Cloud (FREE - Recommended)"
echo "3) Render.com (FREE)"
echo "4) Railway.app (FREE credits)"
echo "5) Heroku (Limited free)"
echo "6) Fly.io (FREE)"
echo "7) ALL platforms (prepare all configs)"
echo ""
read -p "Enter choice (1-7): " choice

case $choice in
    1)
        echo -e "${YELLOW}Deploying with Docker...${NC}"
        docker-compose down 2>/dev/null || true
        docker-compose up -d --build
        echo -e "${GREEN}✅ Docker deployment complete!${NC}"
        echo -e "${WHITE}Access at: http://localhost:8080${NC}"
        ;;
        
    2)
        echo -e "${YELLOW}Deploying to Streamlit Cloud...${NC}"
        
        # Ensure GitHub is updated
        git add -A
        git commit -m "Deploy to Streamlit Cloud" 2>/dev/null || true
        git push origin main
        
        echo -e "${GREEN}✅ Ready for Streamlit Cloud!${NC}"
        echo ""
        echo -e "${CYAN}Steps to complete deployment:${NC}"
        echo "1. Go to: https://share.streamlit.io/"
        echo "2. Click 'New app'"
        echo "3. Repository: BuffonEnterprises/izza-medical-ai"
        echo "4. Branch: main"
        echo "5. Main file: op.py"
        echo "6. Click Deploy!"
        echo ""
        echo -e "${YELLOW}Opening Streamlit Cloud...${NC}"
        open "https://share.streamlit.io/deploy?repository=BuffonEnterprises/izza-medical-ai&branch=main&mainModule=op.py"
        ;;
        
    3)
        echo -e "${YELLOW}Deploying to Render.com...${NC}"
        
        # Update render.yaml
        cat > render.yaml << 'EOF'
services:
  - type: web
    name: izza-medical-ai
    runtime: python
    region: oregon
    plan: free
    buildCommand: "pip install -r requirements.txt"
    startCommand: "streamlit run op.py --server.port $PORT --server.address 0.0.0.0"
    envVars:
      - key: PYTHON_VERSION
        value: 3.9.18
    autoDeploy: true
EOF
        
        git add render.yaml
        git commit -m "Add Render configuration" 2>/dev/null || true
        git push origin main
        
        echo -e "${GREEN}✅ Ready for Render!${NC}"
        echo "1. Go to: https://render.com"
        echo "2. New > Web Service"
        echo "3. Connect GitHub: BuffonEnterprises/izza-medical-ai"
        echo "4. It will auto-deploy!"
        echo ""
        echo -e "${YELLOW}Opening Render...${NC}"
        open "https://dashboard.render.com/select-repo?type=web"
        ;;
        
    4)
        echo -e "${YELLOW}Deploying to Railway...${NC}"
        
        # Create Railway config
        cat > railway.json << 'EOF'
{
  "$schema": "https://railway.app/railway.schema.json",
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
        
        # Install Railway CLI if needed
        if ! command -v railway &> /dev/null; then
            echo "Installing Railway CLI..."
            npm install -g @railway/cli
        fi
        
        railway login
        railway init
        railway up
        
        echo -e "${GREEN}✅ Deployed to Railway!${NC}"
        ;;
        
    5)
        echo -e "${YELLOW}Deploying to Heroku...${NC}"
        
        # Create Heroku files
        cat > Procfile << 'EOF'
web: sh setup.sh && streamlit run op.py --server.port $PORT --server.address 0.0.0.0
EOF
        
        cat > setup.sh << 'EOF'
mkdir -p ~/.streamlit/
echo "[server]\nport = $PORT\nenableCORS = false\n" > ~/.streamlit/config.toml
EOF
        
        echo "python-3.9.18" > runtime.txt
        
        # Deploy
        heroku create izza-medical-ai-$RANDOM
        git add .
        git commit -m "Add Heroku files"
        git push heroku main
        
        echo -e "${GREEN}✅ Deployed to Heroku!${NC}"
        ;;
        
    6)
        echo -e "${YELLOW}Deploying to Fly.io...${NC}"
        
        # Create fly.toml
        cat > fly.toml << 'EOF'
app = "izza-medical-ai"
primary_region = "sjc"

[build]
  builder = "paketobuildpacks/builder:base"

[env]
  PORT = "8080"
  PYTHONUNBUFFERED = "true"

[http_service]
  internal_port = 8080
  force_https = true
  auto_stop_machines = true
  auto_start_machines = true

[[services]]
  http_checks = []
  internal_port = 8080
  protocol = "tcp"
  script_checks = []

  [[services.ports]]
    force_https = true
    handlers = ["http"]
    port = 80

  [[services.ports]]
    handlers = ["tls", "http"]
    port = 443
EOF
        
        # Install Fly CLI if needed
        if ! command -v flyctl &> /dev/null; then
            echo "Installing Fly CLI..."
            curl -L https://fly.io/install.sh | sh
        fi
        
        flyctl auth login
        flyctl launch
        flyctl deploy
        
        echo -e "${GREEN}✅ Deployed to Fly.io!${NC}"
        ;;
        
    7)
        echo -e "${YELLOW}Creating configurations for ALL platforms...${NC}"
        
        # Create all config files
        
        # Docker Compose
        cat > docker-compose.yml << 'EOF'
version: '3.8'
services:
  app:
    build: .
    ports:
      - "8080:8080"
    env_file: .env
    restart: unless-stopped
EOF
        
        # Render
        cat > render.yaml << 'EOF'
services:
  - type: web
    name: izza-medical-ai
    runtime: python
    plan: free
    buildCommand: "pip install -r requirements.txt"
    startCommand: "streamlit run op.py --server.port $PORT --server.address 0.0.0.0"
EOF
        
        # Railway
        cat > railway.json << 'EOF'
{
  "build": {"builder": "NIXPACKS"},
  "deploy": {"startCommand": "streamlit run op.py --server.port $PORT --server.address 0.0.0.0"}
}
EOF
        
        # Heroku
        cat > Procfile << 'EOF'
web: sh setup.sh && streamlit run op.py --server.port $PORT --server.address 0.0.0.0
EOF
        
        cat > setup.sh << 'EOF'
mkdir -p ~/.streamlit/
echo "[server]\nport = $PORT\nenableCORS = false\n" > ~/.streamlit/config.toml
EOF
        
        # Fly.io
        cat > fly.toml << 'EOF'
app = "izza-medical-ai"
primary_region = "sjc"

[env]
  PORT = "8080"

[[services]]
  internal_port = 8080
  protocol = "tcp"

  [[services.ports]]
    port = 80
    handlers = ["http"]

  [[services.ports]]
    port = 443
    handlers = ["tls", "http"]
EOF
        
        # Vercel
        cat > vercel.json << 'EOF'
{
  "builds": [{"src": "op.py", "use": "@vercel/python"}],
  "routes": [{"src": "/(.*)", "dest": "op.py"}]
}
EOF
        
        # Netlify
        cat > netlify.toml << 'EOF'
[build]
  command = "pip install -r requirements.txt"
  publish = "."
EOF
        
        # Update git
        git add .
        git commit -m "Add deployment configurations for all platforms"
        git push origin main
        
        echo -e "${GREEN}✅ All configurations created!${NC}"
        echo ""
        echo -e "${CYAN}Quick deployment links:${NC}"
        echo "• Streamlit: https://share.streamlit.io/"
        echo "• Render: https://render.com"
        echo "• Railway: https://railway.app"
        echo "• Heroku: https://heroku.com"
        echo "• Fly.io: https://fly.io"
        echo "• Vercel: https://vercel.com"
        echo "• Netlify: https://netlify.com"
        echo ""
        echo -e "${WHITE}GitHub repo: https://github.com/BuffonEnterprises/izza-medical-ai${NC}"
        ;;
        
    *)
        echo -e "${RED}Invalid choice${NC}"
        exit 1
        ;;
esac

echo ""
echo -e "${PURPLE}╔════════════════════════════════════════════════════════════════╗${NC}"
echo -e "${PURPLE}║                    DEPLOYMENT COMPLETE!                       ║${NC}"
echo -e "${PURPLE}╚════════════════════════════════════════════════════════════════╝${NC}"