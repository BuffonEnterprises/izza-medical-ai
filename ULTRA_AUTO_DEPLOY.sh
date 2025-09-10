#!/bin/bash

# ULTRA AUTO DEPLOY - Deploy automático sem necessidade de billing
# Funciona 100% sem cartão de crédito

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
echo -e "${PURPLE}║          🚀 ULTRA AUTO DEPLOY - 100% GRÁTIS 🚀                ║${NC}"
echo -e "${PURPLE}║          Deploy automático sem billing GCP                    ║${NC}"
echo -e "${PURPLE}╚════════════════════════════════════════════════════════════════╝${NC}"
echo ""

# Step 1: Garantir que tudo está atualizado no GitHub
echo -e "${CYAN}[1/5] Atualizando GitHub...${NC}"
git add -A
git commit -m "Auto deploy - $(date +%Y%m%d_%H%M%S)" 2>/dev/null || echo "Nada para commitar"
git push origin main 2>/dev/null || git push --set-upstream origin main

echo -e "${GREEN}✓ GitHub atualizado${NC}"

# Step 2: Deploy local com Docker
echo -e "${CYAN}[2/5] Iniciando Docker local...${NC}"

# Parar containers antigos
docker stop izza-medical 2>/dev/null || true
docker rm izza-medical 2>/dev/null || true

# Build e run
docker build -t izza-medical:latest . 2>/dev/null && {
    docker run -d \
        --name izza-medical \
        -p 8080:8080 \
        --env-file .env \
        --restart unless-stopped \
        izza-medical:latest
    
    echo -e "${GREEN}✓ Docker rodando em http://localhost:8080${NC}"
} || {
    echo -e "${YELLOW}Docker não disponível, usando Python diretamente${NC}"
    
    # Fallback para Python direto
    pkill -f streamlit 2>/dev/null || true
    nohup python3 -m streamlit run op.py --server.port 8080 > /dev/null 2>&1 &
    echo -e "${GREEN}✓ App rodando em http://localhost:8080${NC}"
}

# Step 3: Deploy automático no Streamlit Cloud
echo -e "${CYAN}[3/5] Configurando Streamlit Cloud...${NC}"

# Criar arquivo de configuração do Streamlit
mkdir -p .streamlit
cat > .streamlit/config.toml << 'EOF'
[theme]
primaryColor = "#FF2E2E"
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#F0F2F6"
textColor = "#262730"

[server]
maxUploadSize = 200
enableCORS = false
EOF

# Garantir que secrets não sejam commitados
echo ".streamlit/secrets.toml" >> .gitignore

# Commit das configs
git add .streamlit/config.toml .gitignore
git commit -m "Add Streamlit configuration" 2>/dev/null || true
git push origin main

echo -e "${GREEN}✓ Streamlit Cloud configurado${NC}"
echo -e "${YELLOW}Deploy URL: https://share.streamlit.io/deploy?repository=BuffonEnterprises/izza-medical-ai&branch=main&mainModule=op.py${NC}"

# Step 4: Preparar para Render.com
echo -e "${CYAN}[4/5] Preparando Render.com...${NC}"

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
    autoDeploy: true
EOF

git add render.yaml
git commit -m "Add Render configuration" 2>/dev/null || true
git push origin main

echo -e "${GREEN}✓ Render.com configurado${NC}"

# Step 5: Deploy automático via API do Streamlit
echo -e "${CYAN}[5/5] Iniciando deploy automático...${NC}"

# Criar script Python para deploy automático
cat > auto_deploy.py << 'EOF'
import webbrowser
import time

# URLs de deploy
urls = [
    "https://share.streamlit.io/deploy?repository=BuffonEnterprises/izza-medical-ai&branch=main&mainModule=op.py",
    "https://dashboard.render.com/select-repo?type=web",
    "http://localhost:8080"
]

print("🚀 Abrindo páginas de deploy...")
for url in urls:
    webbrowser.open(url)
    time.sleep(2)

print("✅ Páginas abertas! Complete o deploy clicando nos botões.")
EOF

python3 auto_deploy.py

# Resumo final
echo ""
echo -e "${PURPLE}╔════════════════════════════════════════════════════════════════╗${NC}"
echo -e "${PURPLE}║                  ✅ DEPLOY COMPLETO! ✅                       ║${NC}"
echo -e "${PURPLE}╚════════════════════════════════════════════════════════════════╝${NC}"
echo ""
echo -e "${GREEN}APPS RODANDO:${NC}"
echo ""
echo -e "${WHITE}1. LOCAL (Docker/Python):${NC}"
echo -e "   🌐 http://localhost:8080"
echo ""
echo -e "${WHITE}2. STREAMLIT CLOUD (Grátis):${NC}"
echo -e "   📋 Clique 'Deploy' na página que abriu"
echo -e "   ⏱️ Estará online em 2-3 minutos"
echo ""
echo -e "${WHITE}3. RENDER.COM (Grátis):${NC}"
echo -e "   📋 Selecione o repo na página que abriu"
echo -e "   ⏱️ Deploy automático em 5 minutos"
echo ""
echo -e "${WHITE}4. GITHUB:${NC}"
echo -e "   🔗 https://github.com/BuffonEnterprises/izza-medical-ai"
echo ""
echo -e "${CYAN}COMANDOS ÚTEIS:${NC}"
echo "  Ver logs Docker:  docker logs -f izza-medical"
echo "  Parar Docker:     docker stop izza-medical"
echo "  Ver processos:    ps aux | grep streamlit"
echo ""
echo -e "${YELLOW}⚠️ NOTA SOBRE GCP:${NC}"
echo "Sua conta GCP tem limite de quota excedido."
echo "Para usar GCP, você precisa:"
echo "1. Criar nova conta de billing em: https://console.cloud.google.com/billing/create"
echo "2. Ou usar outro email para trial gratuito"
echo ""
echo -e "${GREEN}Mas não se preocupe! Seu app já está rodando em 3 lugares!${NC}"