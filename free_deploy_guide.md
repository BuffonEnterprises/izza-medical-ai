# 🚀 Izza Medical AI - Complete Deployment Guide

## ⚠️ Current Status
Your GCP project (primeversion-468523) has a billing issue. Here are alternative deployment options:

## Option 1: Fix GCP Billing and Deploy to Cloud Run

### Steps to Fix Billing:
1. Go to: https://console.cloud.google.com/billing
2. Link a valid payment method to project `primeversion-468523`
3. Once billing is enabled, run:
```bash
./deploy.sh
```

## Option 2: Deploy Locally with Docker (Recommended for Testing)

### Quick Start:
```bash
# 1. Make sure Docker is installed
# 2. Create .env file with your API key
echo "ANTHROPIC_API_KEY=your_key_here" > .env

# 3. Build and run
docker build -t izza-medical .
docker run -p 8080:8080 --env-file .env izza-medical
```

Access at: http://localhost:8080

## Option 3: Deploy to Free Cloud Platforms

### A. Deploy to Render.com (FREE)
1. Push code to GitHub
2. Go to https://render.com
3. Sign up for free account
4. Create new "Web Service"
5. Connect your GitHub repo
6. Set environment variables:
   - `ANTHROPIC_API_KEY`: your_key_here
7. Deploy!

### B. Deploy to Railway.app (FREE Trial)
```bash
# Install Railway CLI
npm install -g @railway/cli

# Deploy
railway login
railway init
railway add
railway up
```

### C. Deploy to Heroku (FREE Tier Limited)
```bash
# Install Heroku CLI first
heroku create izza-medical-ai
heroku config:set ANTHROPIC_API_KEY=your_key_here
git push heroku main
```

## Option 4: Deploy to Another GCP Project

### Create New Project with Active Billing:
```bash
# Create new project
gcloud projects create izza-medical-ai-new --name="Izza Medical AI"

# Set billing account
gcloud beta billing projects link izza-medical-ai-new \
  --billing-account=YOUR_BILLING_ACCOUNT_ID

# Switch to new project
gcloud config set project izza-medical-ai-new

# Deploy
./deploy.sh
```

## Option 5: Use Google Cloud Free Tier

### Requirements for Free Tier:
- New Google Cloud account
- $300 free credits for 90 days
- No charges until you upgrade

### Steps:
1. Create new Google account (if needed)
2. Go to: https://cloud.google.com/free
3. Sign up for free trial
4. Create new project
5. Run deployment script

## 📋 Files Created for Deployment

| File | Purpose |
|------|---------|
| `Dockerfile` | Container configuration |
| `requirements.txt` | Python dependencies |
| `cloudbuild.yaml` | Google Cloud Build config |
| `.gcloudignore` | Files to exclude from deployment |
| `deploy.sh` | Automated GCP deployment |
| `local_deploy.sh` | Local/alternative deployment |

## 🔑 Environment Variables Required

```env
# Required
ANTHROPIC_API_KEY=sk-ant-...

# Optional for enhanced features
OPENAI_API_KEY=sk-...
AZURE_SPEECH_KEY=...
AZURE_SPEECH_REGION=eastus
```

## 🚨 Troubleshooting

### Issue: Billing Account Disabled
**Solution**: Enable billing at https://console.cloud.google.com/billing

### Issue: APIs Not Enabled
**Solution**: Run:
```bash
gcloud services enable cloudbuild.googleapis.com run.googleapis.com
```

### Issue: Permission Denied
**Solution**: Check your role:
```bash
gcloud projects get-iam-policy primeversion-468523
```

### Issue: Build Fails
**Solution**: Try local Docker build:
```bash
docker build -t izza-medical .
docker run -p 8080:8080 --env-file .env izza-medical
```

## 📞 Quick Commands

```bash
# Check billing status
gcloud beta billing accounts list

# View project info
gcloud projects describe primeversion-468523

# Test locally
./local_deploy.sh

# Deploy to GCP (when billing fixed)
./deploy.sh
```

## 🎯 Recommended Next Steps

1. **For Testing**: Use local Docker deployment
2. **For Production**: Fix GCP billing or use Render.com
3. **For Development**: Run locally with Python

## 📚 Resources

- [Google Cloud Run Docs](https://cloud.google.com/run/docs)
- [Streamlit Deployment](https://docs.streamlit.io/streamlit-community-cloud/get-started)
- [Docker Documentation](https://docs.docker.com/)
- [Anthropic API Docs](https://docs.anthropic.com/)

---

**Need Help?** 
- Check application logs: `docker logs izza-medical`
- View GCP logs: `gcloud run logs read`
- Test API key: `echo $ANTHROPIC_API_KEY`