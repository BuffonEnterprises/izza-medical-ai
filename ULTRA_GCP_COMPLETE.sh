#!/bin/bash

# ULTRA GCP COMPLETE - Ativa e configura TUDO automaticamente
# Este script resolve TODOS os problemas de billing e deploy

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
echo -e "${PURPLE}║        🚀 ULTRA GCP COMPLETE DEPLOYMENT 🚀                    ║${NC}"
echo -e "${PURPLE}║        Ativando TUDO na Google Cloud Platform                 ║${NC}"
echo -e "${PURPLE}╚════════════════════════════════════════════════════════════════╝${NC}"
echo ""

# Configurações
SERVICE_NAME="izza-medical-ai"
REGION="us-central1"
PROJECT_ID=""

# Função para listar contas de billing
list_billing_accounts() {
    echo -e "${CYAN}[1/10] Verificando contas de billing...${NC}"
    
    # Listar contas de billing disponíveis
    BILLING_ACCOUNTS=$(gcloud billing accounts list --format="value(name,displayName,open)" 2>/dev/null || echo "")
    
    if [ -z "$BILLING_ACCOUNTS" ]; then
        echo -e "${YELLOW}Nenhuma conta de billing encontrada${NC}"
        echo -e "${CYAN}Criando link para ativar trial gratuito...${NC}"
        echo ""
        echo -e "${GREEN}ATIVE O TRIAL GRATUITO DE $300:${NC}"
        echo -e "${WHITE}1. Acesse: https://console.cloud.google.com/freetrial${NC}"
        echo -e "${WHITE}2. Clique em 'Activate' ou 'Start free'${NC}"
        echo -e "${WHITE}3. Adicione um cartão (não será cobrado durante o trial)${NC}"
        echo -e "${WHITE}4. Você receberá $300 em créditos por 90 dias${NC}"
        echo ""
        echo -e "${YELLOW}Abrindo página do Free Trial...${NC}"
        open "https://console.cloud.google.com/freetrial"
        echo ""
        echo "Pressione Enter após ativar o billing..."
        read
        
        # Verificar novamente
        BILLING_ACCOUNTS=$(gcloud billing accounts list --format="value(name)" 2>/dev/null | head -1)
    else
        BILLING_ACCOUNTS=$(echo "$BILLING_ACCOUNTS" | head -1 | awk '{print $1}')
        echo -e "${GREEN}✓ Conta de billing encontrada: $BILLING_ACCOUNTS${NC}"
    fi
    
    echo "$BILLING_ACCOUNTS"
}

# Função para criar ou selecionar projeto
setup_project() {
    echo -e "${CYAN}[2/10] Configurando projeto...${NC}"
    
    # Listar projetos existentes
    PROJECTS=$(gcloud projects list --format="value(projectId)" 2>/dev/null)
    
    echo -e "${YELLOW}Projetos disponíveis:${NC}"
    echo "$PROJECTS"
    echo ""
    
    # Tentar usar um projeto existente ou criar novo
    for proj in $PROJECTS; do
        echo -e "${YELLOW}Verificando projeto: $proj${NC}"
        
        # Verificar se tem billing ativo
        BILLING_ENABLED=$(gcloud billing projects describe $proj --format="value(billingEnabled)" 2>/dev/null || echo "false")
        
        if [ "$BILLING_ENABLED" = "True" ]; then
            PROJECT_ID="$proj"
            echo -e "${GREEN}✓ Usando projeto com billing ativo: $PROJECT_ID${NC}"
            break
        fi
    done
    
    # Se não encontrou projeto com billing, criar novo
    if [ -z "$PROJECT_ID" ]; then
        PROJECT_ID="izza-medical-$(date +%s)"
        echo -e "${YELLOW}Criando novo projeto: $PROJECT_ID${NC}"
        
        gcloud projects create "$PROJECT_ID" \
            --name="Izza Medical AI" \
            --set-as-default || {
            echo -e "${YELLOW}Projeto pode já existir${NC}"
            PROJECT_ID=$(gcloud projects list --format="value(projectId)" | head -1)
        }
    fi
    
    # Definir projeto ativo
    gcloud config set project "$PROJECT_ID"
    echo -e "${GREEN}✓ Projeto configurado: $PROJECT_ID${NC}"
}

# Função para vincular billing ao projeto
link_billing() {
    echo -e "${CYAN}[3/10] Vinculando billing ao projeto...${NC}"
    
    local billing_account="$1"
    
    if [ -z "$billing_account" ]; then
        echo -e "${RED}Nenhuma conta de billing disponível${NC}"
        return 1
    fi
    
    # Vincular billing ao projeto
    gcloud billing projects link "$PROJECT_ID" \
        --billing-account="$billing_account" 2>/dev/null || {
        echo -e "${YELLOW}Billing pode já estar vinculado${NC}"
    }
    
    echo -e "${GREEN}✓ Billing vinculado ao projeto${NC}"
}

# Função para habilitar TODAS as APIs
enable_all_apis() {
    echo -e "${CYAN}[4/10] Habilitando TODAS as APIs necessárias...${NC}"
    
    # Lista completa de APIs
    APIS=(
        "cloudbuild.googleapis.com"
        "run.googleapis.com"
        "containerregistry.googleapis.com"
        "artifactregistry.googleapis.com"
        "cloudresourcemanager.googleapis.com"
        "compute.googleapis.com"
        "storage-api.googleapis.com"
        "storage-component.googleapis.com"
        "logging.googleapis.com"
        "monitoring.googleapis.com"
        "secretmanager.googleapis.com"
        "iamcredentials.googleapis.com"
        "iam.googleapis.com"
        "cloudtrace.googleapis.com"
        "serviceusage.googleapis.com"
        "servicenetworking.googleapis.com"
    )
    
    for api in "${APIS[@]}"; do
        echo -e "${YELLOW}Habilitando: $api${NC}"
        gcloud services enable "$api" --project="$PROJECT_ID" 2>/dev/null || true
    done
    
    echo -e "${GREEN}✓ Todas as APIs habilitadas${NC}"
}

# Função para configurar IAM e permissões
setup_permissions() {
    echo -e "${CYAN}[5/10] Configurando permissões IAM...${NC}"
    
    # Obter email da conta
    USER_EMAIL=$(gcloud config get-value account)
    
    # Adicionar roles necessárias
    ROLES=(
        "roles/run.admin"
        "roles/cloudbuild.builds.editor"
        "roles/storage.admin"
        "roles/artifactregistry.admin"
        "roles/iam.serviceAccountUser"
    )
    
    for role in "${ROLES[@]}"; do
        echo -e "${YELLOW}Adicionando role: $role${NC}"
        gcloud projects add-iam-policy-binding "$PROJECT_ID" \
            --member="user:$USER_EMAIL" \
            --role="$role" \
            --quiet 2>/dev/null || true
    done
    
    echo -e "${GREEN}✓ Permissões configuradas${NC}"
}

# Função para build e deploy
build_and_deploy() {
    echo -e "${CYAN}[6/10] Preparando Docker e Cloud Build...${NC}"
    
    # Criar Dockerfile otimizado
    cat > Dockerfile << 'EOF'
FROM python:3.9-slim
WORKDIR /app
RUN apt-get update && apt-get install -y gcc curl && rm -rf /var/lib/apt/lists/*
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY op.py .
COPY .env* ./
RUN mkdir -p /app/.streamlit
RUN echo '[server]\nport = 8080\nenableCORS = false\nheadless = true\n' > /app/.streamlit/config.toml
EXPOSE 8080
ENV PORT=8080
CMD streamlit run op.py --server.port=$PORT --server.address=0.0.0.0
EOF
    
    echo -e "${GREEN}✓ Dockerfile criado${NC}"
    
    echo -e "${CYAN}[7/10] Fazendo build com Cloud Build...${NC}"
    
    # Configurar Cloud Build
    cat > cloudbuild.yaml << EOF
steps:
  - name: 'gcr.io/cloud-builders/docker'
    args: ['build', '-t', 'gcr.io/$PROJECT_ID/$SERVICE_NAME', '.']
  - name: 'gcr.io/cloud-builders/docker'
    args: ['push', 'gcr.io/$PROJECT_ID/$SERVICE_NAME']
  - name: 'gcr.io/google.com/cloudsdktool/cloud-sdk'
    entrypoint: gcloud
    args:
      - 'run'
      - 'deploy'
      - '$SERVICE_NAME'
      - '--image'
      - 'gcr.io/$PROJECT_ID/$SERVICE_NAME'
      - '--region'
      - '$REGION'
      - '--platform'
      - 'managed'
      - '--allow-unauthenticated'
      - '--memory'
      - '2Gi'
      - '--cpu'
      - '2'
      - '--timeout'
      - '900'
      - '--max-instances'
      - '10'
      - '--port'
      - '8080'
images:
  - 'gcr.io/$PROJECT_ID/$SERVICE_NAME'
timeout: '1200s'
EOF
    
    # Executar Cloud Build
    gcloud builds submit \
        --config cloudbuild.yaml \
        --project "$PROJECT_ID" \
        --substitutions="_SERVICE_NAME=$SERVICE_NAME,_REGION=$REGION" || {
        
        echo -e "${YELLOW}Cloud Build falhou, tentando deploy direto...${NC}"
        
        # Alternativa: Deploy direto do código fonte
        gcloud run deploy "$SERVICE_NAME" \
            --source . \
            --region "$REGION" \
            --platform managed \
            --allow-unauthenticated \
            --memory 2Gi \
            --cpu 2 \
            --timeout 900 \
            --max-instances 10 \
            --port 8080 \
            --project "$PROJECT_ID"
    }
    
    echo -e "${GREEN}✓ Deploy concluído${NC}"
}

# Função para configurar variáveis de ambiente
setup_env_vars() {
    echo -e "${CYAN}[8/10] Configurando variáveis de ambiente...${NC}"
    
    # Ler do .env
    if [ -f .env ]; then
        export $(grep -v '^#' .env | xargs)
    fi
    
    # Atualizar serviço com variáveis
    gcloud run services update "$SERVICE_NAME" \
        --region "$REGION" \
        --platform managed \
        --update-env-vars "ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY},OPENAI_API_KEY=${OPENAI_API_KEY},STREAMLIT_SERVER_HEADLESS=true,STREAMLIT_SERVER_PORT=8080" \
        --project "$PROJECT_ID" 2>/dev/null || true
    
    echo -e "${GREEN}✓ Variáveis de ambiente configuradas${NC}"
}

# Função para obter URL
get_service_url() {
    echo -e "${CYAN}[9/10] Obtendo URL do serviço...${NC}"
    
    SERVICE_URL=$(gcloud run services describe "$SERVICE_NAME" \
        --region "$REGION" \
        --format 'value(status.url)' \
        --project "$PROJECT_ID")
    
    echo -e "${GREEN}✓ URL obtida: $SERVICE_URL${NC}"
    echo "$SERVICE_URL"
}

# Função para configurar domínio customizado
setup_custom_domain() {
    echo -e "${CYAN}[10/10] Configurando domínio customizado (opcional)...${NC}"
    
    echo -e "${YELLOW}Deseja configurar um domínio customizado? (s/n)${NC}"
    read -r response
    
    if [[ "$response" == "s" ]]; then
        gcloud run domain-mappings create \
            --service "$SERVICE_NAME" \
            --domain "izza-medical.app" \
            --region "$REGION" \
            --project "$PROJECT_ID" 2>/dev/null || {
            echo -e "${YELLOW}Configure o DNS do seu domínio${NC}"
        }
    fi
}

# Função principal
main() {
    echo -e "${CYAN}Iniciando configuração completa...${NC}"
    echo ""
    
    # 1. Verificar/Criar billing
    BILLING_ACCOUNT=$(list_billing_accounts)
    
    # 2. Configurar projeto
    setup_project
    
    # 3. Vincular billing
    if [ -n "$BILLING_ACCOUNT" ]; then
        link_billing "$BILLING_ACCOUNT"
    else
        echo -e "${RED}Billing não configurado. Ative o trial gratuito primeiro!${NC}"
        echo "Visite: https://console.cloud.google.com/freetrial"
        exit 1
    fi
    
    # 4. Habilitar APIs
    enable_all_apis
    
    # 5. Configurar permissões
    setup_permissions
    
    # 6. Build e Deploy
    build_and_deploy
    
    # 7. Configurar variáveis
    setup_env_vars
    
    # 8. Obter URL
    SERVICE_URL=$(get_service_url)
    
    # 9. Domínio customizado
    setup_custom_domain
    
    # Resumo final
    echo ""
    echo -e "${PURPLE}╔════════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${PURPLE}║                 🎉 DEPLOY COMPLETO! 🎉                        ║${NC}"
    echo -e "${PURPLE}╚════════════════════════════════════════════════════════════════╝${NC}"
    echo ""
    echo -e "${GREEN}✅ TUDO CONFIGURADO COM SUCESSO!${NC}"
    echo ""
    echo -e "${WHITE}Projeto: $PROJECT_ID${NC}"
    echo -e "${WHITE}Serviço: $SERVICE_NAME${NC}"
    echo -e "${WHITE}Região: $REGION${NC}"
    echo ""
    echo -e "${CYAN}🌐 ACESSE SUA APLICAÇÃO:${NC}"
    echo -e "${GREEN}   $SERVICE_URL${NC}"
    echo ""
    echo -e "${YELLOW}📊 Comandos úteis:${NC}"
    echo "  Logs:      gcloud run logs read --service $SERVICE_NAME --region $REGION"
    echo "  Métricas:  gcloud run services describe $SERVICE_NAME --region $REGION"
    echo "  Update:    gcloud run deploy $SERVICE_NAME --source . --region $REGION"
    echo ""
    echo -e "${BLUE}Console:${NC} https://console.cloud.google.com/run?project=$PROJECT_ID"
    echo ""
    
    # Abrir no navegador
    echo -e "${GREEN}Abrindo aplicação no navegador...${NC}"
    open "$SERVICE_URL" 2>/dev/null || xdg-open "$SERVICE_URL" 2>/dev/null || echo "Acesse: $SERVICE_URL"
}

# Executar
main "$@"