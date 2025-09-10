#!/bin/bash

# DEPLOY TO FREE SERVICES - No Credit Card Required!

set -e

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

echo -e "${CYAN}╔══════════════════════════════════════════════════════════╗${NC}"
echo -e "${CYAN}║     🚀 FREE DEPLOYMENT - IZZA MEDICAL AI 🚀             ║${NC}"
echo -e "${CYAN}║     Deploy to Render.com (100% FREE)                    ║${NC}"
echo -e "${CYAN}╚══════════════════════════════════════════════════════════╝${NC}"
echo ""

# Create .env if not exists
if [ ! -f ".env" ]; then
    cat > .env << 'EOF'
ANTHROPIC_API_KEY=
EOF
    echo -e "${YELLOW}⚠️  Add your ANTHROPIC_API_KEY to .env file${NC}"
    exit 1
fi

# Create render.yaml for automatic deployment
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
      - key: STREAMLIT_SERVER_HEADLESS
        value: true
      - key: STREAMLIT_SERVER_ENABLE_CORS
        value: false
    autoDeploy: true
EOF

# Create simplified requirements for Render
cat > requirements.render.txt << 'EOF'
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
EOF

# Create .gitignore
cat > .gitignore << 'EOF'
.env
*.pyc
__pycache__/
venv/
.venv/
*.log
.DS_Store
EOF

# Initialize git if needed
if [ ! -d ".git" ]; then
    git init
    git add .
    git commit -m "Initial commit - Izza Medical AI"
fi

echo -e "${GREEN}✅ Files prepared for deployment!${NC}"
echo ""
echo -e "${BLUE}═══════════════════════════════════════════════════════${NC}"
echo -e "${YELLOW}DEPLOYMENT INSTRUCTIONS:${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════════${NC}"
echo ""
echo -e "${GREEN}Option 1: Deploy to Render.com (Recommended - FREE)${NC}"
echo "1. Create GitHub repo: https://github.com/new"
echo "2. Push your code:"
echo "   git remote add origin YOUR_GITHUB_URL"
echo "   git push -u origin main"
echo "3. Go to: https://render.com"
echo "4. Sign up with GitHub (free)"
echo "5. Click 'New +' → 'Web Service'"
echo "6. Connect your GitHub repo"
echo "7. Add environment variable:"
echo "   ANTHROPIC_API_KEY = your_key_here"
echo "8. Click 'Create Web Service'"
echo ""
echo -e "${GREEN}Option 2: Deploy to Replit (Also FREE)${NC}"
echo "1. Go to: https://replit.com"
echo "2. Create new Repl → Import from GitHub"
echo "3. Add your repo URL"
echo "4. In Secrets, add ANTHROPIC_API_KEY"
echo "5. Click Run"
echo ""
echo -e "${GREEN}Option 3: Deploy to Streamlit Cloud (FREE)${NC}"
echo "1. Go to: https://streamlit.io/cloud"
echo "2. Sign in with GitHub"
echo "3. Deploy from your repo"
echo "4. Add ANTHROPIC_API_KEY in settings"
echo ""
echo -e "${BLUE}═══════════════════════════════════════════════════════${NC}"
echo -e "${YELLOW}LOCAL TESTING:${NC}"
echo "Run locally now: ./RUN_NOW.sh"
echo -e "${BLUE}═══════════════════════════════════════════════════════${NC}"