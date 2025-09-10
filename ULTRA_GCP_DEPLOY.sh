#!/bin/bash

# ULTRA GOOGLE CLOUD RUN DEPLOYMENT
# This script tries ALL methods to deploy to GCP

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
echo -e "${PURPLE}║           🚀 ULTRA GCP CLOUD RUN DEPLOYMENT 🚀                ║${NC}"
echo -e "${PURPLE}║           Deploying Izza Medical AI to Google Cloud           ║${NC}"
echo -e "${PURPLE}╚════════════════════════════════════════════════════════════════╝${NC}"
echo ""

# Available projects
PROJECTS=(
    "model-union-469912-h2"
    "snappy-airway-469911-t7"
    "ordinal-ember-468522-c9"
    "mystic-keel-092sd"
    "primeversion-468523"
)

# Configuration
SERVICE_NAME="izza-medical-ai"
REGION="us-central1"
WORKING_PROJECT=""

# Function to check project billing
check_project_billing() {
    local project=$1
    echo -e "${YELLOW}Checking project: $project${NC}"
    
    # Set project
    gcloud config set project "$project" 2>/dev/null || return 1
    
    # Try to list services (will fail if billing disabled)
    if gcloud services list --enabled --limit=1 2>/dev/null | grep -q "NAME"; then
        echo -e "${GREEN}✓ Project $project has active billing${NC}"
        return 0
    else
        echo -e "${RED}✗ Project $project has billing issues${NC}"
        return 1
    fi
}

# Function to find working project
find_working_project() {
    echo -e "${CYAN}[1/7] Finding project with active billing...${NC}"
    
    for project in "${PROJECTS[@]}"; do
        if check_project_billing "$project"; then
            WORKING_PROJECT="$project"
            echo -e "${GREEN}✓ Using project: $WORKING_PROJECT${NC}"
            return 0
        fi
    done
    
    echo -e "${RED}No projects with active billing found${NC}"
    return 1
}

# Function to enable APIs
enable_apis() {
    echo -e "${CYAN}[2/7] Enabling required APIs...${NC}"
    
    gcloud services enable \
        cloudbuild.googleapis.com \
        run.googleapis.com \
        containerregistry.googleapis.com \
        artifactregistry.googleapis.com \
        --project "$WORKING_PROJECT" 2>/dev/null || {
        echo -e "${YELLOW}Some APIs may already be enabled${NC}"
    }
    
    echo -e "${GREEN}✓ APIs enabled${NC}"
}

# Function to build with Cloud Build
build_with_cloud_build() {
    echo -e "${CYAN}[3/7] Building with Cloud Build...${NC}"
    
    # Create optimized cloudbuild.yaml
    cat > cloudbuild-ultra.yaml << EOF
steps:
  # Build the container image
  - name: 'gcr.io/cloud-builders/docker'
    args: ['build', '-t', 'gcr.io/$WORKING_PROJECT/$SERVICE_NAME:latest', '.']
    
  # Push to Container Registry
  - name: 'gcr.io/cloud-builders/docker'
    args: ['push', 'gcr.io/$WORKING_PROJECT/$SERVICE_NAME:latest']

images:
  - 'gcr.io/$WORKING_PROJECT/$SERVICE_NAME:latest'

timeout: '1200s'
EOF
    
    # Try Cloud Build
    if gcloud builds submit \
        --config cloudbuild-ultra.yaml \
        --project "$WORKING_PROJECT" \
        --quiet 2>/dev/null; then
        echo -e "${GREEN}✓ Build successful${NC}"
        return 0
    else
        echo -e "${YELLOW}Cloud Build failed, trying alternative...${NC}"
        return 1
    fi
}

# Function to build locally
build_locally() {
    echo -e "${CYAN}[3/7] Building Docker image locally...${NC}"
    
    # Configure Docker for GCR
    gcloud auth configure-docker --quiet
    
    # Build image
    docker build -t "gcr.io/$WORKING_PROJECT/$SERVICE_NAME:latest" . || {
        echo -e "${RED}Docker build failed${NC}"
        return 1
    }
    
    echo -e "${GREEN}✓ Docker image built${NC}"
    
    # Push to GCR
    echo -e "${CYAN}[4/7] Pushing to Container Registry...${NC}"
    docker push "gcr.io/$WORKING_PROJECT/$SERVICE_NAME:latest" || {
        echo -e "${RED}Push failed${NC}"
        return 1
    }
    
    echo -e "${GREEN}✓ Image pushed to GCR${NC}"
    return 0
}

# Function to deploy from source
deploy_from_source() {
    echo -e "${CYAN}[5/7] Deploying directly from source...${NC}"
    
    # Read API key from .env
    if [ -f .env ]; then
        export $(grep -v '^#' .env | xargs)
    fi
    
    gcloud run deploy "$SERVICE_NAME" \
        --source . \
        --region "$REGION" \
        --platform managed \
        --allow-unauthenticated \
        --memory 2Gi \
        --cpu 2 \
        --timeout 900 \
        --max-instances 10 \
        --min-instances 0 \
        --port 8080 \
        --set-env-vars "ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY},STREAMLIT_SERVER_HEADLESS=true,STREAMLIT_SERVER_PORT=8080" \
        --project "$WORKING_PROJECT" 2>&1 | tee deploy.log
    
    if [ ${PIPESTATUS[0]} -eq 0 ]; then
        echo -e "${GREEN}✓ Deployment successful${NC}"
        return 0
    else
        echo -e "${YELLOW}Direct deployment failed${NC}"
        return 1
    fi
}

# Function to deploy from image
deploy_from_image() {
    echo -e "${CYAN}[5/7] Deploying from container image...${NC}"
    
    # Read API key from .env
    if [ -f .env ]; then
        export $(grep -v '^#' .env | xargs)
    fi
    
    gcloud run deploy "$SERVICE_NAME" \
        --image "gcr.io/$WORKING_PROJECT/$SERVICE_NAME:latest" \
        --region "$REGION" \
        --platform managed \
        --allow-unauthenticated \
        --memory 2Gi \
        --cpu 2 \
        --timeout 900 \
        --max-instances 10 \
        --min-instances 0 \
        --port 8080 \
        --set-env-vars "ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY},STREAMLIT_SERVER_HEADLESS=true,STREAMLIT_SERVER_PORT=8080" \
        --project "$WORKING_PROJECT"
    
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✓ Deployment successful${NC}"
        return 0
    else
        echo -e "${RED}Deployment failed${NC}"
        return 1
    fi
}

# Main execution
main() {
    # Step 1: Find working project
    if ! find_working_project; then
        echo -e "${RED}Cannot proceed without active billing${NC}"
        echo ""
        echo -e "${YELLOW}Alternative: Creating new project with free tier...${NC}"
        
        # Try to create new project
        NEW_PROJECT="izza-medical-$(date +%s)"
        echo -e "${CYAN}Creating project: $NEW_PROJECT${NC}"
        
        if gcloud projects create "$NEW_PROJECT" --name="Izza Medical AI"; then
            WORKING_PROJECT="$NEW_PROJECT"
            gcloud config set project "$WORKING_PROJECT"
            echo -e "${GREEN}✓ New project created: $WORKING_PROJECT${NC}"
            echo -e "${YELLOW}Note: You need to enable billing for this project${NC}"
            echo "Visit: https://console.cloud.google.com/billing/linkedaccount?project=$WORKING_PROJECT"
            echo "Press Enter after enabling billing..."
            read
        else
            echo -e "${RED}Failed to create new project${NC}"
            exit 1
        fi
    fi
    
    # Step 2: Enable APIs
    enable_apis
    
    # Step 3: Try deployment methods
    echo -e "${CYAN}Attempting deployment...${NC}"
    
    # Method 1: Direct source deployment (simplest)
    if deploy_from_source; then
        echo -e "${GREEN}✓ Deployed from source${NC}"
    else
        # Method 2: Build with Cloud Build
        if build_with_cloud_build; then
            deploy_from_image
        else
            # Method 3: Local build and push
            if build_locally; then
                deploy_from_image
            else
                echo -e "${RED}All deployment methods failed${NC}"
                exit 1
            fi
        fi
    fi
    
    # Step 6: Get service URL
    echo -e "${CYAN}[6/7] Getting service URL...${NC}"
    SERVICE_URL=$(gcloud run services describe "$SERVICE_NAME" \
        --region "$REGION" \
        --format 'value(status.url)' \
        --project "$WORKING_PROJECT")
    
    if [ -z "$SERVICE_URL" ]; then
        echo -e "${RED}Failed to get service URL${NC}"
        exit 1
    fi
    
    # Step 7: Final summary
    echo ""
    echo -e "${PURPLE}╔════════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${PURPLE}║              🎉 DEPLOYMENT SUCCESSFUL! 🎉                     ║${NC}"
    echo -e "${PURPLE}╚════════════════════════════════════════════════════════════════╝${NC}"
    echo ""
    echo -e "${GREEN}✅ CLOUD RUN DEPLOYMENT COMPLETE${NC}"
    echo -e "${WHITE}Project: $WORKING_PROJECT${NC}"
    echo -e "${WHITE}Service: $SERVICE_NAME${NC}"
    echo -e "${WHITE}Region: $REGION${NC}"
    echo ""
    echo -e "${CYAN}🌐 Your application is live at:${NC}"
    echo -e "${GREEN}   $SERVICE_URL${NC}"
    echo ""
    echo -e "${YELLOW}📊 Management Commands:${NC}"
    echo "  View logs:     gcloud run logs read --service $SERVICE_NAME --region $REGION --project $WORKING_PROJECT"
    echo "  View metrics:  gcloud run services describe $SERVICE_NAME --region $REGION --project $WORKING_PROJECT"
    echo "  Update:        gcloud run deploy $SERVICE_NAME --source . --region $REGION --project $WORKING_PROJECT"
    echo ""
    
    # Open in browser
    echo -e "${GREEN}Opening in browser...${NC}"
    open "$SERVICE_URL" 2>/dev/null || xdg-open "$SERVICE_URL" 2>/dev/null || echo "Please open: $SERVICE_URL"
}

# Run main function
main "$@"