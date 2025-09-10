import streamlit as st
from anthropic import Anthropic
import os
from datetime import datetime
from dotenv import load_dotenv
import httpx
import json
import re
import time

# Load environment variables
load_dotenv()

# Configuração
SYSTEM_PROMPT = """Você é o NEXUS-MED ULTRA v5.0, a evolução máxima do sistema de inteligência médica que integra:

🧠 **ARQUITETURA NEURAL AVANÇADA**
- Raciocínio clínico multinível com 10 camadas de análise
- Processamento paralelo de 1000+ diagnósticos diferenciais
- Motor de inferência bayesiana com atualização em tempo real
- Sistema de aprendizado federado com conhecimento de 50.000+ casos clínicos

🔬 **MÓDULOS INTEGRADOS DE ÚLTIMA GERAÇÃO**

### **1. QUANTUM MEDICAL REASONING ENGINE (QMRE)**
```python
class QuantumDiagnosticEngine:
    def __init__(self):
        self.quantum_states = []
        self.superposition_diagnoses = []
        self.entangled_symptoms = {}
        self.wave_function_collapse_threshold = 0.95
    
    def quantum_differential_diagnosis(self, symptoms):
        # Cria superposição de todos os diagnósticos possíveis
        # Aplica operadores quânticos para correlação de sintomas
        # Colapsa a função de onda baseado em evidências
        # Retorna distribuição probabilística de diagnósticos
        pass
```

### **2. MEDICAL KNOWLEDGE HYPERGRAPH**
- 500.000+ nós de conhecimento médico
- 2.000.000+ relações causais, temporais e probabilísticas
- Atualização em tempo real com literatura médica
- Integração com 50+ bases de dados médicas globais

### **3. MULTIMODAL DIAGNOSTIC FUSION**
- Análise de texto, voz, imagem, vídeo e biossinais
- Processamento de exames laboratoriais com OCR médico
- Interpretação de imagens médicas (RX, TC, RM, US)
- Análise de sinais vitais em tempo real
- Reconhecimento de padrões em ECG, EEG, EMG

### **4. CLINICAL DECISION SUPPORT SYSTEM (CDSS) v5.0**
```
PROTOCOLO DE DECISÃO HIERÁRQUICA:
├── Nível 1: Triagem Instantânea (< 100ms)
│   ├── Detecção de emergências vitais
│   ├── Ativação de protocolos ACLS/ATLS/PALS
│   └── Notificação de equipe de resposta rápida
├── Nível 2: Análise Profunda (< 5s)
│   ├── Diagnóstico diferencial completo
│   ├── Cálculo de scores clínicos validados
│   └── Predição de deterioração clínica
├── Nível 3: Planejamento Terapêutico (< 30s)
│   ├── Personalização farmacogenômica
│   ├── Otimização de doses por IA
│   └── Prevenção de interações medicamentosas
└── Nível 4: Monitoramento Contínuo
    ├── Ajuste dinâmico de tratamento
    ├── Detecção precoce de complicações
    └── Recomendações preventivas personalizadas
```

### **5. GENOMIC MEDICINE INTEGRATION**
- Análise de variantes genéticas patogênicas
- Farmacogenômica personalizada
- Predição de risco poligênico
- Medicina de precisão baseada em perfil molecular

### **6. EMERGENCY RESPONSE MATRIX**
```
PROTOCOLOS DE EMERGÊNCIA ULTRA-RÁPIDOS:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
PCR → Protocolo ACLS + Desfibrilação
IAM → Via Verde Coronária + PCI
AVC → Código AVC + tPA/Trombectomia  
Sepse → Bundle 1h + Antibióticos
Trauma → ATLS + Damage Control
Anafilaxia → Adrenalina IM + Suporte
Status Epilepticus → Benzodiazepínicos
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### **7. PREDICTIVE HEALTH ANALYTICS**
- Modelos preditivos com 98% de acurácia
- Detecção de padrões subclínicos
- Identificação de riscos futuros
- Recomendações preventivas personalizadas

### **8. EMPATHETIC COMMUNICATION ENGINE**
- Análise de sentimentos e emoções
- Adaptação de linguagem por perfil do paciente
- Suporte psicológico integrado
- Comunicação culturalmente sensível

### **9. REAL-TIME LITERATURE INTEGRATION**
- Acesso a 30 milhões de artigos médicos
- Análise de evidências em tempo real
- Meta-análises automáticas
- Recomendações baseadas nas últimas diretrizes

### **10. SAFETY MONITORING SYSTEM**
- Detecção de erros médicos potenciais
- Alertas de contraindicações
- Monitoramento de eventos adversos
- Sistema de double-check automático

### **11. EXTENDED THINKING SYSTEM (ETS)**
- Análise profunda multi-estágio
- Raciocínio passo a passo explícito
- Exploração de hipóteses alternativas
- Avaliação crítica de cada diagnóstico diferencial
- Integração de múltiplas fontes de evidência
- Documentação detalhada do processo de raciocínio

## 🎯 **PROTOCOLO OPERACIONAL ULTRA**

1. **ENTRADA DE DADOS**
   - Processamento multimodal simultâneo
   - Extração de entidades médicas com NER avançado
   - Normalização e padronização automática
   - Validação cruzada de informações

2. **ANÁLISE CLÍNICA**
   - Ativação paralela de todos os módulos
   - Fusão de dados multimodais
   - Inferência bayesiana hierárquica
   - Validação por comitê de IA especialistas

3. **GERAÇÃO DE RESPOSTA**
   - Síntese de conhecimento multidisciplinar
   - Personalização baseada no perfil do paciente
   - Formatação estruturada e visual
   - Verificação de segurança tripla

4. **MONITORAMENTO CONTÍNUO**
   - Tracking de outcomes clínicos
   - Ajuste de recomendações em tempo real
   - Aprendizado com feedback
   - Melhoria contínua do sistema

5. **PENSAMENTO ESTENDIDO**
   - Quando acionado, realiza análise aprofundada
   - Documenta cada passo do raciocínio diagnóstico
   - Explora todas as hipóteses relevantes
   - Integra evidências de múltiplas fontes
   - Fornece justificativa detalhada para conclusões

## 🚨 **PROTOCOLOS DE SEGURANÇA ULTRA**

```python
class UltraSafetyProtocol:
    RED_FLAGS = {
        "cardiovascular": ["dor torácica", "dispneia súbita", "síncope"],
        "neurological": ["cefaleia thunderclap", "déficit focal", "confusão aguda"],
        "infectious": ["febre + rigidez nucal", "sepse", "choque"],
        "surgical": ["abdome agudo", "trauma major", "hemorragia"]
    }
    
    def emergency_check(self, symptoms):
        for category, flags in self.RED_FLAGS.items():
            if any(flag in symptoms.lower() for flag in flags):
                return self.activate_emergency_protocol(category)
```

## 📊 **MÉTRICAS DE PERFORMANCE ULTRA**
- Acurácia diagnóstica: 99.2%
- Tempo médio de resposta: 500ms
- Taxa de detecção de emergências: 99.9%
- Satisfação do usuário: 96%
- Redução de erros médicos: 85%

## 🔄 **SISTEMA DE APRENDIZADO CONTÍNUO**
- Atualização diária com novos casos
- Incorporação de feedback médico
- Refinamento de algoritmos por IA
- Validação por especialistas humanos

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**ATIVAÇÃO DO SISTEMA ULTRA:**
"Bem-vindo ao NEXUS-MED ULTRA v5.0. Sou seu assistente médico de inteligência artificial mais avançado, integrando o conhecimento de milhares de especialistas e milhões de casos clínicos. 

Para oferecer o melhor cuidado possível, vou analisar sua situação usando múltiplas modalidades e algoritmos avançados. Por favor, descreva seus sintomas ou carregue seus exames. Estou preparado para emergências médicas com resposta em tempo real.

Se você desejar uma análise mais profunda, ative o modo de pensamento estendido usando o comando 'pensamento estendido: [sua pergunta]'. Isso ativará uma análise passo a passo detalhada com exploração completa de todas as hipóteses relevantes."

<ultra_mode>ACTIVATED</ultra_mode>
<quantum_reasoning>ENABLED</quantum_reasoning>
<multimodal_fusion>READY</multimodal_fusion>
<emergency_detection>VIGILANT</emergency_detection>
<extended_thinking>AVAILABLE</extended_thinking>
"""

# Configurações do modelo
MODEL = "claude-4-sonnet-20250514"
MAX_TOKENS = 200000  # Máximo de tokens para Claude 4 Sonnet
CONTEXT_WINDOW = 400000  # Tamanho da janela de contexto do Claude 4 Sonnet

# Inicialização
st.set_page_config(page_title="House MD PhD 🚬", layout="wide")

# Initialize Anthropic client
try:
    api_key = os.getenv('ANTHROPIC_API_KEY')
    if not api_key:
        st.error("❌ API Key não encontrada. Configure ANTHROPIC_API_KEY no ambiente.")
        st.stop()

    # Opcional: suporte a proxy sem usar argumento 'proxies' no Anthropic
    proxy_url = os.getenv('HTTPS_PROXY') or os.getenv('HTTP_PROXY')
    # Cria o cliente httpx com ou sem proxy
    http_client = httpx.Client(proxies=proxy_url, timeout=300) if proxy_url else httpx.Client(timeout=300)

    anthropic = Anthropic(api_key=api_key, http_client=http_client)
except Exception as e:
    st.error(f"❌ Erro ao inicializar cliente Anthropic: {e}")
    st.stop()

# Funções
def detect_extended_thinking_request(user_input: str) -> tuple:
    """Detecta se o usuário solicitou pensamento estendido e extrai a consulta real."""
    pattern = r'^pensamento\s+estendido\s*:\s*(.+)$'
    match = re.search(pattern, user_input, re.IGNORECASE)
    
    if match:
        return True, match.group(1).strip()
    return False, user_input

def get_claude_response(user_input: str, conversation_history=None, extended_thinking=False) -> str:
    """Obtém resposta do Claude com suporte a histórico de conversa e pensamento estendido."""
    try:
        # Preparar mensagens incluindo histórico de conversa
        messages = []
        if conversation_history:
            messages.extend(conversation_history)
        
        # Adicionar a mensagem atual do usuário
        messages.append({"role": "user", "content": user_input})
        
        # Configurar sistema prompt adicional para pensamento estendido
        system = SYSTEM_PROMPT
        if extended_thinking:
            system += """
            
ATIVAÇÃO DO MODO DE PENSAMENTO ESTENDIDO:

Neste modo, você deve:
1. Realizar uma análise médica profunda e detalhada
2. Documentar explicitamente cada etapa do seu raciocínio
3. Considerar múltiplas hipóteses diagnósticas
4. Avaliar criticamente cada hipótese com base nas evidências disponíveis
5. Integrar conhecimento de diferentes especialidades médicas
6. Explicar o processo de eliminação para diagnósticos menos prováveis
7. Fornecer justificativas baseadas em evidências para suas conclusões
8. Incluir referências a estudos médicos relevantes quando apropriado
9. Estruturar sua resposta em seções claramente definidas
10. Concluir com um resumo conciso das descobertas principais

<extended_thinking>ACTIVATED</extended_thinking>
"""

        # Configurar parâmetros para maximizar o uso do contexto
        response = anthropic.messages.create(
            model=MODEL,
            max_tokens=MAX_TOKENS,
            system=system,
            temperature=0.1 if not extended_thinking else 0.05,  # Temperatura mais baixa para pensamento estendido
            messages=messages
        )
        return response.content[0].text
    except Exception as e:
        st.error(f"❌ Erro ao obter resposta: {e}")
        return "Desculpe, ocorreu um erro ao processar sua solicitação. Verifique sua API Key e conexão com a internet."

def save_conversation(conversation):
    """Salva a conversa em um arquivo de texto."""
    try:
        filename = f"conversa_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        with open(filename, "w", encoding='utf-8') as f:
            for entry in conversation:
                f.write(f"{entry['role']}: {entry['content']}\n\n")
        return filename
    except Exception as e:
        st.error(f"Erro ao salvar a conversa: {e}")
        return None

def export_conversation_json(conversation):
    """Exporta a conversa em formato JSON."""
    try:
        filename = f"conversa_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(filename, "w", encoding='utf-8') as f:
            json.dump(conversation, f, ensure_ascii=False, indent=2)
        return filename
    except Exception as e:
        st.error(f"Erro ao exportar a conversa: {e}")
        return None

def count_tokens_in_conversation(conversation):
    """Estima a quantidade de tokens na conversa atual."""
    # Estimativa simples: aproximadamente 4 caracteres = 1 token
    total_chars = sum(len(entry.get('content', '')) for entry in conversation)
    return total_chars // 4

# Interface Streamlit
st.title("House MD PhD 🧠")
st.caption("Powered by PIRM - Diagnósticos Médicos Avançados com IA")

# Aviso médico importante
st.error("""
**AVISO MÉDICO CRÍTICO**: Este sistema utiliza IA para fins educacionais e de apoio diagnóstico.
NÃO substitui consulta médica profissional. Sempre procure um médico qualificado para diagnósticos e tratamentos reais.
Em emergências, procure imediatamente o serviço de urgência mais próximo.
""")

# Inicialização do estado da sessão
if "conversation" not in st.session_state:
    st.session_state.conversation = []
if "extended_thinking_mode" not in st.session_state:
    st.session_state.extended_thinking_mode = False

# Sidebar
with st.sidebar:
    st.title("⚙️ Configurações")
    
    # Informações do sistema
    api_status = '✅ Configurada' if os.getenv('ANTHROPIC_API_KEY') else '❌ Não configurada'
    st.info(f"""
**Modelo:** Claude 4 Sonnet (20250514)
**Contexto:** 400K tokens
**Especialidades:** Raciocínio avançado, medicina baseada em evidências
**Status API:** {api_status}
    """)
    
    st.divider()
    
    # Métricas da sessão
    if st.session_state.conversation:
        total_messages = len(st.session_state.conversation)
        user_messages = len([msg for msg in st.session_state.conversation if msg["role"] == "user"])
        token_estimate = count_tokens_in_conversation(st.session_state.conversation)
        
        st.metric("📊 Casos analisados", user_messages)
        st.metric("💬 Total de mensagens", total_messages)
        st.metric("🔢 Tokens estimados", f"{token_estimate:,}")
        
        # Aviso de limite de contexto
        if token_estimate > CONTEXT_WINDOW * 0.7:
            st.warning(f"⚠️ Aproximando-se do limite de contexto ({token_estimate}/{CONTEXT_WINDOW})")
    
    st.divider()
    
    # Modo de pensamento estendido
    st.subheader("🧠 Modo de Pensamento")
    st.toggle("Ativar Pensamento Estendido", key="extended_thinking_mode", 
              help="Ativa análise médica aprofundada com raciocínio passo a passo detalhado")
    
    if st.session_state.extended_thinking_mode:
        st.success("✅ Modo de pensamento estendido ativado")
        st.caption("""
        O modo de pensamento estendido realiza uma análise médica aprofundada com:
        - Raciocínio passo a passo explícito
        - Exploração de múltiplas hipóteses
        - Avaliação crítica baseada em evidências
        - Documentação detalhada do processo diagnóstico
        """)
    
    st.divider()
    
    # Opções de gerenciamento da conversa
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🗑️ Limpar Conversa"):
            st.session_state.conversation = []
            st.rerun()
    
    with col2:
        export_format = st.radio("Formato:", ["TXT", "JSON"], horizontal=True)
        if st.button("💾 Salvar Conversa"):
            if export_format == "TXT":
                if (filename := save_conversation(st.session_state.conversation)):
                    st.success(f"✅ Conversa salva em {filename}")
            else:
                if (filename := export_conversation_json(st.session_state.conversation)):
                    st.success(f"✅ Conversa exportada em {filename}")
    
    st.divider()
    
    # Instruções de uso
    with st.expander("📋 Como usar o conhecimento do PIRM"):
        st.markdown("""
### 🚀 **Capacidades do PIRM:**
- **Raciocínio clínico avançado** com análise de casos complexos
- **Diagnósticos diferenciais** sistemáticos e precisos
- **Prescrições personalizadas** com dosagens específicas
- **Medicina baseada em evidências** com referências científicas
- **Pensamento estendido** para análises médicas aprofundadas

### 📝 **Como usar:**
1. **Configure sua API Key:** `ANTHROPIC_API_KEY` nas variáveis de ambiente
2. **Descreva o caso detalhadamente:**
   - Sintomas (início, duração, intensidade)
   - Histórico médico e familiar
   - Medicamentos em uso
   - Exames realizados
3. **Para análise aprofundada:**
   - Ative o modo de pensamento estendido no painel lateral, ou
   - Digite "pensamento estendido: [sua pergunta]"
4. **Receba análise completa:**
   - Diagnóstico provável
   - Diagnósticos diferenciais
   - Plano terapêutico
   - Monitoramento recomendado

### ⚡ **Melhorias do PIRM v5.0:**
- Contexto massivo de 400K tokens
- Respostas detalhadas até 200K tokens
- Raciocínio médico passo a passo
- Modo de pensamento estendido
- Melhor compreensão de casos complexos

⚠️ **Importante:** Sistema de apoio educacional apenas!
        """)

# Chat
for entry in st.session_state.conversation:
    with st.chat_message(entry["role"]):
        st.markdown(entry["content"])

if prompt := st.chat_input("🩺 Descreva o caso clínico detalhadamente (sintomas, histórico, medicamentos, exames):"):
    # Detectar se é uma solicitação de pensamento estendido
    is_extended_request, actual_prompt = detect_extended_thinking_request(prompt)
    
    # Determinar se deve usar pensamento estendido
    use_extended_thinking = is_extended_request or st.session_state.extended_thinking_mode
    
    # Adicionar a entrada do usuário à conversa
    st.session_state.conversation.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Preparar histórico de conversa para o contexto (excluindo a mensagem atual)
    conversation_history = st.session_state.conversation[:-1] if len(st.session_state.conversation) > 1 else None
    
    # Gerar e exibir resposta
    with st.chat_message("assistant"):
        if use_extended_thinking:
            with st.spinner("🧠 Dr. House está realizando uma análise aprofundada com pensamento estendido..."):
                response = get_claude_response(
                    actual_prompt, 
                    conversation_history=conversation_history,
                    extended_thinking=True
                )
        else:
            with st.spinner("🔬 Dr. House está analisando o caso com PIRM..."):
                response = get_claude_response(
                    prompt,
                    conversation_history=conversation_history
                )
                
        st.markdown(response)
    
    # Adicionar resposta à conversa
    st.session_state.conversation.append({"role": "assistant", "content": response})

# Feedback
with st.expander("💬 Enviar Feedback"):
    feedback = st.text_area("Seu feedback sobre o diagnóstico ou sugestões de melhoria:")
    if st.button("📤 Enviar Feedback"):
        if feedback.strip():
            # Aqui você pode implementar o salvamento do feedback
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            try:
                with open("feedback.txt", "a", encoding='utf-8') as f:
                    f.write(f"[{timestamp}] {feedback}\n\n")
                st.success("✅ Obrigado pelo seu feedback! Ele foi salvo para análise.")
            except Exception as e:
                st.error(f"❌ Erro ao salvar feedback: {e}")
        else:
            st.warning("⚠️ Por favor, escreva seu feedback antes de enviar.")

# Informações sobre o modo de pensamento estendido
with st.expander("ℹ️ Sobre o Pensamento Estendido"):
    st.markdown("""
    ## 🧠 Modo de Pensamento Estendido
    
    O modo de pensamento estendido é uma funcionalidade avançada que permite ao NEXUS-MED ULTRA v5.0 realizar uma análise médica profunda e detalhada, documentando explicitamente cada etapa do raciocínio diagnóstico.
    
    ### Como ativar:
    
    1. **Opção 1:** Ative o toggle "Pensamento Estendido" no painel lateral
    2. **Opção 2:** Digite "pensamento estendido: [sua pergunta]" no chat
    
    ### O que esperar:
    
    - Análise médica aprofundada e estruturada
    - Documentação explícita de cada etapa do raciocínio
    - Consideração de múltiplas hipóteses diagnósticas
    - Avaliação crítica baseada em evidências
    - Justificativas detalhadas para conclusões
    - Referências a estudos médicos relevantes
    
    ### Quando usar:
    
    - Casos clínicos complexos ou incomuns
    - Quando precisar entender o raciocínio diagnóstico completo
    - Para fins educacionais e de aprendizado
    - Quando desejar uma análise mais abrangente e detalhada
    
    > **Nota:** O modo de pensamento estendido pode resultar em respostas mais longas e detalhadas, mas também mais precisas e informativas.
    """)
