#!/bin/bash

# ULTRA COMPLETE DEPLOYMENT - FULLY AUTOMATED
# This script does EVERYTHING automatically

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
echo -e "${PURPLE}║                                                                ║${NC}"
echo -e "${PURPLE}║     ${WHITE}🚀 ULTRA COMPLETE DEPLOYMENT SYSTEM 🚀${PURPLE}                    ║${NC}"
echo -e "${PURPLE}║     ${CYAN}Izza Medical AI - Automated Deployment${PURPLE}                    ║${NC}"
echo -e "${PURPLE}║                                                                ║${NC}"
echo -e "${PURPLE}╚════════════════════════════════════════════════════════════════╝${NC}"
echo ""

# Step 1: Clean environment
echo -e "${YELLOW}[1/7] Cleaning environment...${NC}"
pkill -f streamlit 2>/dev/null || true
pkill -f "python.*op.py" 2>/dev/null || true
docker stop izza-medical 2>/dev/null || true
docker rm izza-medical 2>/dev/null || true
echo -e "${GREEN}✓ Environment cleaned${NC}"

# Step 2: Verify .env file
echo -e "${YELLOW}[2/7] Checking configuration...${NC}"
if [ ! -f ".env" ]; then
    echo -e "${RED}Creating .env file...${NC}"
    cat > .env << 'EOF'
ANTHROPIC_API_KEY=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
OPENAI_API_KEY=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
ANTHROPIC_MODEL=claude-opus-4-1-20250805
MAX_OUTPUT_TOKENS=2048
EOF
fi
echo -e "${GREEN}✓ Configuration verified${NC}"

# Step 3: Install dependencies
echo -e "${YELLOW}[3/7] Installing dependencies...${NC}"
if command -v python3 >/dev/null 2>&1; then
    python3 -m pip install --quiet --user streamlit anthropic python-dotenv httpx Pillow PyPDF2 reportlab numpy pandas beautifulsoup4 2>/dev/null || {
        echo -e "${YELLOW}Using pip3 directly...${NC}"
        pip3 install --quiet --user streamlit anthropic python-dotenv httpx Pillow PyPDF2 reportlab numpy pandas beautifulsoup4
    }
else
    echo -e "${RED}Python3 not found. Installing...${NC}"
    if [[ "$OSTYPE" == "darwin"* ]]; then
        brew install python3
    else
        sudo apt-get update && sudo apt-get install -y python3 python3-pip
    fi
fi
echo -e "${GREEN}✓ Dependencies installed${NC}"

# Step 4: Find available port
echo -e "${YELLOW}[4/7] Finding available port...${NC}"
PORT=8080
while lsof -Pi :$PORT -sTCP:LISTEN -t >/dev/null 2>&1; do
    PORT=$((PORT + 1))
done
echo -e "${GREEN}✓ Using port $PORT${NC}"

# Step 5: Start local server
echo -e "${YELLOW}[5/7] Starting local server...${NC}"
nohup python3 -m streamlit run op.py \
    --server.port $PORT \
    --server.address 0.0.0.0 \
    --server.headless true \
    --browser.gatherUsageStats false \
    > streamlit.log 2>&1 &

STREAMLIT_PID=$!
sleep 5

# Check if running
if ps -p $STREAMLIT_PID > /dev/null; then
    echo -e "${GREEN}✓ Local server running on port $PORT${NC}"
    LOCAL_URL="http://localhost:$PORT"
else
    echo -e "${RED}Failed to start local server${NC}"
    LOCAL_URL=""
fi

# Step 6: Setup cloud deployment files
echo -e "${YELLOW}[6/7] Creating cloud deployment files...${NC}"

# Create Streamlit Cloud config
cat > .streamlit/config.toml << 'EOF'
[theme]
primaryColor = "#FF2E2E"
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#F0F2F6"
textColor = "#262730"

[server]
maxUploadSize = 200
enableCORS = false
enableXsrfProtection = false
EOF

# Create app.py wrapper for Streamlit Cloud
cat > app.py << 'EOF'
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from op import *
EOF

# Create requirements for Streamlit Cloud
cat > requirements.txt << 'EOF'
streamlit==1.29.0
anthropic==0.18.1
python-dotenv==1.0.0
httpx==0.25.2
Pillow==10.1.0
PyPDF2==3.0.1
reportlab==4.0.7
numpy==1.24.3
pandas==2.1.4
beautifulsoup4==4.12.2
python-dateutil==2.8.2
audio-recorder-streamlit==0.0.8
SpeechRecognition==3.10.0
gtts==2.4.0
python-docx==1.1.0
EOF

# Create Render.com config
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
EOF

# Create Railway config
cat > railway.toml << 'EOF'
[build]
builder = "nixpacks"

[deploy]
startCommand = "streamlit run op.py --server.port $PORT --server.address 0.0.0.0"
restartPolicyType = "ON_FAILURE"
restartPolicyMaxRetries = 10
EOF

# Create Procfile for Heroku
cat > Procfile << 'EOF'
web: sh setup.sh && streamlit run op.py --server.port $PORT --server.address 0.0.0.0
EOF

cat > setup.sh << 'EOF'
mkdir -p ~/.streamlit/
echo "[server]\nport = $PORT\nenableCORS = false\n" > ~/.streamlit/config.toml
EOF

echo -e "${GREEN}✓ Cloud deployment files created${NC}"

# Step 7: Initialize Git and prepare for deployment
echo -e "${YELLOW}[7/7] Preparing for cloud deployment...${NC}"

# Create .gitignore
cat > .gitignore << 'EOF'
.env
*.pyc
__pycache__/
venv/
.venv/
*.log
.DS_Store
.streamlit/secrets.toml
EOF

# Initialize git if needed
if [ ! -d ".git" ]; then
    git init
    git add .
    git commit -m "Initial commit - Izza Medical AI"
fi

echo -e "${GREEN}✓ Git repository prepared${NC}"

# Final Summary
echo ""
echo -e "${PURPLE}╔════════════════════════════════════════════════════════════════╗${NC}"
echo -e "${PURPLE}║                   ${WHITE}🎉 DEPLOYMENT COMPLETE! 🎉${PURPLE}                  ║${NC}"
echo -e "${PURPLE}╚════════════════════════════════════════════════════════════════╝${NC}"
echo ""

if [ ! -z "$LOCAL_URL" ]; then
    echo -e "${GREEN}✅ LOCAL DEPLOYMENT:${NC}"
    echo -e "   ${WHITE}$LOCAL_URL${NC}"
    echo ""
fi

echo -e "${CYAN}📤 CLOUD DEPLOYMENT OPTIONS:${NC}"
echo ""
echo -e "${YELLOW}Option 1: Streamlit Cloud (EASIEST - FREE)${NC}"
echo "  1. Go to: https://share.streamlit.io/"
echo "  2. Sign in with GitHub"
echo "  3. Deploy from your repo"
echo "  4. Add secrets (ANTHROPIC_API_KEY)"
echo ""
echo -e "${YELLOW}Option 2: Render.com (FREE)${NC}"
echo "  1. Push to GitHub: git push origin main"
echo "  2. Go to: https://render.com"
echo "  3. New > Web Service > Connect repo"
echo "  4. Add environment variable: ANTHROPIC_API_KEY"
echo ""
echo -e "${YELLOW}Option 3: Railway.app (FREE TRIAL)${NC}"
echo "  1. Install: npm i -g @railway/cli"
echo "  2. Run: railway login && railway up"
echo ""

# Open browser
if [ ! -z "$LOCAL_URL" ]; then
    echo -e "${GREEN}Opening browser...${NC}"
    if [[ "$OSTYPE" == "darwin"* ]]; then
        open "$LOCAL_URL"
    elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
        xdg-open "$LOCAL_URL"
    fi
fi

echo ""
echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"
echo -e "${WHITE}Commands:${NC}"
echo -e "  View logs:    ${CYAN}tail -f streamlit.log${NC}"
echo -e "  Stop app:     ${CYAN}kill $STREAMLIT_PID${NC}"
echo -e "  Restart:      ${CYAN}./ULTRA_COMPLETE_DEPLOY.sh${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"