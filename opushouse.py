import streamlit as st
from anthropic import Anthropic
import os
from datetime import datetime
from dotenv import load_dotenv
import httpx
import json
from typing import Optional, List, Dict, Any
import re
import time
import base64
from PIL import Image
import PyPDF2
import io
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak, Image as RLImage
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT, TA_RIGHT
from reportlab.pdfgen import canvas
from reportlab.platypus.flowables import HRFlowable
import textwrap

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
MODEL = "claude-opus-4-1-20250805"

# Persistência de notas: caminho gravável no Cloud Run/App Engine
NOTES_FILE_PATH = os.getenv("NOTES_FILE_PATH", "/tmp/notes.json")

# Inicialização
st.set_page_config(page_title="Izza MD PhD", layout="wide")

# Ultra-Modern Medical Theme with Advanced Design Elements
st.markdown("""
<style>
    /* Import Premium Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=JetBrains+Mono:wght@400;500;600;700&family=Poppins:wght@300;400;500;600;700;800&display=swap');
    
    /* Root Variables - Enhanced Chalk Red Color System */
    :root {
        /* Primary Chalk Red Palette */
        --chalk-red: #E74C3C;
        --chalk-red-light: #EC7063;
        --chalk-red-soft: #F1948A;
        --chalk-red-pale: #FADBD8;
        --chalk-red-muted: #D98880;
        
        /* Deep Red Variations */
        --crimson: #DC143C;
        --scarlet: #FF2400;
        --vermillion: #E34234;
        --carmine: #960018;
        --burgundy: #800020;
        --wine: #722F37;
        --maroon: #85144B;
        
        /* Gradient Red Tones */
        --coral-red: #FF6B6B;
        --rose-red: #FF4757;
        --cherry-red: #CB2D3E;
        --ruby-red: #E0115F;
        --blood-red: #8B0000;
        
        /* Chalk Texture Colors */
        --chalk-white: #FAFAFA;
        --chalk-overlay: rgba(255, 255, 255, 0.15);
        --chalk-dust: rgba(231, 76, 60, 0.08);
        --chalk-stroke: rgba(231, 76, 60, 0.25);
        
        /* Primary System Colors */
        --primary-red: #E74C3C;
        --dark-red: #C0392B;
        --light-red: #EC7063;
        --accent-red: #E84342;
        --neon-red: #FF3838;
        
        /* Complex Gradients */
        --gradient-chalk: linear-gradient(135deg, #E74C3C, #EC7063, #F1948A);
        --gradient-fire: linear-gradient(135deg, #FF2400, #E74C3C, #DC143C);
        --gradient-wine: linear-gradient(180deg, #722F37, #800020, #960018);
        --gradient-sunset: linear-gradient(90deg, #FF6B6B, #FF4757, #E84342);
        --gradient-blood: linear-gradient(135deg, #8B0000, #DC143C, #E74C3C);
        
        /* Gradient Points */
        --gradient-start: #E74C3C;
        --gradient-mid: #EC7063;
        --gradient-end: #C0392B;
        
        /* Background Colors */
        --bg-dark: #0A0A0C;
        --bg-secondary: #141418;
        --bg-tertiary: #1C1C22;
        --bg-chalk: #1A1114;
        
        /* Text Colors */
        --text-primary: #FFFFFF;
        --text-secondary: #B8B8C0;
        --text-accent: #EC7063;
        --text-chalk: #F5E6E8;
        
        /* Border & Effects */
        --border-color: rgba(231, 76, 60, 0.15);
        --border-hover: rgba(231, 76, 60, 0.4);
        --border-chalk: rgba(236, 112, 99, 0.2);
        
        /* Card Colors */
        --card-bg: rgba(20, 20, 24, 0.85);
        --card-hover: rgba(20, 20, 24, 0.95);
        --card-chalk: rgba(231, 76, 60, 0.03);
        
        /* Glass Effects */
        --glass-bg: rgba(255, 255, 255, 0.02);
        --glass-border: rgba(255, 255, 255, 0.08);
        --glass-red: rgba(231, 76, 60, 0.05);
        
        /* Shadows & Glows */
        --hover-glow: rgba(231, 76, 60, 0.5);
        --shadow-sm: 0 2px 8px rgba(0, 0, 0, 0.3);
        --shadow-md: 0 4px 20px rgba(0, 0, 0, 0.4);
        --shadow-lg: 0 8px 40px rgba(0, 0, 0, 0.5);
        --shadow-glow: 0 0 40px rgba(231, 76, 60, 0.3);
        --shadow-chalk: 0 4px 16px rgba(231, 76, 60, 0.15);
        
        /* Transitions */
        --transition-fast: 0.2s cubic-bezier(0.4, 0, 0.2, 1);
        --transition-smooth: 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        --transition-bounce: 0.6s cubic-bezier(0.68, -0.55, 0.265, 1.55);
    }
    
    /* Animated Gradient Background */
    @keyframes gradientShift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    @keyframes floatingParticles {
        0% { transform: translateY(100vh) rotate(0deg); opacity: 0; }
        10% { opacity: 1; }
        90% { opacity: 1; }
        100% { transform: translateY(-10vh) rotate(720deg); opacity: 0; }
    }
    
    /* Main App Background with Chalk Red Gradient */
    .stApp {
        background: 
            radial-gradient(ellipse at top left, var(--chalk-dust) 0%, transparent 40%),
            radial-gradient(ellipse at bottom right, rgba(192, 57, 43, 0.05) 0%, transparent 40%),
            linear-gradient(-45deg, #0A0A0C, var(--bg-chalk), #0F0515, var(--bg-chalk));
        background-size: 400% 400%;
        animation: gradientShift 20s ease infinite;
        color: var(--text-primary);
        font-family: 'Poppins', 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        position: relative;
        overflow-x: hidden;
    }
    
    /* Chalk Texture Overlay */
    .stApp::before {
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: 
            repeating-linear-gradient(
                45deg,
                transparent,
                transparent 10px,
                var(--chalk-dust) 10px,
                var(--chalk-dust) 11px
            ),
            repeating-linear-gradient(
                -45deg,
                transparent,
                transparent 10px,
                rgba(231, 76, 60, 0.02) 10px,
                rgba(231, 76, 60, 0.02) 11px
            );
        opacity: 0.3;
        pointer-events: none;
        mix-blend-mode: overlay;
    }
    
    /* Floating Chalk Particles */
    .stApp::after {
        content: '';
        position: fixed;
        width: 100%;
        height: 100%;
        top: 0;
        left: 0;
        background-image: 
            radial-gradient(circle at 20% 80%, var(--chalk-red-soft) 0%, transparent 2%),
            radial-gradient(circle at 80% 20%, var(--coral-red) 0%, transparent 2%),
            radial-gradient(circle at 40% 40%, var(--rose-red) 0%, transparent 2%),
            radial-gradient(circle at 60% 60%, var(--chalk-red-light) 0%, transparent 2%),
            radial-gradient(circle at 30% 30%, var(--crimson) 0%, transparent 2%);
        pointer-events: none;
        animation: floatingParticles 25s linear infinite;
        filter: blur(1px);
        opacity: 0.4;
    }
    
    /* Chalk Red Sidebar with Fine Gradients */
    .css-1d391kg, [data-testid="stSidebar"] {
        background: 
            linear-gradient(180deg, 
                var(--chalk-dust) 0%, 
                rgba(20, 20, 24, 0.95) 20%,
                var(--bg-chalk) 60%,
                rgba(10, 10, 12, 0.98) 100%),
            repeating-linear-gradient(
                90deg,
                transparent,
                transparent 100px,
                var(--chalk-dust) 100px,
                var(--chalk-dust) 101px
            );
        backdrop-filter: blur(20px) saturate(150%);
        -webkit-backdrop-filter: blur(20px) saturate(150%);
        border-right: 2px solid var(--border-chalk);
        border-radius: 0 30px 30px 0;
        box-shadow: 
            inset 0 0 40px var(--chalk-dust),
            4px 0 24px rgba(0, 0, 0, 0.4),
            inset -1px 0 0 var(--chalk-red-light);
        position: relative;
        overflow: hidden;
    }
    
    /* Chalk Red Sidebar Glow Line */
    .css-1d391kg::before, [data-testid="stSidebar"]::before {
        content: '';
        position: absolute;
        top: 0;
        right: 0;
        width: 3px;
        height: 100%;
        background: linear-gradient(180deg, 
            transparent 0%, 
            var(--chalk-red) 20%,
            var(--crimson) 50%, 
            var(--chalk-red-light) 80%,
            transparent 100%);
        animation: chalkScan 4s ease-in-out infinite;
        filter: blur(1px);
        box-shadow: 
            0 0 10px var(--chalk-red),
            0 0 20px var(--chalk-red-light);
    }
    
    @keyframes chalkScan {
        0%, 100% { 
            transform: translateY(-100%);
            opacity: 0.6;
        }
        50% { 
            transform: translateY(100%);
            opacity: 1;
        }
    }
    
    @keyframes scanLine {
        0%, 100% { transform: translateY(-100%); }
        50% { transform: translateY(100%); }
    }
    
    .css-1d391kg .stTextInput > div > div, 
    [data-testid="stSidebar"] .stTextInput > div > div {
        background: rgba(255, 46, 46, 0.05);
        border: 1px solid var(--border-color);
        border-radius: 20px;
        transition: all 0.3s ease;
    }
    
    .css-1d391kg .stTextInput > div > div:focus-within,
    [data-testid="stSidebar"] .stTextInput > div > div:focus-within {
        border-color: var(--primary-red);
        box-shadow: 0 0 20px rgba(255, 46, 46, 0.3);
    }
    
    /* Chalk-Style Headers with Red Tones */
    h1 {
        background: var(--gradient-chalk);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-weight: 800;
        font-size: 2.5rem;
        letter-spacing: -0.03em;
        position: relative;
        text-shadow: 
            0 0 20px var(--chalk-red-light),
            0 0 40px rgba(231, 76, 60, 0.4),
            0 0 60px rgba(236, 112, 99, 0.2);
        animation: chalkGlow 3s ease-in-out infinite;
        filter: contrast(1.2) brightness(1.1);
    }
    
    h2, h3 {
        background: linear-gradient(90deg, var(--chalk-red), var(--chalk-red-light), var(--chalk-red-soft));
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-weight: 600;
        letter-spacing: -0.01em;
        text-shadow: 0 2px 10px var(--chalk-dust);
    }
    
    @keyframes chalkGlow {
        0%, 100% { 
            filter: brightness(1) contrast(1.2) drop-shadow(0 0 20px var(--chalk-red-light));
            text-shadow: 
                0 0 20px var(--chalk-red-light),
                0 0 40px rgba(231, 76, 60, 0.4);
        }
        50% { 
            filter: brightness(1.15) contrast(1.3) drop-shadow(0 0 30px var(--chalk-red));
            text-shadow: 
                0 0 30px var(--chalk-red),
                0 0 50px rgba(231, 76, 60, 0.6),
                0 0 70px rgba(236, 112, 99, 0.3);
        }
    }
    
    /* Chalk Red Buttons with Fine Gradients */
    .stButton > button {
        background: var(--gradient-fire);
        color: var(--chalk-white);
        border: 1px solid var(--chalk-stroke);
        border-radius: 30px;
        padding: 14px 36px;
        font-weight: 600;
        font-size: 14px;
        letter-spacing: 0.8px;
        text-transform: uppercase;
        position: relative;
        overflow: hidden;
        transition: var(--transition-smooth);
        box-shadow: 
            0 4px 15px var(--shadow-chalk),
            inset 0 1px 0 var(--chalk-overlay),
            inset 0 -2px 0 rgba(192, 57, 43, 0.3),
            0 0 30px rgba(231, 76, 60, 0.2);
        transform-style: preserve-3d;
        perspective: 1000px;
        text-shadow: 0 1px 2px rgba(0, 0, 0, 0.3);
    }
    
    /* Chalk Texture on Button */
    .stButton > button::after {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: 
            repeating-linear-gradient(
                90deg,
                transparent,
                transparent 2px,
                var(--chalk-overlay) 2px,
                var(--chalk-overlay) 3px
            );
        opacity: 0.3;
        pointer-events: none;
    }
    
    .stButton > button::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, 
            transparent, 
            rgba(255, 255, 255, 0.3), 
            transparent);
        transition: left 0.5s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-3px) rotateX(-10deg);
        box-shadow: 
            0 10px 30px var(--shadow-chalk),
            inset 0 1px 0 var(--chalk-overlay),
            0 0 50px rgba(231, 76, 60, 0.4),
            0 0 80px rgba(236, 112, 99, 0.2);
        background: var(--gradient-sunset);
        filter: brightness(1.1) saturate(1.2);
    }
    
    .stButton > button:hover::before {
        left: 100%;
    }
    
    .stButton > button:active {
        transform: translateY(-1px) rotateX(-5deg);
        box-shadow: 
            0 2px 10px rgba(255, 46, 46, 0.4),
            inset 0 2px 4px rgba(0, 0, 0, 0.3);
    }
    
    /* Chalk-Style Input Fields */
    .stTextInput > div > div, .stTextArea > div > div > textarea {
        background: linear-gradient(135deg, 
            rgba(20, 20, 24, 0.6), 
            var(--card-chalk));
        backdrop-filter: blur(10px) saturate(120%);
        -webkit-backdrop-filter: blur(10px) saturate(120%);
        border: 1px solid var(--border-chalk);
        color: var(--text-primary);
        border-radius: 25px;
        padding: 16px 24px;
        font-size: 15px;
        font-weight: 500;
        transition: var(--transition-smooth);
        box-shadow: 
            inset 0 2px 4px rgba(0, 0, 0, 0.3),
            0 4px 12px rgba(0, 0, 0, 0.2),
            0 0 20px var(--chalk-dust);
        position: relative;
    }
    
    /* Chalk Border Effect */
    .stTextInput > div > div::before, 
    .stTextArea > div > div > textarea::before {
        content: '';
        position: absolute;
        top: -1px;
        left: -1px;
        right: -1px;
        bottom: -1px;
        background: var(--gradient-chalk);
        border-radius: 25px;
        opacity: 0;
        z-index: -1;
        transition: opacity var(--transition-smooth);
    }
    
    .stTextInput > div > div:focus, .stTextArea > div > div > textarea:focus {
        border-color: var(--chalk-red);
        background: linear-gradient(135deg, 
            rgba(20, 20, 24, 0.8), 
            var(--glass-red));
        box-shadow: 
            0 0 0 3px var(--chalk-stroke),
            0 0 40px var(--chalk-red-light),
            0 0 60px rgba(236, 112, 99, 0.2),
            inset 0 2px 4px rgba(0, 0, 0, 0.2);
        outline: none;
        transform: translateY(-2px);
    }
    
    .stTextInput > div > div:focus::before, 
    .stTextArea > div > div > textarea:focus::before {
        opacity: 0.1;
    }
    
    .stTextInput > div > div::placeholder, 
    .stTextArea > div > div > textarea::placeholder {
        color: var(--text-secondary);
        opacity: 0.6;
    }
    
    /* Chalk Red Chat Cards with Texture */
    .stMarkdown {
        background: 
            linear-gradient(135deg, 
                rgba(20, 20, 24, 0.9), 
                var(--card-chalk)),
            repeating-linear-gradient(
                45deg,
                transparent,
                transparent 20px,
                var(--chalk-dust) 20px,
                var(--chalk-dust) 21px
            );
        backdrop-filter: blur(20px) saturate(140%);
        -webkit-backdrop-filter: blur(20px) saturate(140%);
        border-radius: 25px;
        padding: 24px;
        margin: 16px 0;
        border: 1px solid var(--border-chalk);
        box-shadow: 
            0 8px 32px rgba(0, 0, 0, 0.4),
            inset 0 1px 0 var(--chalk-overlay),
            0 0 40px var(--chalk-dust);
        transition: var(--transition-smooth);
        position: relative;
        overflow: hidden;
    }
    
    .stMarkdown::before {
        content: '';
        position: absolute;
        top: -2px;
        left: -2px;
        right: -2px;
        bottom: -2px;
        background: var(--gradient-chalk);
        border-radius: 25px;
        opacity: 0;
        z-index: -1;
        transition: opacity var(--transition-smooth);
        filter: blur(2px);
    }
    
    .stMarkdown:hover {
        border-color: var(--chalk-red-light);
        transform: translateY(-4px) scale(1.01);
        box-shadow: 
            0 12px 40px var(--shadow-chalk),
            0 0 60px var(--chalk-dust),
            0 0 80px rgba(236, 112, 99, 0.1),
            inset 0 1px 0 var(--chalk-overlay);
        background: 
            linear-gradient(135deg, 
                rgba(20, 20, 24, 0.95), 
                rgba(231, 76, 60, 0.05));
    }
    
    .stMarkdown:hover::before {
        opacity: 0.1;
    }
    
    /* Chalk Red Expandable Cards */
    .streamlit-expanderHeader {
        background: 
            linear-gradient(135deg, 
                var(--chalk-dust), 
                rgba(20, 20, 24, 0.9)),
            linear-gradient(90deg,
                transparent 0%,
                var(--chalk-red-pale) 50%,
                transparent 100%);
        background-size: 100% 100%, 200% 100%;
        backdrop-filter: blur(10px);
        border: 1px solid var(--border-chalk);
        border-radius: 25px;
        padding: 18px 28px;
        font-weight: 600;
        color: var(--text-chalk);
        position: relative;
        overflow: hidden;
        transition: var(--transition-smooth);
        cursor: pointer;
        text-shadow: 0 1px 3px rgba(0, 0, 0, 0.2);
    }
    
    .streamlit-expanderHeader::after {
        content: '⚕️';
        position: absolute;
        right: 20px;
        font-size: 20px;
        animation: pulse 2s ease-in-out infinite;
    }
    
    .streamlit-expanderHeader:hover {
        background: 
            linear-gradient(135deg, 
                var(--chalk-red-soft), 
                rgba(20, 20, 24, 0.95));
        background-size: 100% 100%;
        box-shadow: 
            0 8px 32px var(--shadow-chalk),
            inset 0 1px 0 var(--chalk-overlay),
            0 0 30px var(--chalk-dust);
        transform: translateX(5px);
        border-color: var(--chalk-red-light);
    }
    
    .streamlit-expanderContent {
        background: linear-gradient(180deg, 
            rgba(20, 20, 24, 0.95), 
            rgba(10, 10, 12, 0.98));
        backdrop-filter: blur(20px);
        border: 1px solid var(--glass-border);
        border-top: none;
        border-radius: 0 0 25px 25px;
        padding: 28px;
        margin-top: -5px;
        box-shadow: inset 0 2px 8px rgba(0, 0, 0, 0.3);
    }
    
    /* Metrics with Professional Medical Style */
    [data-testid="metric-container"] {
        background: linear-gradient(135deg, rgba(255, 46, 46, 0.05), rgba(26, 26, 30, 0.9));
        border: 1px solid var(--border-color);
        border-radius: 20px;
        padding: 20px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
        transition: all 0.3s ease;
    }
    
    [data-testid="metric-container"]:hover {
        border-color: var(--primary-red);
        box-shadow: 0 8px 25px rgba(255, 46, 46, 0.2);
        transform: translateY(-2px);
    }
    
    /* Chalk Red Slider */
    .stSlider > div > div {
        background: 
            linear-gradient(90deg,
                var(--border-chalk),
                var(--chalk-dust));
        border-radius: 25px;
        box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.2);
    }
    
    .stSlider > div > div > div {
        background: var(--gradient-chalk);
        border-radius: 25px;
        box-shadow: 
            0 0 10px var(--chalk-red-light),
            inset 0 1px 2px var(--chalk-overlay);
    }
    
    .stSlider > div > div > div > div {
        background: var(--gradient-fire);
        border: 3px solid var(--chalk-white);
        box-shadow: 
            0 2px 10px var(--shadow-chalk),
            0 0 20px var(--chalk-red-light),
            inset 0 1px 3px rgba(255, 255, 255, 0.4);
        border-radius: 50%;
        cursor: grab;
    }
    
    .stSlider > div > div > div > div:active {
        cursor: grabbing;
        transform: scale(1.1);
    }
    
    /* Select Box with Rounded Corners */
    .stSelectbox > div > div {
        background: rgba(26, 26, 30, 0.8);
        border: 1px solid var(--border-color);
        border-radius: 20px;
        color: var(--text-primary);
        transition: all 0.3s ease;
    }
    
    .stSelectbox > div > div:focus-within {
        border-color: var(--primary-red);
        box-shadow: 0 0 20px rgba(255, 46, 46, 0.3);
    }
    
    /* Ultra-Modern File Upload Zone */
    .stFileUploader > div {
        background: linear-gradient(135deg, 
            rgba(20, 20, 24, 0.4), 
            rgba(255, 46, 46, 0.02));
        border: 2px dashed var(--glass-border);
        border-radius: 30px;
        padding: 40px;
        position: relative;
        overflow: hidden;
        transition: var(--transition-smooth);
    }
    
    .stFileUploader > div::before {
        content: '📄 \A Arraste arquivos médicos aqui';
        white-space: pre;
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        font-size: 14px;
        color: var(--text-secondary);
        opacity: 0.5;
        pointer-events: none;
        text-align: center;
        z-index: 0;
    }
    
    .stFileUploader > div:hover {
        border-color: var(--primary-red);
        border-style: solid;
        background: linear-gradient(135deg, 
            rgba(255, 46, 46, 0.08), 
            rgba(20, 20, 24, 0.6));
        box-shadow: 
            0 8px 32px rgba(255, 46, 46, 0.2),
            inset 0 1px 0 rgba(255, 255, 255, 0.05);
        transform: scale(1.02);
    }
    
    .stFileUploader > div:hover::before {
        opacity: 0.8;
        animation: bounce 1s ease-in-out;
    }
    
    @keyframes bounce {
        0%, 100% { transform: translate(-50%, -50%) scale(1); }
        50% { transform: translate(-50%, -50%) scale(1.1); }
    }
    
    /* Chalk Red Progress Bar */
    .stProgress > div > div {
        background: var(--gradient-sunset);
        border-radius: 25px;
        box-shadow: 
            0 2px 10px var(--shadow-chalk),
            0 0 20px var(--chalk-dust),
            inset 0 1px 2px var(--chalk-overlay);
        position: relative;
        overflow: hidden;
    }
    
    .stProgress > div > div::after {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg,
            transparent,
            rgba(255, 255, 255, 0.3),
            transparent);
        animation: progressShine 2s infinite;
    }
    
    @keyframes progressShine {
        0% { left: -100%; }
        100% { left: 100%; }
    }
    
    /* Alerts with Rounded Corners */
    .stAlert {
        background: rgba(26, 26, 30, 0.9);
        border: 1px solid var(--primary-red);
        border-radius: 20px;
        color: var(--text-primary);
        box-shadow: 0 4px 15px rgba(255, 46, 46, 0.2);
    }
    
    /* Code Blocks with Medical Theme */
    .stCodeBlock {
        background: rgba(26, 26, 30, 0.95);
        border: 1px solid var(--border-color);
        border-radius: 20px;
        padding: 20px;
        box-shadow: inset 0 2px 10px rgba(0, 0, 0, 0.3);
    }
    
    code {
        background: rgba(255, 46, 46, 0.1);
        color: var(--light-red);
        padding: 2px 8px;
        border-radius: 8px;
        font-family: 'JetBrains Mono', 'Fira Code', monospace;
    }
    
    /* Tables with Medical Style */
    .stDataFrame {
        border: 1px solid var(--border-color);
        border-radius: 20px;
        overflow: hidden;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
    }
    
    .stDataFrame thead {
        background: linear-gradient(135deg, rgba(255, 46, 46, 0.1), rgba(204, 0, 0, 0.05));
    }
    
    .stDataFrame tbody tr:hover {
        background: rgba(255, 46, 46, 0.05);
    }
    
    /* Spinner with Medical Red */
    .stSpinner > div {
        border-color: var(--primary-red) transparent transparent transparent;
    }
    
    /* Chalk Red Alert Messages */
    .stSuccess, .stError, .stWarning, .stInfo {
        border-radius: 25px;
        padding: 20px 28px;
        margin: 16px 0;
        backdrop-filter: blur(10px) saturate(120%);
        position: relative;
        overflow: hidden;
        animation: chalkSlideIn 0.5s ease-out;
    }
    
    @keyframes chalkSlideIn {
        from {
            opacity: 0;
            transform: translateY(-20px) scale(0.95);
            filter: blur(5px);
        }
        to {
            opacity: 1;
            transform: translateY(0) scale(1);
            filter: blur(0);
        }
    }
    
    @keyframes slideInFade {
        from {
            opacity: 0;
            transform: translateY(-20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .stSuccess {
        background: linear-gradient(135deg, 
            rgba(34, 197, 94, 0.15), 
            rgba(20, 20, 24, 0.9));
        border: 1px solid rgba(34, 197, 94, 0.3);
        box-shadow: 
            0 4px 20px rgba(34, 197, 94, 0.2),
            inset 0 1px 0 rgba(255, 255, 255, 0.05);
    }
    
    .stError {
        background: 
            linear-gradient(135deg, 
                var(--chalk-red-soft) 0%, 
                rgba(20, 20, 24, 0.9) 100%),
            repeating-linear-gradient(
                -45deg,
                transparent,
                transparent 20px,
                rgba(231, 76, 60, 0.03) 20px,
                rgba(231, 76, 60, 0.03) 21px
            );
        border: 2px solid var(--chalk-red);
        box-shadow: 
            0 4px 20px var(--shadow-chalk),
            inset 0 1px 0 var(--chalk-overlay),
            0 0 40px rgba(231, 76, 60, 0.2);
        position: relative;
    }
    
    .stError::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 2px;
        background: var(--gradient-fire);
        opacity: 0.8;
    }
    
    .stWarning {
        background: linear-gradient(135deg, 
            rgba(251, 191, 36, 0.15), 
            rgba(20, 20, 24, 0.9));
        border: 1px solid rgba(251, 191, 36, 0.3);
        box-shadow: 
            0 4px 20px rgba(251, 191, 36, 0.2),
            inset 0 1px 0 rgba(255, 255, 255, 0.05);
    }
    
    .stInfo {
        background: linear-gradient(135deg, 
            rgba(59, 130, 246, 0.15), 
            rgba(20, 20, 24, 0.9));
        border: 1px solid rgba(59, 130, 246, 0.3);
        box-shadow: 
            0 4px 20px rgba(59, 130, 246, 0.2),
            inset 0 1px 0 rgba(255, 255, 255, 0.05);
    }
    
    /* Chalk Red Custom Scrollbar */
    ::-webkit-scrollbar {
        width: 14px;
        height: 14px;
    }
    
    ::-webkit-scrollbar-track {
        background: 
            linear-gradient(90deg,
                var(--bg-secondary),
                var(--bg-chalk));
        border-radius: 25px;
        box-shadow: inset 0 0 10px rgba(0, 0, 0, 0.3);
    }
    
    ::-webkit-scrollbar-thumb {
        background: var(--gradient-chalk);
        border-radius: 25px;
        border: 2px solid var(--bg-secondary);
        box-shadow: 
            0 0 10px var(--chalk-dust),
            inset 0 1px 2px var(--chalk-overlay);
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: var(--gradient-fire);
        box-shadow: 
            0 0 15px var(--chalk-red-light),
            inset 0 1px 3px rgba(255, 255, 255, 0.3);
    }
    
    /* Tooltips with Rounded Corners */
    .stTooltipIcon {
        color: var(--primary-red);
    }
    
    [data-baseweb="tooltip"] > div {
        background: var(--card-bg);
        border: 1px solid var(--primary-red);
        border-radius: 15px;
        color: var(--text-primary);
        box-shadow: 0 4px 20px rgba(255, 46, 46, 0.3);
    }
    
    /* Chalk Red Links */
    a {
        color: var(--chalk-red);
        text-decoration: none;
        transition: all 0.3s ease;
        position: relative;
        font-weight: 500;
    }
    
    a::after {
        content: '';
        position: absolute;
        bottom: -2px;
        left: 0;
        width: 0;
        height: 2px;
        background: var(--gradient-sunset);
        transition: width 0.3s ease;
    }
    
    a:hover {
        color: var(--chalk-red-light);
        text-shadow: 
            0 0 10px var(--chalk-red-light),
            0 0 20px rgba(236, 112, 99, 0.3);
    }
    
    a:hover::after {
        width: 100%;
    }
    
    /* Radio Buttons and Checkboxes with Rounded Design */
    .stRadio > div > label > div:first-child,
    .stCheckbox > label > div:first-child {
        border-color: var(--border-color);
        border-radius: 50%;
    }
    
    .stRadio > div > label > div:first-child:checked,
    .stCheckbox > label > div:first-child:checked {
        background: var(--primary-red);
        border-color: var(--primary-red);
    }
    
    /* Toggle Switch with Rounded Design */
    .stCheckbox > label {
        cursor: pointer;
    }
    
    /* Date Input with Rounded Corners */
    .stDateInput > div > div {
        background: rgba(26, 26, 30, 0.8);
        border: 1px solid var(--border-color);
        border-radius: 20px;
        color: var(--text-primary);
    }
    
    /* Time Input with Rounded Corners */
    .stTimeInput > div > div {
        background: rgba(26, 26, 30, 0.8);
        border: 1px solid var(--border-color);
        border-radius: 20px;
        color: var(--text-primary);
    }
    
    /* Number Input with Rounded Corners */
    .stNumberInput > div > div {
        background: rgba(26, 26, 30, 0.8);
        border: 1px solid var(--border-color);
        border-radius: 20px;
        color: var(--text-primary);
    }
    
    /* Color Picker with Rounded Design */
    .stColorPicker > div > div {
        border-radius: 20px;
        border: 1px solid var(--border-color);
    }
    
    /* Camera Input with Rounded Corners */
    .stCameraInput > div {
        background: rgba(26, 26, 30, 0.6);
        border: 2px dashed var(--border-color);
        border-radius: 20px;
        padding: 30px;
    }
    
    /* Audio Input with Rounded Corners */
    .stAudioInput > div {
        background: rgba(26, 26, 30, 0.6);
        border: 2px dashed var(--border-color);
        border-radius: 20px;
        padding: 30px;
    }
    
    /* Tabs with Medical Style and Rounded Corners */
    .stTabs > div > div > div {
        background: transparent;
        border-bottom: 2px solid var(--border-color);
    }
    
    .stTabs > div > div > div > button {
        color: var(--text-secondary);
        border-radius: 15px 15px 0 0;
        transition: all 0.3s ease;
    }
    
    .stTabs > div > div > div > button[aria-selected="true"] {
        color: var(--primary-red);
        border-bottom: 3px solid var(--primary-red);
        background: rgba(255, 46, 46, 0.05);
    }
    
    /* Multiselect with Rounded Corners */
    .stMultiSelect > div > div {
        background: rgba(26, 26, 30, 0.8);
        border: 1px solid var(--border-color);
        border-radius: 20px;
        color: var(--text-primary);
    }
    
    /* Download Button with Special Style */
    .stDownloadButton > button {
        background: linear-gradient(135deg, var(--dark-red), var(--primary-red));
        border-radius: 25px;
        box-shadow: 0 4px 15px rgba(255, 46, 46, 0.3);
    }
    
    .stDownloadButton > button:hover {
        background: linear-gradient(135deg, var(--primary-red), var(--accent-red));
        box-shadow: 0 8px 25px rgba(255, 46, 46, 0.5);
    }
    
    /* Form Submit Button with Emphasis */
    .stFormSubmitButton > button {
        background: linear-gradient(135deg, var(--primary-red), var(--accent-red));
        border-radius: 25px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 1px;
        padding: 14px 40px;
        box-shadow: 0 6px 20px rgba(255, 46, 46, 0.4);
    }
    
    .stFormSubmitButton > button:hover {
        transform: translateY(-3px);
        box-shadow: 0 10px 30px rgba(255, 46, 46, 0.6);
    }
    
    /* Ultra-Modern Main Container with Advanced Glass */
    .main .block-container {
        padding: 3rem 4rem;
        max-width: 1400px;
        background: linear-gradient(135deg, 
            rgba(20, 20, 24, 0.4), 
            rgba(20, 20, 24, 0.2));
        backdrop-filter: blur(20px) saturate(180%);
        -webkit-backdrop-filter: blur(20px) saturate(180%);
        border-radius: 35px;
        border: 1px solid var(--glass-border);
        box-shadow: 
            0 20px 60px rgba(0, 0, 0, 0.4),
            inset 0 1px 0 rgba(255, 255, 255, 0.05),
            inset 0 -1px 0 rgba(0, 0, 0, 0.1);
        position: relative;
        animation: fadeInUp 0.6s ease-out;
    }
    
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    /* Chalk Red Header Effects */
    h1 {
        position: relative;
        display: inline-block;
    }
    
    h1::after {
        content: '';
        display: block;
        width: 80px;
        height: 5px;
        background: var(--gradient-chalk);
        margin-top: 15px;
        border-radius: 50px;
        animation: chalkPulseWidth 3s ease-in-out infinite;
        box-shadow: 
            0 0 20px var(--chalk-red-light),
            0 0 40px rgba(236, 112, 99, 0.3),
            inset 0 1px 2px rgba(255, 255, 255, 0.3);
        filter: blur(0.5px);
    }
    
    h1::before {
        content: '⚕️';
        position: absolute;
        left: -40px;
        top: 50%;
        transform: translateY(-50%);
        font-size: 30px;
        animation: rotateMedical 4s linear infinite;
        opacity: 0.8;
    }
    
    @keyframes chalkPulseWidth {
        0%, 100% { 
            width: 80px;
            opacity: 0.9;
            background: var(--gradient-chalk);
        }
        50% { 
            width: 120px;
            opacity: 1;
            background: var(--gradient-fire);
            filter: blur(0) brightness(1.2);
        }
    }
    
    @keyframes rotateMedical {
        from { transform: translateY(-50%) rotate(0deg); }
        to { transform: translateY(-50%) rotate(360deg); }
    }
    
    /* Medical Cross Icon Animation */
    @keyframes rotate {
        from { transform: rotate(0deg); }
        to { transform: rotate(360deg); }
    }
    
    /* Glow Effect for Important Elements */
    .medical-glow {
        box-shadow: 0 0 30px rgba(255, 46, 46, 0.5),
                    0 0 60px rgba(255, 46, 46, 0.3),
                    0 0 90px rgba(255, 46, 46, 0.1);
    }
    
    /* Chalk Red Medical Badges */
    .medical-badge {
        display: inline-block;
        padding: 8px 20px;
        background: var(--gradient-blood);
        color: var(--chalk-white);
        border-radius: 50px;
        font-size: 12px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 1.2px;
        position: relative;
        overflow: hidden;
        box-shadow: 
            0 6px 20px var(--shadow-chalk),
            inset 0 1px 0 var(--chalk-overlay),
            0 0 30px rgba(231, 76, 60, 0.3);
        animation: chalkBadgeGlow 3s ease-in-out infinite;
        border: 1px solid var(--chalk-stroke);
        text-shadow: 0 1px 3px rgba(0, 0, 0, 0.4);
    }
    
    /* Chalk Texture Overlay for Badge */
    .medical-badge::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 200%;
        height: 100%;
        background: linear-gradient(90deg,
            transparent,
            var(--chalk-overlay),
            transparent);
        animation: shimmerChalk 3s infinite;
    }
    
    @keyframes shimmerChalk {
        0% { transform: translateX(-100%); }
        100% { transform: translateX(100%); }
    }
    
    @keyframes chalkBadgeGlow {
        0%, 100% { 
            box-shadow: 
                0 6px 20px var(--shadow-chalk),
                inset 0 1px 0 var(--chalk-overlay),
                0 0 30px rgba(231, 76, 60, 0.3);
            filter: brightness(1) saturate(1);
        }
        50% { 
            box-shadow: 
                0 8px 30px rgba(231, 76, 60, 0.5),
                inset 0 1px 0 rgba(255, 255, 255, 0.3),
                0 0 50px var(--chalk-red-light),
                0 0 80px rgba(236, 112, 99, 0.2);
            filter: brightness(1.1) saturate(1.3);
        }
    }
    
    /* Chalk Red Loading Skeleton */
    @keyframes chalkSkeleton {
        0% { 
            background-position: -200% 0;
            filter: brightness(1);
        }
        50% {
            filter: brightness(1.1);
        }
        100% { 
            background-position: 200% 0;
            filter: brightness(1);
        }
    }
    
    .skeleton-loader {
        background: linear-gradient(90deg, 
            var(--chalk-dust) 0%, 
            var(--chalk-red-pale) 25%,
            var(--chalk-red-light) 50%, 
            var(--chalk-red-pale) 75%,
            var(--chalk-dust) 100%);
        background-size: 200% 100%;
        animation: chalkSkeleton 2s ease-in-out infinite;
        border-radius: 25px;
        position: relative;
        overflow: hidden;
    }
    
    .skeleton-loader::after {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: repeating-linear-gradient(
            90deg,
            transparent,
            transparent 10px,
            var(--chalk-overlay) 10px,
            var(--chalk-overlay) 11px
        );
        opacity: 0.3;
    }
    
    /* Floating Action Button */
    .floating-action {
        position: fixed;
        bottom: 30px;
        right: 30px;
        width: 60px;
        height: 60px;
        background: linear-gradient(135deg, var(--gradient-start), var(--gradient-end));
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: 
            0 10px 30px rgba(255, 46, 46, 0.4),
            inset 0 1px 0 rgba(255, 255, 255, 0.2);
        cursor: pointer;
        transition: var(--transition-bounce);
        z-index: 1000;
    }
    
    .floating-action:hover {
        transform: scale(1.1) rotate(90deg);
        box-shadow: 
            0 15px 40px rgba(255, 46, 46, 0.5),
            0 0 60px rgba(255, 46, 46, 0.3);
    }
    
    /* Medical Heartbeat Animation */
    @keyframes heartbeat {
        0%, 100% { transform: scale(1); }
        10% { transform: scale(1.1); }
        20% { transform: scale(1); }
        30% { transform: scale(1.15); }
        40% { transform: scale(1); }
    }
    
    .heartbeat {
        animation: heartbeat 2s ease-in-out infinite;
    }
    
    /* DNA Helix Loading Animation */
    @keyframes dnaRotate {
        0% { transform: rotateY(0deg); }
        100% { transform: rotateY(360deg); }
    }
    
    .dna-loader {
        width: 60px;
        height: 60px;
        position: relative;
        animation: dnaRotate 2s linear infinite;
        transform-style: preserve-3d;
    }
    
    /* Ultra-Modern Tooltip */
    [data-tooltip] {
        position: relative;
    }
    
    [data-tooltip]::after {
        content: attr(data-tooltip);
        position: absolute;
        bottom: 120%;
        left: 50%;
        transform: translateX(-50%) scale(0);
        background: linear-gradient(135deg, 
            rgba(20, 20, 24, 0.95), 
            rgba(20, 20, 24, 0.9));
        color: var(--text-primary);
        padding: 8px 16px;
        border-radius: 15px;
        font-size: 12px;
        white-space: nowrap;
        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.4);
        border: 1px solid var(--glass-border);
        backdrop-filter: blur(10px);
        opacity: 0;
        transition: var(--transition-bounce);
        pointer-events: none;
        z-index: 1000;
    }
    
    [data-tooltip]:hover::after {
        transform: translateX(-50%) scale(1);
        opacity: 1;
    }
    
    /* Smooth Page Transitions */
    * {
        scroll-behavior: smooth;
    }
    
    /* Enhanced Focus States */
    *:focus-visible {
        outline: 2px solid var(--primary-red);
        outline-offset: 4px;
        border-radius: 8px;
    }
    
    /* Performance Optimizations */
    .stApp * {
        will-change: auto;
    }
    
    .stApp *:hover {
        will-change: transform, box-shadow;
    }
</style>
""", unsafe_allow_html=True)

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

def process_uploaded_file(uploaded_file) -> Dict[str, Any]:
    """Processa arquivo enviado e retorna informações estruturadas."""
    file_info = {
        "name": uploaded_file.name,
        "type": uploaded_file.type,
        "size": uploaded_file.size,
        "content": None,
        "preview": None,
        "error": None
    }
    
    try:
        # Processar imagens
        if uploaded_file.type.startswith('image/'):
            # Converter imagem para base64 para enviar ao Claude
            bytes_data = uploaded_file.getvalue()
            base64_image = base64.b64encode(bytes_data).decode('utf-8')
            
            # Criar preview para UI
            image = Image.open(io.BytesIO(bytes_data))
            file_info["content"] = {
                "type": "image",
                "media_type": uploaded_file.type,
                "data": base64_image
            }
            file_info["preview"] = image
            
        # Processar PDFs
        elif uploaded_file.type == 'application/pdf':
            pdf_reader = PyPDF2.PdfReader(uploaded_file)
            text_content = ""
            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                text_content += f"\n--- Página {page_num + 1} ---\n"
                text_content += page.extract_text()
            
            file_info["content"] = {
                "type": "text",
                "data": text_content
            }
            file_info["preview"] = f"PDF com {len(pdf_reader.pages)} páginas"
            
        # Processar arquivos de texto
        elif uploaded_file.type.startswith('text/') or uploaded_file.name.endswith(('.txt', '.md', '.csv')):
            text_content = uploaded_file.read().decode('utf-8')
            file_info["content"] = {
                "type": "text",
                "data": text_content
            }
            file_info["preview"] = text_content[:500] + ("..." if len(text_content) > 500 else "")
            
        # Processar documentos Word (se tiver python-docx instalado)
        elif uploaded_file.type in ['application/vnd.openxmlformats-officedocument.wordprocessingml.document', 
                                   'application/msword']:
            try:
                import docx
                doc = docx.Document(uploaded_file)
                text_content = "\n".join([paragraph.text for paragraph in doc.paragraphs])
                file_info["content"] = {
                    "type": "text",
                    "data": text_content
                }
                file_info["preview"] = text_content[:500] + ("..." if len(text_content) > 500 else "")
            except ImportError:
                file_info["error"] = "python-docx não está instalado. Instale com: pip install python-docx"
            except Exception as e:
                file_info["error"] = f"Erro ao processar documento Word: {str(e)}"
                
        else:
            file_info["error"] = f"Tipo de arquivo não suportado: {uploaded_file.type}"
            
    except Exception as e:
        file_info["error"] = f"Erro ao processar arquivo: {str(e)}"
    
    return file_info

def create_message_content(user_input: str, file_contexts: List[Dict[str, Any]]) -> Any:
    """Cria conteúdo da mensagem incluindo texto e arquivos anexados."""
    content = []
    
    # Adicionar contexto dos arquivos primeiro
    for file_info in file_contexts:
        if file_info.get("content"):
            if file_info["content"]["type"] == "image":
                content.append({
                    "type": "image",
                    "source": {
                        "type": "base64",
                        "media_type": file_info["content"]["media_type"],
                        "data": file_info["content"]["data"]
                    }
                })
            elif file_info["content"]["type"] == "text":
                # Adicionar contexto do documento como texto
                doc_context = f"\n\n[ANEXO] **Arquivo anexado: {file_info['name']}**\n"
                doc_context += f"Tipo: {file_info['type']}\n"
                doc_context += f"Conteúdo:\n{file_info['content']['data']}\n"
                content.append({
                    "type": "text",
                    "text": doc_context
                })
    
    # Adicionar a mensagem do usuário
    content.append({
        "type": "text",
        "text": user_input
    })
    
    # Se houver apenas texto, retornar como string simples
    if len(content) == 1 and content[0]["type"] == "text":
        return content[0]["text"]
    
    return content

def get_claude_response(user_input: str, conversation_history=None, extended_thinking=False, file_contexts=None) -> str:
    """Obtém resposta do Claude com suporte a histórico de conversa, pensamento estendido e arquivos anexados."""
    try:
        # Preparar mensagens incluindo histórico de conversa
        messages = []
        if conversation_history:
            messages.extend(conversation_history)
        
        # Criar conteúdo da mensagem com arquivos se fornecidos
        if file_contexts:
            message_content = create_message_content(user_input, file_contexts)
        else:
            message_content = user_input
        
        # Adicionar a mensagem atual do usuário
        messages.append({"role": "user", "content": message_content})
        
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
            max_tokens=32000,
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

def generate_medical_report_pdf(conversation):
    """Gera um relatório médico em PDF ultra-estruturado com o conteúdo do chat."""
    try:
        from reportlab.lib import colors
        from reportlab.lib.pagesizes import A4
        from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib.units import inch, mm
        from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT, TA_RIGHT
        from reportlab.platypus.flowables import HRFlowable
        from reportlab.lib.colors import HexColor
        
        # Configuração do arquivo PDF
        timestamp = datetime.now()
        filename = f"relatorio_medico_{timestamp.strftime('%Y%m%d_%H%M%S')}.pdf"
        
        # Criar o documento PDF
        doc = SimpleDocTemplate(
            filename,
            pagesize=A4,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=72
        )
        
        # Container para elementos do PDF
        story = []
        
        # Clean Professional Color Palette - Medical Guide Template Style
        COLOR_PRIMARY = HexColor('#DC2626')       # Clean Red (Main headers)
        COLOR_SECONDARY = HexColor('#991B1B')     # Deep Red (Section headers)  
        COLOR_ACCENT = HexColor('#EF4444')        # Bright Red (Highlights)
        COLOR_BG_SECTION = HexColor('#FEF2F2')    # Very Light Red (Section backgrounds)
        COLOR_BG_HEADER = HexColor('#FEE2E2')     # Light Red (Header backgrounds)
        COLOR_TEXT_PRIMARY = HexColor('#1F2937')  # Dark Grey (Body text)
        COLOR_TEXT_SECONDARY = HexColor('#6B7280') # Medium Grey (Secondary text)
        COLOR_BORDER = HexColor('#E5E7EB')        # Light Grey (Borders)
        COLOR_SUCCESS = HexColor('#059669')       # Green (Success indicators)
        
        # Estilos personalizados
        styles = getSampleStyleSheet()
        
        # Estilo para título principal
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor=COLOR_PRIMARY,
            spaceAfter=30,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        )
        
        # Estilo para subtítulos
        subtitle_style = ParagraphStyle(
            'CustomSubtitle',
            parent=styles['Heading2'],
            fontSize=14,
            textColor=COLOR_SECONDARY,
            spaceAfter=12,
            spaceBefore=20,
            alignment=TA_LEFT,
            fontName='Helvetica-Bold'
        )
        
        # Estilo para texto normal
        body_style = ParagraphStyle(
            'CustomBody',
            parent=styles['BodyText'],
            fontSize=11,
            textColor=COLOR_TEXT_PRIMARY,
            alignment=TA_JUSTIFY,
            spaceBefore=6,
            spaceAfter=6,
            leading=14
        )
        
        # Estilo para perguntas do usuário
        user_style = ParagraphStyle(
            'UserStyle',
            parent=styles['BodyText'],
            fontSize=11,
            textColor=COLOR_TEXT_PRIMARY,
            leftIndent=20,
            rightIndent=20,
            spaceBefore=10,
            spaceAfter=10,
            borderColor=COLOR_BORDER,
            borderWidth=0,
            borderPadding=10,
            backColor=COLOR_BG_SECTION
        )
        
        # Estilo para respostas do assistente
        assistant_style = ParagraphStyle(
            'AssistantStyle',
            parent=styles['BodyText'],
            fontSize=11,
            textColor=COLOR_TEXT_PRIMARY,
            leftIndent=20,
            rightIndent=20,
            spaceBefore=10,
            spaceAfter=10,
            leading=14,
            alignment=TA_JUSTIFY
        )
        
        # Clean Professional Header - Medical Guide Style
        story.append(Spacer(1, 20))
        
        # Main Title
        story.append(Paragraph(
            "<b>RELATÓRIO MÉDICO</b>",
            title_style
        ))
        
        # Subtitle
        story.append(Paragraph(
            "Sistema IZZA MD PhD - Inteligência Artificial Médica",
            ParagraphStyle('SubTitle',
                          parent=styles['Normal'],
                          fontSize=12,
                          textColor=COLOR_TEXT_SECONDARY,
                          alignment=TA_CENTER,
                          spaceAfter=20)
        ))
        
        # Clean horizontal line
        story.append(HRFlowable(
            width="100%",
            thickness=2,
            color=COLOR_PRIMARY,
            spaceBefore=5,
            spaceAfter=20,
            hAlign='CENTER'
        ))
        # Document Information Section - Clean Design
        story.append(Paragraph(
            "<b>INFORMAÇÕES DO DOCUMENTO</b>",
            ParagraphStyle('SectionTitle',
                          parent=styles['Heading2'],
                          fontSize=12,
                          textColor=COLOR_SECONDARY,
                          spaceBefore=10,
                          spaceAfter=10)
        ))
        
        # Information table with clean style
        info_data = [
            ['Data:', timestamp.strftime('%d/%m/%Y')],
            ['Hora:', timestamp.strftime('%H:%M:%S')],
            ['Documento:', f'REL-{timestamp.strftime("%Y%m%d-%H%M%S")}'],
            ['Sistema:', 'IZZA MD PhD'],
            ['Modelo IA:', 'Claude 4.1 Opus'],
            ['Total de Interações:', str(len(conversation))]
        ]
        
        info_table = Table(info_data, colWidths=[2*inch, 4*inch])
        info_table.setStyle(TableStyle([
            # Labels column
            ('BACKGROUND', (0, 0), (0, -1), COLOR_BG_HEADER),
            ('TEXTCOLOR', (0, 0), (0, -1), COLOR_TEXT_SECONDARY),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            # Values column
            ('BACKGROUND', (1, 0), (1, -1), colors.white),
            ('TEXTCOLOR', (1, 0), (1, -1), COLOR_TEXT_PRIMARY),
            ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
            # Clean borders and spacing
            ('GRID', (0, 0), (-1, -1), 0.5, COLOR_BORDER),
            ('ALIGN', (0, 0), (0, -1), 'RIGHT'),
            ('ALIGN', (1, 0), (1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('LEFTPADDING', (0, 0), (-1, -1), 12),
            ('RIGHTPADDING', (0, 0), (-1, -1), 12),
        ]))
        
        story.append(info_table)
        story.append(Spacer(1, 30))
        
        # Medical Warning Section - Clean Style
        story.append(Paragraph(
            "<b>AVISO IMPORTANTE</b>",
            ParagraphStyle('WarningTitle',
                          parent=styles['Heading2'],
                          fontSize=11,
                          textColor=COLOR_SECONDARY,
                          spaceBefore=10,
                          spaceAfter=8)
        ))
        
        warning_text = """Este relatório foi gerado por um sistema de inteligência artificial 
        para fins educacionais e de apoio diagnóstico. Este documento NÃO substitui 
        uma consulta médica profissional. Sempre procure um médico qualificado para 
        diagnósticos e tratamentos definitivos."""
        
        warning_style = ParagraphStyle(
            'Warning',
            parent=body_style,
            textColor=COLOR_TEXT_PRIMARY,
            fontSize=10,
            borderColor=COLOR_BORDER,
            borderWidth=1,
            borderPadding=10,
            backColor=COLOR_BG_SECTION
        )
        story.append(Paragraph(warning_text, warning_style))
        story.append(Spacer(1, 30))
        
        # Section 1: Executive Summary
        story.append(Paragraph(
            "<b>1. SUMÁRIO EXECUTIVO</b>",
            ParagraphStyle('SectionHeader',
                          parent=styles['Heading1'],
                          fontSize=14,
                          textColor=COLOR_SECONDARY,
                          spaceBefore=15,
                          spaceAfter=8)
        ))
        
        # Red line under section header
        story.append(HRFlowable(
            width="100%",
            thickness=2,
            color=COLOR_PRIMARY,
            spaceBefore=2,
            spaceAfter=12,
            hAlign='LEFT'
        ))
        
        # Summary content
        user_messages = [msg for msg in conversation if msg["role"] == "user"]
        assistant_messages = [msg for msg in conversation if msg["role"] == "assistant"]
        
        summary_text = f"""
        Este documento apresenta o registro completo da sessão de consulta médica realizada através do 
        Sistema IZZA MD PhD. Durante esta sessão foram processadas <b>{len(user_messages)}</b> consultas 
        com suas respectivas análises médicas baseadas em inteligência artificial.
        """
        
        story.append(Paragraph(
            summary_text,
            ParagraphStyle('SummaryText',
                          parent=styles['Normal'],
                          fontSize=11,
                          textColor=COLOR_TEXT_PRIMARY,
                          alignment=TA_JUSTIFY,
                          leftIndent=20,
                          rightIndent=20,
                          spaceBefore=8,
                          spaceAfter=20)
        ))
        
        # Section 2: Consultation History
        story.append(PageBreak())
        story.append(Paragraph(
            "<b>2. HISTÓRICO DE CONSULTAS</b>",
            ParagraphStyle('SectionHeader',
                          parent=styles['Heading1'],
                          fontSize=14,
                          textColor=COLOR_SECONDARY,
                          spaceBefore=15,
                          spaceAfter=8)
        ))
        
        # Red line under section header
        story.append(HRFlowable(
            width="100%",
            thickness=2,
            color=COLOR_PRIMARY,
            spaceBefore=2,
            spaceAfter=20,
            hAlign='LEFT'
        ))
        # Process each message in conversation
        consultation_num = 0
        for i, entry in enumerate(conversation, 1):
            role = entry.get("role", "")
            content = entry.get("content", "")
            
            # Clean HTML/Markdown content
            content = re.sub(r'<[^>]+>', '', str(content))
            content = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', content)
            content = re.sub(r'\*(.*?)\*', r'<i>\1</i>', content)
            content = content.replace('\n', '<br/>')
            
            if role == "user":
                consultation_num += 1
                
                # Clean consultation header
                story.append(Paragraph(
                    f"<b>Consulta {consultation_num}</b>",
                    ParagraphStyle('ConsultHeader',
                                 parent=styles['Heading2'],
                                 fontSize=12,
                                 textColor=COLOR_PRIMARY,
                                 spaceBefore=15,
                                 spaceAfter=10)
                ))
                
                # Question label
                story.append(Paragraph(
                    "<b>QUESTÃO:</b>",
                    ParagraphStyle('QuestionLabel',
                                 parent=styles['Normal'],
                                 fontSize=10,
                                 textColor=COLOR_TEXT_SECONDARY,
                                 spaceBefore=5,
                                 spaceAfter=5)
                ))
                
                # Question content with clean formatting
                story.append(Paragraph(
                    content,
                    user_style
                ))
                
            elif role == "assistant":
                # Response label
                story.append(Paragraph(
                    "<b>ANÁLISE MÉDICA:</b>",
                    ParagraphStyle('ResponseLabel',
                                 parent=styles['Normal'],
                                 fontSize=10,
                                 textColor=COLOR_TEXT_SECONDARY,
                                 spaceBefore=10,
                                 spaceAfter=5)
                ))
                
                # Response content with clean formatting
                if len(content) > 1000:
                    # Split into paragraphs for better readability
                    paragraphs = content.split('<br/>')
                    for para in paragraphs[:15]:  # Limit number of paragraphs
                        if para.strip():
                            # Detect and format lists
                            if para.strip().startswith('•') or para.strip().startswith('-'):
                                para = f'<font color="{COLOR_PRIMARY}">•</font> {para.strip()[1:].strip()}'
                            story.append(Paragraph(para.strip(), assistant_style))
                            story.append(Spacer(1, 4))
                else:
                    story.append(Paragraph(content, assistant_style))
                
                story.append(Spacer(1, 15))
                
                # Clean separator between consultations
                story.append(HRFlowable(
                    width="100%",
                    thickness=0.5,
                    color=COLOR_BORDER,
                    spaceBefore=10,
                    spaceAfter=10,
                    hAlign='LEFT'
                ))
        
        # Section 3: Conclusion
        story.append(PageBreak())
        story.append(Paragraph(
            "<b>3. CONCLUSÃO</b>",
            ParagraphStyle('ConclusionHeader',
                          parent=styles['Heading1'],
                          fontSize=14,
                          textColor=COLOR_SECONDARY,
                          spaceBefore=15,
                          spaceAfter=8)
        ))
        
        # Red line under section header
        story.append(HRFlowable(
            width="100%",
            thickness=2,
            color=COLOR_PRIMARY,
            spaceBefore=2,
            spaceAfter=12,
            hAlign='LEFT'
        ))
        story.append(Spacer(1, 15))
        
        conclusion_text = f"""
        Este relatório documenta a sessão de consulta médica realizada através do sistema IZZA MD PhD.
        Foram analisadas {len([m for m in conversation if m['role'] == 'user'])} consultas com respostas 
        detalhadas baseadas em evidências médicas e raciocínio clínico avançado.
        <br/><br/>
        <b>Observações Importantes:</b><br/>
        • Todas as análises são baseadas em literatura médica atualizada<br/>
        • O sistema utiliza raciocínio diagnóstico diferencial<br/>
        • As recomendações devem ser validadas por profissional médico<br/>
        • Este documento é confidencial e para uso médico-educacional
        """
        story.append(Paragraph(conclusion_text, body_style))
        story.append(Spacer(1, 30))
        
        # Rodapé
        footer_style = ParagraphStyle(
            'Footer',
            parent=body_style,
            fontSize=9,
            textColor=HexColor('#7F8C8D'),
            alignment=TA_CENTER
        )
        
        footer_text = f"""
        <b>Documento gerado automaticamente</b><br/>
        IZZA MD PhD - Sistema de Inteligência Médica<br/>
        {timestamp.strftime('%d de %B de %Y às %H:%M:%S')}<br/>
        Powered by Claude 4.1 Opus - Anthropic
        """
        story.append(HRFlowable(width="100%", thickness=1, color=HexColor('#BDC3C7')))
        story.append(Spacer(1, 10))
        story.append(Paragraph(footer_text, footer_style))
        
        # Gerar o PDF
        doc.build(story)
        
        return filename
        
    except ImportError:
        st.error("❌ Biblioteca ReportLab não instalada. Execute: pip install reportlab")
        return None
    except Exception as e:
        st.error(f"Erro ao gerar PDF: {e}")
        return None

def load_notes() -> list:
    """Carrega notas do armazenamento persistente local (sobrevive a refresh)."""
    try:
        with open(NOTES_FILE_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
            if isinstance(data, list):
                return data
            return []
    except FileNotFoundError:
        return []
    except Exception as e:
        st.warning(f"Não foi possível carregar as notas: {e}")
        return []

def save_notes_storage(notes: list) -> bool:
    """Salva notas no armazenamento persistente local."""
    try:
        with open(NOTES_FILE_PATH, "w", encoding="utf-8") as f:
            json.dump(notes, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        st.error(f"Erro ao salvar notas: {e}")
        return False

def sanitize_notes(notes: list) -> list:
    """Garante campos padrão em cada nota (retrocompatibilidade)."""
    sanitized: list = []
    for n in notes:
        if not isinstance(n, dict):
            continue
        nid = n.get("id") or f"note-{int(time.time()*1000)}"
        title = n.get("title", "")
        content = n.get("content", "")
        created_at = n.get("created_at") or n.get("updated_at") or datetime.now().isoformat(timespec="seconds")
        updated_at = n.get("updated_at") or created_at
        tags = n.get("tags") or []
        pinned = bool(n.get("pinned", False))
        sanitized.append({
            "id": nid,
            "title": title,
            "content": content,
            "created_at": created_at,
            "updated_at": updated_at,
            "tags": tags,
            "pinned": pinned,
        })
    return sanitized

def upsert_note(notes: list, note_id: Optional[str], title: str, content: str,
                tags: Optional[List[str]] = None, pinned: bool = False) -> list:
    """Insere ou atualiza uma nota e retorna a lista atualizada."""
    timestamp = datetime.now().isoformat(timespec="seconds")
    if note_id:
        for n in notes:
            if n.get("id") == note_id:
                n["title"] = title
                n["content"] = content
                n["updated_at"] = timestamp
                n["tags"] = tags or []
                n["pinned"] = bool(pinned)
                break
        else:
            notes.append({
                "id": note_id,
                "title": title,
                "content": content,
                "updated_at": timestamp,
                "created_at": timestamp,
                "tags": tags or [],
                "pinned": bool(pinned),
            })
    else:
        new_id = f"note-{int(time.time()*1000)}"
        notes.append({
            "id": new_id,
            "title": title,
            "content": content,
            "updated_at": timestamp,
            "created_at": timestamp,
            "tags": tags or [],
            "pinned": bool(pinned),
        })
    return notes

def delete_note(notes: list, note_id: str) -> list:
    """Remove uma nota pelo id e retorna a lista atualizada."""
    return [n for n in notes if n.get("id") != note_id]

def count_tokens_in_conversation(conversation):
    """Estima a quantidade de tokens na conversa atual."""
    # Estimativa simples: aproximadamente 4 caracteres = 1 token
    total_chars = sum(len(entry.get('content', '')) for entry in conversation)
    return total_chars // 4

# Ultra-Modern Interface Header
st.markdown("""
<div class="main-header" style="text-align: center; padding: 30px 0; position: relative;">
    <div style="position: absolute; top: 0; left: 50%; transform: translateX(-50%); width: 300px; height: 2px;" class="skeleton-loader"></div>
    <h1 style="font-size: 3.5rem; margin: 0; font-weight: 900; letter-spacing: -2px;">
        <span style="animation: heartbeat 2s ease-in-out infinite; display: inline-block;">🩺</span> 
        Izza MD PhD 
        <span style="animation: rotateMedical 4s linear infinite; display: inline-block;">🧬</span>
    </h1>
    <p style="margin-top: 15px; font-size: 1.2rem; opacity: 0.9;">
        <span class="medical-badge" style="
            display: inline-block;
            padding: 8px 20px;
            background: linear-gradient(135deg, #FF2E2E, #CC0000);
            color: white;
            border-radius: 50px;
            font-size: 12px;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 1.2px;
            box-shadow: 0 6px 20px rgba(255, 46, 46, 0.4);
        ">NEXUS-MED ULTRA v5.0</span>
    </p>
    <p style="margin-top: 10px; opacity: 0.7; font-size: 1rem;">
        Diagnósticos Médicos com IA de Última Geração
    </p>
    <div style="position: absolute; bottom: 0; left: 50%; transform: translateX(-50%); width: 300px; height: 2px;" class="skeleton-loader"></div>
</div>
""", unsafe_allow_html=True)

# Ultra-Modern Medical Warning Card
st.markdown("""
<div style="
    background: linear-gradient(135deg, rgba(255, 46, 46, 0.15), rgba(20, 20, 24, 0.95));
    border: 2px solid rgba(255, 46, 46, 0.3);
    border-radius: 25px;
    padding: 28px;
    margin: 30px 0;
    backdrop-filter: blur(15px);
    box-shadow: 
        0 10px 40px rgba(255, 46, 46, 0.2),
        inset 0 1px 0 rgba(255, 255, 255, 0.05);
    position: relative;
    overflow: hidden;
    animation: slideInFade 0.6s ease-out;
">
    <div style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; 
        background: linear-gradient(45deg, transparent 30%, rgba(255, 46, 46, 0.05) 50%, transparent 70%);
        animation: shimmer 3s infinite;"></div>
    <div style="position: relative; display: flex; align-items: start; gap: 20px;">
        <span style="font-size: 36px; animation: pulse 2s infinite;">⚠️</span>
        <div style="flex: 1;">
            <h3 style="margin: 0 0 12px 0; color: #FF2E2E; font-weight: 800; font-size: 1.4rem;">AVISO MÉDICO CRÍTICO</h3>
            <p style="margin: 0; line-height: 1.7; font-size: 1rem; opacity: 0.95;">
                Este sistema utiliza IA para fins <strong>educacionais</strong> e de <strong>apoio diagnóstico</strong>.
                <span style="color: #FF6B6B; font-weight: 600;">NÃO substitui</span> consulta médica profissional.
                Sempre procure um <strong>médico qualificado</strong> para diagnósticos e tratamentos reais.
            </p>
            <p style="margin-top: 10px; padding: 10px; background: rgba(255, 46, 46, 0.1); border-radius: 15px;
                border-left: 4px solid #FF2E2E; font-weight: 600;">
                🚑 Em emergências, procure <span style="color: #FF2E2E;">IMEDIATAMENTE</span> o serviço de urgência mais próximo.
            </p>
        </div>
    </div>
</div>

<style>
@keyframes shimmer {
    0% { transform: translateX(-100%); }
    100% { transform: translateX(100%); }
}
</style>
""", unsafe_allow_html=True)

# Inicialização do estado da sessão
if "conversation" not in st.session_state:
    st.session_state.conversation = []
if "uploaded_files" not in st.session_state:
    st.session_state.uploaded_files = []
if "file_contexts" not in st.session_state:
    st.session_state.file_contexts = []
if "extended_thinking_mode" not in st.session_state:
    st.session_state.extended_thinking_mode = False

# Ultra-Modern Sidebar
with st.sidebar:
    st.markdown("""
    <div style="text-align: center; padding: 25px 0 20px 0; border-bottom: 2px solid rgba(255, 46, 46, 0.1); margin-bottom: 25px;">
        <h2 style="margin: 0; font-size: 2rem; font-weight: 800; background: linear-gradient(135deg, #FF2E2E, #FF0040);
            -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;">
            <span style="animation: rotateMedical 4s linear infinite; display: inline-block;">⚙️</span> Configurações
        </h2>
        <div class="skeleton-loader" style="height: 2px; width: 120px; margin: 15px auto 0; opacity: 0.5;"></div>
    </div>
    """, unsafe_allow_html=True)
    
    # Ultra-Modern System Info Cards
    api_status = '✅ Ativo' if os.getenv('ANTHROPIC_API_KEY') else '❌ Inativo'
    status_color = '#22C55E' if '✅' in api_status else '#FF2E2E'
    
    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, rgba(20, 20, 24, 0.95), rgba(20, 20, 24, 0.8));
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 20px;
        padding: 20px;
        margin-bottom: 20px;
        backdrop-filter: blur(10px);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3), inset 0 1px 0 rgba(255, 255, 255, 0.05);
    ">
        <div style="display: grid; gap: 12px;">
            <div style="display: flex; justify-content: space-between; align-items: center;
                padding: 10px; background: rgba(255, 46, 46, 0.05); border-radius: 12px;">
                <span style="font-weight: 600; opacity: 0.8;">🤖 Modelo</span>
                <span style="color: #FF6B6B; font-weight: 700;">Claude 4.1 Opus</span>
            </div>
            <div style="display: flex; justify-content: space-between; align-items: center;
                padding: 10px; background: rgba(255, 46, 46, 0.05); border-radius: 12px;">
                <span style="font-weight: 600; opacity: 0.8;">📝 Contexto</span>
                <span style="color: #FF6B6B; font-weight: 700;">32,000 tokens</span>
            </div>
            <div style="display: flex; justify-content: space-between; align-items: center;
                padding: 10px; background: rgba(255, 46, 46, 0.05); border-radius: 12px;">
                <span style="font-weight: 600; opacity: 0.8;">🔑 API</span>
                <span style="color: {status_color}; font-weight: 700;">{api_status}</span>
            </div>
            <div style="padding: 10px; background: rgba(255, 46, 46, 0.05); border-radius: 12px;">
                <span style="font-weight: 600; opacity: 0.8;">✨ Especialidades</span>
                <div style="margin-top: 8px; font-size: 0.9rem; opacity: 0.7; line-height: 1.5;">
                    Raciocínio avançado • Medicina baseada em evidências • Análise multimodal
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
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
        if token_estimate > 32000 * 0.7:
            st.warning(f"⚠️ Aproximando-se do limite de contexto ({token_estimate}/{32000})")
    
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
    
    # Ultra-Modern Action Buttons
    st.markdown("""
    <style>
        div[data-testid="stSidebar"] .stButton > button {
            background: linear-gradient(135deg, #FF2E2E, #CC0000);
            border: 1px solid rgba(255, 255, 255, 0.1);
            color: white;
            font-weight: 700;
            letter-spacing: 0.5px;
            border-radius: 25px;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            box-shadow: 0 4px 15px rgba(255, 46, 46, 0.3);
        }
        div[data-testid="stSidebar"] .stButton > button:hover {
            background: linear-gradient(135deg, #FF0040, #FF2E2E);
            transform: translateY(-2px);
            box-shadow: 0 8px 25px rgba(255, 46, 46, 0.4);
        }
    </style>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🗑️ Limpar", use_container_width=True):
            st.session_state.conversation = []
            st.rerun()
    
    with col2:
        export_format = st.radio("Formato:", ["TXT", "JSON"], horizontal=True, label_visibility="collapsed")
        if st.button("💾 Salvar", use_container_width=True):
            if export_format == "TXT":
                if (filename := save_conversation(st.session_state.conversation)):
                    st.success(f"✅ Salvo: {filename}")
            else:
                if (filename := export_conversation_json(st.session_state.conversation)):
                    st.success(f"✅ Exportado: {filename}")
    
    st.divider()
    
    # 📄 Exportar Relatório Médico em PDF
    st.markdown("""
    <div style="
        background: linear-gradient(135deg, rgba(231, 76, 60, 0.1), rgba(20, 20, 24, 0.9));
        border: 2px solid rgba(231, 76, 60, 0.3);
        border-radius: 20px;
        padding: 15px;
        margin: 20px 0;
    ">
        <h4 style="margin: 0 0 10px 0; text-align: center; color: #EC7063;">
            📄 Relatório Médico PDF
        </h4>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("**EXPORTAR RELATÓRIO PDF**", use_container_width=True, key="export_pdf"):
        if st.session_state.conversation:
            with st.spinner("Gerando relatório médico estruturado..."):
                pdf_filename = generate_medical_report_pdf(st.session_state.conversation)
                if pdf_filename:
                    st.success(f"Relatório gerado: {pdf_filename}")
                    
                    # Oferecer download do PDF
                    try:
                        with open(pdf_filename, "rb") as pdf_file:
                            pdf_bytes = pdf_file.read()
                            st.download_button(
                                label="⬇️ **BAIXAR RELATÓRIO PDF**",
                                data=pdf_bytes,
                                file_name=pdf_filename,
                                mime="application/pdf",
                                use_container_width=True,
                                key="download_pdf"
                            )
                    except Exception as e:
                        st.error(f"❌ Erro ao preparar download: {e}")
        else:
            st.warning("Nenhuma conversa para exportar. Inicie uma consulta primeiro.")
    
    st.markdown("""
    <div style="
        background: rgba(236, 112, 99, 0.05);
        border-radius: 15px;
        padding: 10px;
        margin-top: 10px;
        font-size: 0.85rem;
        opacity: 0.8;
    ">
        💡 <b>Dica:</b> O relatório PDF inclui formatação profissional, 
        sumário executivo e estrutura médica completa.
    </div>
    """, unsafe_allow_html=True)
    
    st.divider()
    
    # 📒 Notas (na sidebar)
    st.subheader("📒 Notas")

    # Estado inicial de notas
    if "notes" not in st.session_state:
        st.session_state.notes = sanitize_notes(load_notes())
    if "selected_note_id" not in st.session_state:
        st.session_state.selected_note_id = None
    if "note_title" not in st.session_state:
        st.session_state.note_title = ""
    if "note_body" not in st.session_state:
        st.session_state.note_body = ""
    if "note_tags" not in st.session_state:
        st.session_state.note_tags = ""
    if "note_pinned" not in st.session_state:
        st.session_state.note_pinned = False

    # Barra de busca e ordenação
    with st.container():
        q = st.text_input("🔎 Buscar (título/conteúdo/tags)", "", help="Filtra por título, conteúdo ou tags")
        sort_opt = st.selectbox("Ordenar por", ["Atualizadas recentemente", "Criadas recentemente", "Título (A-Z)"])

        notes = st.session_state.notes
        # Filtrar por query em título, conteúdo e tags
        def match_query(n: dict) -> bool:
            if not q:
                return True
            ql = q.lower()
            title = (n.get("title", "")).lower()
            content = (n.get("content", "")).lower()
            tags_list = [str(t).lower() for t in (n.get("tags") or [])]
            return (ql in title) or (ql in content) or any(ql in t for t in tags_list)

        filtered = [n for n in notes if match_query(n)]

        # Ordenação com pinned primeiro
        def sort_key(n: dict):
            if sort_opt == "Criadas recentemente":
                key = n.get("created_at", "")
            elif sort_opt == "Título (A-Z)":
                key = (n.get("title") or "").lower()
            else:
                key = n.get("updated_at", "")
            return (not n.get("pinned", False), key)

        filtered.sort(key=sort_key, reverse=(sort_opt != "Título (A-Z)"))

        # Lista e seleção
        def label(n: dict) -> str:
            t = n.get("title") or "(Sem título)"
            pin = "📌 " if n.get("pinned") else ""
            return f"{pin}{t} — {n.get('updated_at','')}"

        if filtered:
            idxs = list(range(len(filtered)))
            sel = st.selectbox("Notas", idxs, format_func=lambda i: label(filtered[i]))
            selected = filtered[sel]

            # Sincroniza seleção
            if st.session_state.selected_note_id != selected.get("id"):
                st.session_state.selected_note_id = selected.get("id")
                st.session_state.note_title = selected.get("title", "")
                st.session_state.note_body = selected.get("content", "")
                st.session_state.note_tags = ", ".join(selected.get("tags", []))
                st.session_state.note_pinned = bool(selected.get("pinned", False))
        else:
            st.info("Nenhuma nota encontrada.")
            selected = None

    # Editor compacto
    with st.container():
        st.text_input("Título", key="note_title")
        st.text_area("Conteúdo", key="note_body", height=160)
        st.text_input("Tags (separadas por vírgula)", key="note_tags")
        st.checkbox("Fixar (pinned)", key="note_pinned")

        b1, b2, b3, b4 = st.columns(4)
        with b1:
            if st.button("💾 Salvar", use_container_width=True):
                title = (st.session_state.note_title or "").strip()
                body = (st.session_state.note_body or "").strip()
                tags = [t.strip() for t in (st.session_state.note_tags or "").split(",") if t.strip()]
                pinned = bool(st.session_state.note_pinned)
                if not title and not body:
                    st.warning("Digite um título ou conteúdo para salvar.")
                else:
                    st.session_state.notes = upsert_note(
                        sanitize_notes(st.session_state.notes),
                        st.session_state.selected_note_id,
                        title,
                        body,
                        tags,
                        pinned,
                    )
                    if save_notes_storage(st.session_state.notes):
                        st.success("Nota salva.")
                    # Seleciona a última (nova) se era criação
                    if st.session_state.selected_note_id is None and st.session_state.notes:
                        st.session_state.selected_note_id = st.session_state.notes[-1]["id"]
        with b2:
            if st.button("🗑️ Excluir", use_container_width=True, disabled=st.session_state.selected_note_id is None):
                if st.session_state.selected_note_id:
                    st.session_state.notes = delete_note(st.session_state.notes, st.session_state.selected_note_id)
                    if save_notes_storage(st.session_state.notes):
                        st.success("Nota excluída.")
                    st.session_state.selected_note_id = None
                    st.session_state.note_title = ""
                    st.session_state.note_body = ""
                    st.session_state.note_tags = ""
                    st.session_state.note_pinned = False
        with b3:
            if st.button("📄 Duplicar", use_container_width=True, disabled=st.session_state.selected_note_id is None):
                sel_id = st.session_state.selected_note_id
                if sel_id:
                    src = next((n for n in st.session_state.notes if n.get("id") == sel_id), None)
                    if src:
                        st.session_state.notes = upsert_note(
                            st.session_state.notes,
                            None,
                            (src.get("title") or "") + " (cópia)",
                            src.get("content") or "",
                            src.get("tags") or [],
                            bool(src.get("pinned", False)),
                        )
                        save_notes_storage(st.session_state.notes)
                        st.success("Nota duplicada.")
        with b4:
            if st.button("➕ Nova", use_container_width=True):
                st.session_state.selected_note_id = None
                st.session_state.note_title = ""
                st.session_state.note_body = ""
                st.session_state.note_tags = ""
                st.session_state.note_pinned = False

    # Exportar / Importar
    with st.container():
        st.caption("Exportar/Importar")
        cexp, cimp = st.columns(2)
        with cexp:
            if st.button("⬇️ Exportar JSON", use_container_width=True):
                try:
                    export_blob = json.dumps(st.session_state.notes, ensure_ascii=False, indent=2)
                    st.download_button("Baixar notas.json", export_blob, file_name="notas.json", mime="application/json")
                except Exception as e:
                    st.error(f"Falha ao exportar: {e}")
        with cimp:
            up = st.file_uploader("Importar JSON", type=["json"], label_visibility="collapsed")
            if up is not None:
                try:
                    data = json.loads(up.read().decode("utf-8"))
                    if isinstance(data, list):
                        st.session_state.notes = sanitize_notes(data)
                        if save_notes_storage(st.session_state.notes):
                            st.success("Notas importadas.")
                    else:
                        st.warning("Arquivo inválido: esperado um array JSON de notas.")
                except Exception as e:
                    st.error(f"Falha ao importar: {e}")

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

# Seção de upload de arquivos
st.markdown("### 📎 Anexar Arquivos")
st.caption("Upload de imagens médicas, exames, PDFs ou documentos relevantes")

uploaded_files = st.file_uploader(
    "Anexe imagens, PDFs ou documentos ao contexto",
    type=['png', 'jpg', 'jpeg', 'gif', 'bmp', 'pdf', 'txt', 'md', 'csv', 'docx', 'doc'],
    accept_multiple_files=True,
    help="Suporta imagens (PNG, JPG, etc.), PDFs, documentos de texto e Word"
)

if uploaded_files:
    st.session_state.uploaded_files = uploaded_files
    st.session_state.file_contexts = []
    
    cols = st.columns(min(len(uploaded_files), 3))
    for idx, file in enumerate(uploaded_files):
        file_info = process_uploaded_file(file)
        st.session_state.file_contexts.append(file_info)
        
        with cols[idx % 3]:
            if file_info.get("error"):
                st.error(f"❌ {file.name}: {file_info['error']}")
            else:
                st.success(f"✅ {file.name}")
                
                # Mostrar preview
                if file_info.get("preview"):
                    if isinstance(file_info["preview"], Image.Image):
                        st.image(file_info["preview"], caption=file.name, use_column_width=True)
                    else:
                        with st.expander(f"Preview: {file.name}"):
                            st.text(file_info["preview"])
    
    # Botão para limpar arquivos
    if st.button("🗑️ Limpar Arquivos"):
        st.session_state.uploaded_files = []
        st.session_state.file_contexts = []
        st.rerun()

# Mostrar indicador de arquivos anexados
if st.session_state.file_contexts:
    valid_files = [f for f in st.session_state.file_contexts if not f.get("error")]
    if valid_files:
        st.info(f"📎 {len(valid_files)} arquivo(s) anexado(s) ao contexto da conversa")

st.divider()

# Chat
for entry in st.session_state.conversation:
    with st.chat_message(entry["role"]):
        # Renderizar conteúdo complexo (com imagens) ou simples (texto)
        if isinstance(entry["content"], list):
            for content_item in entry["content"]:
                if content_item.get("type") == "text":
                    st.markdown(content_item.get("text", ""))
                elif content_item.get("type") == "image":
                    # Mostrar indicador de imagem anexada
                    st.caption("🖼️ [Imagem anexada]")
        else:
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
        # Obter contexto de arquivos se houver
        file_contexts = st.session_state.file_contexts if st.session_state.file_contexts else None
        
        if use_extended_thinking:
            with st.spinner("🧠 Dr. Izza está realizando uma análise aprofundada com pensamento estendido..."):
                response = get_claude_response(
                    actual_prompt, 
                    conversation_history=conversation_history,
                    extended_thinking=True,
                    file_contexts=file_contexts
                )
        else:
            spinner_text = "🔬 Dr. Izza está analisando o caso com PIRM..."
            if file_contexts:
                spinner_text = "🔬 Dr. Izza está analisando o caso e os arquivos anexados com PIRM..."
            
            with st.spinner(spinner_text):
                response = get_claude_response(
                    prompt,
                    conversation_history=conversation_history,
                    file_contexts=file_contexts
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
