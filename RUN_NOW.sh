#!/bin/bash

# IMMEDIATE DEPLOYMENT - Works without any cloud billing
# This script will get your app running NOW

set -e

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${BLUE}═══════════════════════════════════════════════════════${NC}"
echo -e "${BLUE}    🚀 IZZA MEDICAL AI - INSTANT DEPLOYMENT 🚀         ${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════════${NC}"
echo ""

# Check for .env file
if [ ! -f ".env" ]; then
    echo -e "${YELLOW}Creating .env file...${NC}"
    cat > .env << 'EOF'
# ADD YOUR KEY HERE (required)
ANTHROPIC_API_KEY=

# Optional
ANTHROPIC_MODEL=claude-opus-4-1-20250805
MAX_OUTPUT_TOKENS=2048
EOF
    
    echo -e "${RED}⚠️  IMPORTANT: Add your ANTHROPIC_API_KEY to .env file!${NC}"
    echo -e "${YELLOW}Get your key from: https://console.anthropic.com/${NC}"
    echo ""
    echo "Press Enter after adding your key..."
    read
fi

# Check if key is set
if ! grep -q "ANTHROPIC_API_KEY=sk-" .env 2>/dev/null; then
    echo -e "${RED}❌ No API key found in .env!${NC}"
    echo "Please add your Anthropic API key to .env file"
    exit 1
fi

echo -e "${GREEN}✅ API key detected${NC}"
echo ""

# Method 1: Try Python directly (fastest)
echo -e "${YELLOW}Starting deployment...${NC}"

if command -v python3 >/dev/null 2>&1; then
    echo -e "${BLUE}Using Python 3...${NC}"
    
    # Install requirements
    echo "Installing dependencies..."
    python3 -m pip install --user streamlit anthropic python-dotenv httpx Pillow PyPDF2 reportlab audio-recorder-streamlit SpeechRecognition gtts python-docx numpy pandas beautifulsoup4 python-dateutil
    
    # Run the app
    echo -e "${GREEN}🎉 Starting Izza Medical AI...${NC}"
    python3 -m streamlit run op.py --server.port 8080 --server.address 0.0.0.0
    
elif command -v python >/dev/null 2>&1; then
    echo -e "${BLUE}Using Python...${NC}"
    
    # Install requirements
    echo "Installing dependencies..."
    python -m pip install --user streamlit anthropic python-dotenv httpx Pillow PyPDF2 reportlab audio-recorder-streamlit SpeechRecognition gtts python-docx numpy pandas beautifulsoup4 python-dateutil
    
    # Run the app
    echo -e "${GREEN}🎉 Starting Izza Medical AI...${NC}"
    python -m streamlit run op.py --server.port 8080 --server.address 0.0.0.0
    
else
    echo -e "${RED}Python not found! Installing...${NC}"
    
    # Try to install Python
    if [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS
        if command -v brew >/dev/null 2>&1; then
            brew install python3
        else
            echo "Please install Python from: https://www.python.org/downloads/"
            exit 1
        fi
    else
        # Linux
        sudo apt-get update && sudo apt-get install -y python3 python3-pip
    fi
    
    # Retry
    $0
fi