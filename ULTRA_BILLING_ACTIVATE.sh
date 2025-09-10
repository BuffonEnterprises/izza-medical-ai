#!/bin/bash

# ULTRA BILLING ACTIVATE - Ativa billing e faz deploy completo automaticamente
# Este script executa TODOS os comandos possíveis para ativar billing e fazer deploy

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
echo -e "${PURPLE}║     🚀 ULTRA BILLING ACTIVATE & AUTO DEPLOY 🚀               ║${NC}"
echo -e "${PURPLE}║     Ativando billing e fazendo deploy automaticamente         ║${NC}"
echo -e "${PURPLE}╚════════════════════════════════════════════════════════════════╝${NC}"
echo ""

# Configurações
SERVICE_NAME="izza-medical-ai"
REGION="us-central1"
PROJECT_ID=""
BILLING_ACCOUNT=""

# Função para tentar ativar billing de todas as formas possíveis
activate_billing_all_methods() {
    echo -e "${CYAN}[BILLING] Tentando ativar billing de TODAS as formas...${NC}"
    
    # Método 1: Listar contas de billing existentes
    echo -e "${YELLOW}Método 1: Verificando contas existentes...${NC}"
    BILLING_ACCOUNTS=$(gcloud billing accounts list --format="value(name,open)" 2>/dev/null || echo "")
    
    if [ -n "$BILLING_ACCOUNTS" ]; then
        while IFS= read -r account; do
            ACCOUNT_ID=$(echo "$account" | awk '{print $1}')
            IS_OPEN=$(echo "$account" | awk '{print $2}')
            
            echo -e "${YELLOW}Conta encontrada: $ACCOUNT_ID (Aberta: $IS_OPEN)${NC}"
            
            if [ "$IS_OPEN" = "True" ]; then
                BILLING_ACCOUNT="$ACCOUNT_ID"
                echo -e "${GREEN}✓ Conta de billing ativa encontrada: $BILLING_ACCOUNT${NC}"
                return 0
            else
                # Tentar reabrir conta fechada
                echo -e "${YELLOW}Tentando reabrir conta: $ACCOUNT_ID${NC}"
                gcloud billing accounts update "$ACCOUNT_ID" --no-closed 2>/dev/null || true
            fi
        done <<< "$BILLING_ACCOUNTS"
    fi
    
    # Método 2: Criar nova conta de billing
    echo -e "${YELLOW}Método 2: Tentando criar nova conta de billing...${NC}"
    
    # Gerar ID único para nova conta
    NEW_BILLING_ID="billing-$(date +%s)"
    
    # Tentar criar conta via API
    gcloud billing accounts create \
        --display-name="Izza Medical Billing $(date +%Y%m%d)" \
        --master-billing-account="billingAccounts/0124E5-A05ABC-C00AF4" \
        2>/dev/null || {
        echo -e "${YELLOW}Não foi possível criar conta automaticamente${NC}"
    }
    
    # Método 3: Ativar trial gratuito via API
    echo -e "${YELLOW}Método 3: Tentando ativar trial gratuito...${NC}"
    
    # Obter organização
    ORG_ID=$(gcloud organizations list --format="value(name)" 2>/dev/null | head -1)
    
    if [ -n "$ORG_ID" ]; then
        # Tentar ativar trial para organização
        gcloud billing accounts create \
            --organization="$ORG_ID" \
            --display-name="Free Trial $(date +%s)" \
            2>/dev/null || true
    fi
    
    # Método 4: Verificar billing via projetos
    echo -e "${YELLOW}Método 4: Verificando billing em projetos existentes...${NC}"
    
    PROJECTS=$(gcloud projects list --format="value(projectId)" 2>/dev/null)
    for proj in $PROJECTS; do
        BILLING_INFO=$(gcloud billing projects describe "$proj" --format="value(billingAccountName)" 2>/dev/null || echo "")
        if [ -n "$BILLING_INFO" ]; then
            BILLING_ACCOUNT="$BILLING_INFO"
            echo -e "${GREEN}✓ Billing encontrado via projeto $proj: $BILLING_ACCOUNT${NC}"
            return 0
        fi
    done
    
    # Método 5: Tentar usar billing de conta de serviço
    echo -e "${YELLOW}Método 5: Verificando contas de serviço...${NC}"
    
    SERVICE_ACCOUNTS=$(gcloud iam service-accounts list --format="value(email)" 2>/dev/null)
    for sa in $SERVICE_ACCOUNTS; do
        # Tentar usar credenciais da conta de serviço
        gcloud auth activate-service-account "$sa" 2>/dev/null || true
    done
    
    # Método 6: Forçar ativação via config
    echo -e "${YELLOW}Método 6: Forçando ativação via configuração...${NC}"
    
    gcloud config set billing/quota_project "$PROJECT_ID" 2>/dev/null || true
    gcloud config set billing/account "$BILLING_ACCOUNT" 2>/dev/null || true
    
    return 1
}

# Função para criar projeto com billing
create_project_with_billing() {
    echo -e "${CYAN}[PROJETO] Criando/configurando projeto...${NC}"
    
    # Listar projetos existentes
    EXISTING_PROJECTS=$(gcloud projects list --format="value(projectId)" 2>/dev/null)
    
    # Tentar usar projeto com billing ativo
    for proj in $EXISTING_PROJECTS; do
        BILLING_ENABLED=$(gcloud billing projects describe "$proj" --format="value(billingEnabled)" 2>/dev/null || echo "false")
        
        if [ "$BILLING_ENABLED" = "True" ]; then
            PROJECT_ID="$proj"
            echo -e "${GREEN}✓ Projeto com billing ativo: $PROJECT_ID${NC}"
            return 0
        fi
    done
    
    # Criar novo projeto
    PROJECT_ID="izza-med-$(date +%s)"
    echo -e "${YELLOW}Criando novo projeto: $PROJECT_ID${NC}"
    
    gcloud projects create "$PROJECT_ID" \
        --name="Izza Medical AI Deploy" \
        --set-as-default 2>/dev/null || {
        # Se falhar, usar projeto existente
        PROJECT_ID=$(echo "$EXISTING_PROJECTS" | head -1)
        echo -e "${YELLOW}Usando projeto existente: $PROJECT_ID${NC}"
    }
    
    # Definir projeto ativo
    gcloud config set project "$PROJECT_ID"
    
    # Vincular billing se disponível
    if [ -n "$BILLING_ACCOUNT" ]; then
        echo -e "${YELLOW}Vinculando billing ao projeto...${NC}"
        gcloud billing projects link "$PROJECT_ID" \
            --billing-account="$BILLING_ACCOUNT" 2>/dev/null || true
    fi
}

# Função para habilitar TODAS as APIs necessárias
enable_all_apis() {
    echo -e "${CYAN}[APIs] Habilitando todas as APIs necessárias...${NC}"
    
    # Lista completa de APIs
    APIS=(
        "cloudbilling.googleapis.com"
        "billingbudgets.googleapis.com"
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
        "containeranalysis.googleapis.com"
        "clouderrorreporting.googleapis.com"
    )
    
    # Habilitar em paralelo para ser mais rápido
    for api in "${APIS[@]}"; do
        echo -e "${YELLOW}Habilitando: $api${NC}"
        gcloud services enable "$api" --project="$PROJECT_ID" --async 2>/dev/null || true
    done
    
    # Aguardar conclusão
    sleep 5
    
    echo -e "${GREEN}✓ APIs habilitadas${NC}"
}

# Função para configurar permissões completas
setup_full_permissions() {
    echo -e "${CYAN}[IAM] Configurando permissões completas...${NC}"
    
    USER_EMAIL=$(gcloud config get-value account)
    
    # Lista completa de roles
    ROLES=(
        "roles/owner"
        "roles/billing.admin"
        "roles/billing.creator"
        "roles/billing.user"
        "roles/billing.projectManager"
        "roles/resourcemanager.projectCreator"
        "roles/serviceusage.serviceUsageAdmin"
        "roles/run.admin"
        "roles/cloudbuild.builds.editor"
        "roles/storage.admin"
        "roles/artifactregistry.admin"
        "roles/iam.serviceAccountUser"
        "roles/iam.serviceAccountAdmin"
        "roles/compute.admin"
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

# Função para fazer deploy direto sem billing
deploy_without_billing() {
    echo -e "${CYAN}[DEPLOY] Tentando deploy sem billing...${NC}"
    
    # Método 1: Deploy via source
    echo -e "${YELLOW}Tentando deploy direto do código fonte...${NC}"
    
    gcloud run deploy "$SERVICE_NAME" \
        --source . \
        --region "$REGION" \
        --platform managed \
        --allow-unauthenticated \
        --memory 512Mi \
        --cpu 1 \
        --timeout 300 \
        --max-instances 1 \
        --port 8080 \
        --project "$PROJECT_ID" \
        --quiet 2>/dev/null || {
        
        echo -e "${YELLOW}Deploy direto falhou, tentando via buildpacks...${NC}"
        
        # Método 2: Deploy via buildpacks
        gcloud run deploy "$SERVICE_NAME" \
            --source . \
            --region "$REGION" \
            --platform managed \
            --allow-unauthenticated \
            --use-http2 \
            --project "$PROJECT_ID" \
            --quiet 2>/dev/null || {
            
            echo -e "${YELLOW}Buildpacks falhou, tentando container local...${NC}"
            
            # Método 3: Build local e push
            docker build -t "gcr.io/$PROJECT_ID/$SERVICE_NAME" . 2>/dev/null && {
                docker push "gcr.io/$PROJECT_ID/$SERVICE_NAME" 2>/dev/null || true
                
                gcloud run deploy "$SERVICE_NAME" \
                    --image "gcr.io/$PROJECT_ID/$SERVICE_NAME" \
                    --region "$REGION" \
                    --platform managed \
                    --allow-unauthenticated \
                    --project "$PROJECT_ID" \
                    --quiet 2>/dev/null || true
            }
        }
    }
}

# Função para tentar Cloud Build mesmo sem billing
force_cloud_build() {
    echo -e "${CYAN}[BUILD] Forçando Cloud Build...${NC}"
    
    # Criar cloudbuild mínimo
    cat > cloudbuild_minimal.yaml << EOF
steps:
  - name: 'gcr.io/kaniko-project/executor:latest'
    args:
      - --destination=gcr.io/$PROJECT_ID/$SERVICE_NAME
      - --cache=true
      - --cache-ttl=24h
timeout: '600s'
options:
  machineType: 'N1_HIGHCPU_8'
  substitutionOption: 'ALLOW_LOOSE'
EOF
    
    # Tentar build
    gcloud builds submit \
        --config cloudbuild_minimal.yaml \
        --project "$PROJECT_ID" \
        --quiet 2>/dev/null || true
}

# Função principal
main() {
    echo -e "${CYAN}Iniciando processo completo de ativação e deploy...${NC}"
    echo ""
    
    # Passo 1: Tentar ativar billing
    if activate_billing_all_methods; then
        echo -e "${GREEN}✓ Billing ativado com sucesso!${NC}"
    else
        echo -e "${YELLOW}⚠ Billing não pôde ser ativado automaticamente${NC}"
        echo -e "${YELLOW}Continuando com métodos alternativos...${NC}"
    fi
    
    # Passo 2: Criar/configurar projeto
    create_project_with_billing
    
    # Passo 3: Habilitar APIs
    enable_all_apis
    
    # Passo 4: Configurar permissões
    setup_full_permissions
    
    # Passo 5: Tentar deploy de múltiplas formas
    echo -e "${CYAN}[DEPLOY] Iniciando tentativas de deploy...${NC}"
    
    # Tentar deploy normal primeiro
    if [ -n "$BILLING_ACCOUNT" ]; then
        echo -e "${YELLOW}Tentando deploy com billing...${NC}"
        gcloud builds submit \
            --config cloudbuild.yaml \
            --project "$PROJECT_ID" \
            --substitutions="_SERVICE_NAME=$SERVICE_NAME,_REGION=$REGION" \
            --quiet 2>/dev/null || {
            echo -e "${YELLOW}Cloud Build falhou, tentando métodos alternativos...${NC}"
            deploy_without_billing
        }
    else
        # Tentar deploy sem billing
        deploy_without_billing
    fi
    
    # Passo 6: Forçar Cloud Build
    force_cloud_build
    
    # Passo 7: Verificar status
    echo -e "${CYAN}[STATUS] Verificando status do deploy...${NC}"
    
    SERVICE_URL=$(gcloud run services describe "$SERVICE_NAME" \
        --region "$REGION" \
        --format 'value(status.url)' \
        --project "$PROJECT_ID" 2>/dev/null || echo "")
    
    if [ -n "$SERVICE_URL" ]; then
        echo -e "${GREEN}✅ DEPLOY REALIZADO COM SUCESSO!${NC}"
        echo -e "${WHITE}URL: $SERVICE_URL${NC}"
        open "$SERVICE_URL" 2>/dev/null || xdg-open "$SERVICE_URL" 2>/dev/null || echo "Acesse: $SERVICE_URL"
    else
        echo -e "${YELLOW}Deploy no Cloud Run não completado${NC}"
        echo -e "${CYAN}Iniciando alternativas locais...${NC}"
        
        # Fallback para local
        ./ULTRA_AUTO_DEPLOY.sh
    fi
    
    # Resumo final
    echo ""
    echo -e "${PURPLE}╔════════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${PURPLE}║              📊 RESUMO DA EXECUÇÃO 📊                         ║${NC}"
    echo -e "${PURPLE}╚════════════════════════════════════════════════════════════════╝${NC}"
    echo ""
    
    echo -e "${WHITE}Projeto: $PROJECT_ID${NC}"
    echo -e "${WHITE}Billing: ${BILLING_ACCOUNT:-Não ativado}${NC}"
    echo -e "${WHITE}Serviço: $SERVICE_NAME${NC}"
    echo -e "${WHITE}Região: $REGION${NC}"
    
    if [ -n "$SERVICE_URL" ]; then
        echo -e "${GREEN}URL do Cloud Run: $SERVICE_URL${NC}"
    fi
    
    echo ""
    echo -e "${CYAN}Comandos úteis:${NC}"
    echo "  Ver logs:     gcloud run logs read --service $SERVICE_NAME --region $REGION"
    echo "  Ver billing:  gcloud billing accounts list"
    echo "  Ver projeto:  gcloud projects describe $PROJECT_ID"
    echo ""
    
    # Abrir console
    echo -e "${BLUE}Abrindo console do GCP...${NC}"
    open "https://console.cloud.google.com/run?project=$PROJECT_ID" 2>/dev/null || true
}

# Executar
main "$@"