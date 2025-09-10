#!/bin/bash

# Izza Medical AI - Complete Cloud Run Deployment Script
# Project: primeversion-468523

set -e

echo "🚀 Starting Izza Medical AI deployment to Google Cloud Run..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Configuration
PROJECT_ID="primeversion-468523"
REGION="us-central1"
SERVICE_NAME="izza-medical-ai"
IMAGE_NAME="gcr.io/${PROJECT_ID}/${SERVICE_NAME}"

# Check if gcloud is installed
if ! command -v gcloud &> /dev/null; then
    echo -e "${RED}❌ gcloud CLI is not installed. Please install it first.${NC}"
    exit 1
fi

# Check if logged in
echo -e "${YELLOW}📋 Checking GCP authentication...${NC}"
if ! gcloud auth list --filter=status:ACTIVE --format="value(account)" | grep -q .; then
    echo -e "${RED}❌ Not logged in to GCP. Please run: gcloud auth login${NC}"
    exit 1
fi

# Set project
echo -e "${YELLOW}📋 Setting project to ${PROJECT_ID}...${NC}"
gcloud config set project ${PROJECT_ID}

# Enable required APIs
echo -e "${YELLOW}🔧 Enabling required GCP APIs...${NC}"
gcloud services enable \
    cloudbuild.googleapis.com \
    run.googleapis.com \
    containerregistry.googleapis.com \
    artifactregistry.googleapis.com \
    secretmanager.googleapis.com

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo -e "${YELLOW}⚠️  No .env file found. Creating template...${NC}"
    cat > .env << EOF
# Anthropic API Configuration
ANTHROPIC_API_KEY=your_anthropic_api_key_here
ANTHROPIC_MODEL=claude-opus-4-1-20250805
ANTHROPIC_FALLBACK_MODEL=claude-3-5-sonnet-20240620

# Optional API Keys for enhanced features
OPENAI_API_KEY=
AZURE_SPEECH_KEY=
AZURE_SPEECH_REGION=eastus

# Performance Settings
MAX_OUTPUT_TOKENS=2048
MAX_OUTPUT_TOKENS_EXTENDED=4096
MAX_HISTORY_MESSAGES=12
MAX_HISTORY_CHARS=16000
ATTACH_TEXT_CHAR_CAP=12000
PDF_MAX_PAGES=5
IMAGE_MAX_DIM=1280
IMAGE_JPEG_QUALITY=80

# Proxy (optional)
HTTPS_PROXY=
HTTP_PROXY=
EOF
    echo -e "${RED}⚠️  Please edit .env file with your API keys before deploying!${NC}"
    echo -e "${YELLOW}Press Enter to continue after editing .env file...${NC}"
    read
fi

# Build with Cloud Build
echo -e "${YELLOW}🏗️  Starting Cloud Build...${NC}"
gcloud builds submit --config cloudbuild.yaml \
    --substitutions=COMMIT_SHA=latest \
    --timeout=20m

# Alternative: Direct deployment (if Cloud Build fails)
if [ $? -ne 0 ]; then
    echo -e "${YELLOW}⚠️  Cloud Build failed. Trying direct deployment...${NC}"
    
    # Build locally
    echo -e "${YELLOW}🐳 Building Docker image locally...${NC}"
    docker build -t ${IMAGE_NAME}:latest .
    
    # Push to Container Registry
    echo -e "${YELLOW}📤 Pushing image to Container Registry...${NC}"
    docker push ${IMAGE_NAME}:latest
    
    # Deploy to Cloud Run
    echo -e "${YELLOW}🚀 Deploying to Cloud Run...${NC}"
    gcloud run deploy ${SERVICE_NAME} \
        --image ${IMAGE_NAME}:latest \
        --region ${REGION} \
        --platform managed \
        --allow-unauthenticated \
        --memory 2Gi \
        --cpu 2 \
        --timeout 900 \
        --max-instances 10 \
        --min-instances 0 \
        --port 8080 \
        --set-env-vars "STREAMLIT_SERVER_HEADLESS=true,STREAMLIT_SERVER_PORT=8080,STREAMLIT_SERVER_ADDRESS=0.0.0.0"
fi

# Get service URL
echo -e "${YELLOW}📍 Getting service URL...${NC}"
SERVICE_URL=$(gcloud run services describe ${SERVICE_NAME} \
    --region ${REGION} \
    --format 'value(status.url)')

if [ -z "$SERVICE_URL" ]; then
    echo -e "${RED}❌ Failed to get service URL${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Deployment successful!${NC}"
echo -e "${GREEN}🌐 Your application is available at:${NC}"
echo -e "${GREEN}   ${SERVICE_URL}${NC}"
echo ""
echo -e "${YELLOW}📊 Additional commands:${NC}"
echo "  View logs:     gcloud run logs read --service ${SERVICE_NAME} --region ${REGION}"
echo "  View metrics:  gcloud run services describe ${SERVICE_NAME} --region ${REGION}"
echo "  Update env:    gcloud run services update ${SERVICE_NAME} --update-env-vars KEY=VALUE --region ${REGION}"
echo ""
echo -e "${YELLOW}⚠️  Important: Make sure to set your API keys as environment variables in Cloud Run:${NC}"
echo "  gcloud run services update ${SERVICE_NAME} --update-env-vars ANTHROPIC_API_KEY=your_key --region ${REGION}"