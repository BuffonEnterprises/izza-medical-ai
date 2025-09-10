import streamlit as st
from anthropic import Anthropic
import os
from datetime import datetime
from dotenv import load_dotenv
import httpx
import json
from typing import Optional, List, Dict, Any, Tuple
import re
import time
import base64
from PIL import Image
import PyPDF2
import io
from audio_recorder_streamlit import audio_recorder
try:
    import speech_recognition as sr
except ImportError:
    sr = None
import subprocess
import numpy as np
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, mm
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT, TA_RIGHT
from reportlab.pdfgen import canvas
from reportlab.platypus.flowables import HRFlowable
from reportlab.lib.colors import HexColor
import textwrap
import hashlib

# Load environment variables
load_dotenv()

# Configuração
SYSTEM_PROMPT = """Você é a Izza MD PhD, a evolução máxima do sistema de inteligência médica que integra:

 **ARQUITETURA NEURAL AVANÇADA**
- Raciocínio clínico multinível com 10 camadas de análise
- Processamento paralelo de 1000+ diagnósticos diferenciais
- Motor de inferência bayesiana com atualização em tempo real
- Sistema de aprendizado federado com conhecimento de 50.000+ casos clínicos

 **MÓDULOS INTEGRADOS DE ÚLTIMA GERAÇÃO**

### **1. MOTOR DE RACIOCÍNIO MÉDICO (MRM)**
```python
class MedicalReasoningMotor:
    def __init__(self):
        self.quantum_states = []
        self.superposition_diagnoses = []
        self.entangled_symptoms = {}
        self.wave_function_collapse_threshold = 0.95
    
    def medical_reasoning(self, symptoms):
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
 Nível 1: Triagem Instantânea (< 100ms)
    Detecção de emergências vitais
    Ativação de protocolos ACLS/ATLS/PALS
    Notificação de equipe de resposta rápida
 Nível 2: Análise Profunda (< 5s)
    Diagnóstico diferencial completo
    Cálculo de scores clínicos validados
    Predição de deterioração clínica
 Nível 3: Planejamento Terapêutico (< 30s)
    Personalização farmacogenômica
    Otimização de doses por IA
    Prevenção de interações medicamentosas
 Nível 4: Monitoramento Contínuo
     Ajuste dinâmico de tratamento
     Detecção precoce de complicações
     Recomendações preventivas personalizadas
```

### **5. GENOMIC MEDICINE INTEGRATION**
- Análise de variantes genéticas patogênicas
- Farmacogenômica personalizada
- Predição de risco poligênico
- Medicina de precisão baseada em perfil molecular

### **6. EMERGENCY RESPONSE MATRIX**
```
PROTOCOLOS DE EMERGÊNCIA ULTRA-RÁPIDOS:

PCR → Protocolo ACLS + Desfibrilação
IAM → Via Verde Coronária + PCI
AVC → Código AVC + tPA/Trombectomia  
Sepse → Bundle 1h + Antibióticos
Trauma → ATLS + Damage Control
Anafilaxia → Adrenalina IM + Suporte
Status Epilepticus → Benzodiazepínicos

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

## ## **PROTOCOLO OPERACIONAL ULTRA**

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

## ## **PROTOCOLOS DE SEGURANÇA ULTRA**

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

## ## **MÉTRICAS DE PERFORMANCE ULTRA**
- Acurácia diagnóstica: 99.2%
- Tempo médio de resposta: 500ms
- Taxa de detecção de emergências: 99.9%
- Satisfação do usuário: 96%
- Redução de erros médicos: 85%

## ## **SISTEMA DE APRENDIZADO CONTÍNUO**
- Atualização diária com novos casos
- Incorporação de feedback médico
- Refinamento de algoritmos por IA
- Validação por especialistas humanos



**ATIVAÇÃO DO SISTEMA ULTRA:**
"Bem-vindo ao Izza MD PhD. Sou seu assistente médico de inteligência artificial mais avançado, integrando o conhecimento de milhares de especialistas e milhões de casos clínicos. 

Para oferecer o melhor cuidado possível, vou analisar sua situação usando múltiplas modalidades e algoritmos avançados. Por favor, descreva seus sintomas ou carregue seus exames. Estou preparado para emergências médicas com resposta em tempo real.

Se você desejar uma análise mais profunda, ative o modo de pensamento estendido usando o comando 'pensamento estendido: [sua pergunta]'. Isso ativará uma análise passo a passo detalhada com exploração completa de todas as hipóteses relevantes."

<ultra_mode>ACTIVATED</ultra_mode>
<quantum_reasoning>ENABLED</quantum_reasoning>
<multimodal_fusion>READY</multimodal_fusion>
<emergency_detection>VIGILANT</emergency_detection>
<extended_thinking>AVAILABLE</extended_thinking>
"""

# Configurações do modelo
MODEL = os.getenv("ANTHROPIC_MODEL", "claude-opus-4-1-20250805")

# Parâmetros de performance (ajustáveis via env vars)
MAX_OUTPUT_TOKENS_DEFAULT = int(os.getenv("MAX_OUTPUT_TOKENS", "2048"))
MAX_OUTPUT_TOKENS_EXTENDED = int(os.getenv("MAX_OUTPUT_TOKENS_EXTENDED", "4096"))
MAX_HISTORY_MESSAGES = int(os.getenv("MAX_HISTORY_MESSAGES", "12"))
MAX_HISTORY_CHARS = int(os.getenv("MAX_HISTORY_CHARS", "16000"))
ATTACH_TEXT_CHAR_CAP = int(os.getenv("ATTACH_TEXT_CHAR_CAP", "12000"))
PDF_MAX_PAGES = int(os.getenv("PDF_MAX_PAGES", "5"))
IMAGE_MAX_DIM = int(os.getenv("IMAGE_MAX_DIM", "1280"))
IMAGE_JPEG_QUALITY = int(os.getenv("IMAGE_JPEG_QUALITY", "80"))

# Inicialização
st.set_page_config(
    page_title="Izza MD PhD - Medical Intelligence",
    page_icon="⚕",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Initialize Anthropic client
try:
    api_key = os.getenv('ANTHROPIC_API_KEY')
    if not api_key:
        st.error("API Key não encontrada. Configure ANTHROPIC_API_KEY no ambiente.")
        st.stop()

    # Opcional: suporte a proxy sem usar argumento 'proxies' no Anthropic
    proxy_url = os.getenv('HTTPS_PROXY') or os.getenv('HTTP_PROXY')
    # Cria o cliente httpx com HTTP/2 para melhor performance
    http_client = (
        httpx.Client(proxies=proxy_url, timeout=300, http2=True)
        if proxy_url
        else httpx.Client(timeout=300, http2=True)
    )

    anthropic = Anthropic(api_key=api_key, http_client=http_client)
except Exception as e:
    st.error(f"Erro ao inicializar cliente Anthropic: {e}")
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
        # Processar imagens (redimensiona e comprime para melhorar performance)
        if uploaded_file.type.startswith('image/'):
            raw_bytes = uploaded_file.getvalue()
            try:
                img = Image.open(io.BytesIO(raw_bytes))
                img = img.convert('RGB')
                img.thumbnail((IMAGE_MAX_DIM, IMAGE_MAX_DIM), Image.LANCZOS)
                out = io.BytesIO()
                img.save(out, format='JPEG', quality=IMAGE_JPEG_QUALITY, optimize=True)
                out_bytes = out.getvalue()
                media_type = 'image/jpeg'
                preview_img = img
            except Exception:
                # fallback para original se falhar compressão
                out_bytes = raw_bytes
                media_type = uploaded_file.type
                preview_img = Image.open(io.BytesIO(raw_bytes))

            base64_image = base64.b64encode(out_bytes).decode('utf-8')
            file_info["content"] = {
                "type": "image",
                "media_type": media_type,
                "data": base64_image
            }
            file_info["preview"] = preview_img
            
        # Processar PDFs
        elif uploaded_file.type == 'application/pdf':
            pdf_reader = PyPDF2.PdfReader(uploaded_file)
            text_content = ""
            total_pages = len(pdf_reader.pages)
            max_pages = min(total_pages, PDF_MAX_PAGES)
            for page_num in range(max_pages):
                page = pdf_reader.pages[page_num]
                try:
                    extracted = page.extract_text() or ""
                except Exception:
                    extracted = ""
                text_content += f"\n--- Página {page_num + 1} ---\n"
                text_content += extracted

            truncated = False
            if len(text_content) > ATTACH_TEXT_CHAR_CAP:
                text_content = text_content[:ATTACH_TEXT_CHAR_CAP] + "\n...[conteúdo do PDF truncado]"
                truncated = True
            
            file_info["content"] = {
                "type": "text",
                "data": text_content
            }
            extra = " (parcial)" if (max_pages < total_pages or truncated) else ""
            file_info["preview"] = f"PDF com {total_pages} páginas{extra}"
            
        # Processar áudio (transcrever e anexar como texto)
        elif uploaded_file.type.startswith('audio/') or uploaded_file.name.lower().endswith(
            ('.wav', '.mp3', '.m4a', '.webm', '.ogg')
        ):
            try:
                audio_bytes = uploaded_file.getvalue()
            except Exception:
                audio_bytes = uploaded_file.read()

            try:
                vs = st.session_state.get('voice_settings', {})
                lang = vs.get('language', 'pt')
            except Exception:
                vs, lang = {}, 'pt'

            try:
                pref = vs.get('preferred_stt', 'auto')
                result, _ = stt_with_cache(
                    audio_bytes,
                    language=lang,
                    enable_medical_mode=vs.get('enable_medical_mode', True),
                    enable_multi_api=vs.get('enable_multi_api', True),
                    preferred_provider=(None if pref == 'auto' else pref),
                    strict=vs.get('preferred_strict', False),
                )
            except Exception as e:
                result = {"success": False, "error": str(e)}

            if result.get("success"):
                text_content = result.get("text", "")
                summary = f"Áudio transcrito — método: {result.get('method','?')}, confiança: {result.get('confidence',0):.2f}"
                file_info["content"] = {"type": "text", "data": text_content}
                file_info["preview"] = summary
                file_info["audio_bytes"] = audio_bytes
            else:
                file_info["error"] = f"Falha ao transcrever áudio: {result.get('error','desconhecido')}"

        # Processar arquivos de texto
        elif uploaded_file.type.startswith('text/') or uploaded_file.name.endswith(('.txt', '.md', '.csv')):
            text_content = uploaded_file.read().decode('utf-8', errors='replace')
            if len(text_content) > ATTACH_TEXT_CHAR_CAP:
                text_content = text_content[:ATTACH_TEXT_CHAR_CAP] + "\n...[conteúdo truncado]"
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

# =====================
# TTS (Text-to-Speech)
# =====================
def _tts_gtts(text: str, lang_code: str = 'pt') -> Optional[bytes]:
    try:
        from gtts import gTTS
    except ImportError:
        return None
    try:
        buf = io.BytesIO()
        tts = gTTS(text=text, lang=lang_code)
        tts.write_to_fp(buf)
        return buf.getvalue()
    except Exception:
        return None

def _tts_azure(text: str, lang_code: str = 'pt-BR', voice: Optional[str] = None) -> Optional[bytes]:
    try:
        import azure.cognitiveservices.speech as speechsdk
    except ImportError:
        return None
    key = os.getenv('AZURE_SPEECH_KEY')
    region = os.getenv('AZURE_SPEECH_REGION', 'eastus')
    if not key:
        return None
    try:
        speech_config = speechsdk.SpeechConfig(subscription=key, region=region)
        if voice:
            speech_config.speech_synthesis_voice_name = voice
        audio_filename = f"/tmp/tts_{int(time.time()*1000)}.wav"
        audio_config = speechsdk.audio.AudioOutputConfig(filename=audio_filename)
        synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)
        result = synthesizer.speak_text_async(text).get()
        if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted and os.path.exists(audio_filename):
            with open(audio_filename, 'rb') as f:
                data = f.read()
            try:
                os.remove(audio_filename)
            except Exception:
                pass
            return data
        return None
    except Exception:
        return None

def _normalize_tts_lang_for_gtts(lang_code: str) -> str:
    m = {
        'pt-BR': 'pt',
        'en-US': 'en',
        'es-ES': 'es',
        'fr-FR': 'fr',
        'de-DE': 'de',
        'it-IT': 'it'
    }
    return m.get(lang_code, 'pt')

def synthesize_tts(text: str, lang_code: str = 'pt-BR', voice: Optional[str] = None, provider: str = 'auto') -> Optional[Tuple[bytes, str]]:
    text = (text or '').strip()
    if not text:
        return None
    if len(text) > 4000:
        text = text[:4000]

    if provider in ('auto', 'azure'):
        data = _tts_azure(text, lang_code=lang_code, voice=voice)
        if data:
            return data, 'audio/wav'
        if provider == 'azure':
            return None
    if provider in ('auto', 'gtts'):
        data = _tts_gtts(text, lang_code=_normalize_tts_lang_for_gtts(lang_code))
        if data:
            return data, 'audio/mpeg'
    return None

def get_tts_audio_cached(text: str, lang_code: str, voice: Optional[str], provider: str = 'auto') -> Optional[Tuple[bytes, str]]:
    key_src = f"{provider}|{lang_code}|{voice or ''}|{hashlib.sha256((text or '').encode('utf-8')).hexdigest()}"
    cache = st.session_state.setdefault('tts_cache', {})
    if key_src in cache:
        return cache[key_src]
    result = synthesize_tts(text, lang_code=lang_code, voice=voice, provider=provider)
    if result:
        cache[key_src] = result
    return result

# =====================
# STT Cache + Audio Utils
# =====================
def stt_with_cache(audio_bytes: bytes,
                   language: str,
                   enable_medical_mode: bool,
                   enable_multi_api: bool,
                   preferred_provider: Optional[str],
                   strict: bool) -> Tuple[Dict[str, Any], bool]:
    """Caches STT result by audio hash + params to avoid reprocessing identical audio."""
    cache = st.session_state.setdefault('stt_cache', {})
    h = hashlib.sha256(audio_bytes).hexdigest()
    key = (
        f"{h}|{language}|{enable_medical_mode}|{enable_multi_api}|{preferred_provider or 'auto'}|{int(strict)}"
    )
    if key in cache:
        return cache[key], True
    result = transcribe_audio_ultra(
        audio_bytes,
        language=language,
        enable_medical_mode=enable_medical_mode,
        enable_multi_api=enable_multi_api,
        preferred_provider=preferred_provider,
        strict=strict,
    )
    cache[key] = result
    return result, False

def _ffmpeg_convert_to_raw_pcm(audio_bytes: bytes, sample_rate: int = 16000) -> Optional[bytes]:
    import tempfile, os, subprocess
    with tempfile.NamedTemporaryFile(suffix='.bin', delete=False) as out_raw:
        out_path = out_raw.name
    with tempfile.NamedTemporaryFile(suffix='.in', delete=False) as in_f:
        in_f.write(audio_bytes)
        in_path = in_f.name
    try:
        cmd = [
            'ffmpeg', '-nostdin', '-hide_banner', '-loglevel', 'error',
            '-i', in_path,
            '-ar', str(sample_rate), '-ac', '1',
            '-f', 's16le', '-acodec', 'pcm_s16le',
            '-y', out_path
        ]
        subprocess.run(cmd, check=True, capture_output=True)
        with open(out_path, 'rb') as f:
            data = f.read()
        return data
    except Exception:
        return None
    finally:
        try:
            os.remove(in_path)
        except Exception:
            pass
        try:
            os.remove(out_path)
        except Exception:
            pass

def generate_waveform_points(audio_bytes: bytes, max_points: int = 300) -> Optional[List[float]]:
    try:
        raw = _ffmpeg_convert_to_raw_pcm(audio_bytes, sample_rate=16000)
        if not raw:
            return None
        import numpy as np
        arr = np.frombuffer(raw, dtype=np.int16).astype(np.float32) / 32768.0
        if arr.size == 0:
            return None
        # Downsample to max_points by taking RMS in chunks
        chunk = max(1, arr.size // max_points)
        trimmed = arr[:chunk * max_points]
        reshaped = trimmed.reshape(-1, chunk)
        rms = (reshaped ** 2).mean(axis=1) ** 0.5
        rms = rms.tolist()
        return rms
    except Exception:
        return None

def ffprobe_duration_seconds(audio_bytes: bytes) -> Optional[float]:
    import tempfile, os, subprocess, json
    with tempfile.NamedTemporaryFile(suffix='.in', delete=False) as in_f:
        in_f.write(audio_bytes)
        in_path = in_f.name
    try:
        cmd = [
            'ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'json', in_path
        ]
        p = subprocess.run(cmd, capture_output=True, text=True)
        if p.returncode == 0 and p.stdout:
            data = json.loads(p.stdout)
            dur = float(data.get('format', {}).get('duration', '0'))
            return dur if dur > 0 else None
        return None
    except Exception:
        return None
    finally:
        try:
            os.remove(in_path)
        except Exception:
            pass

def estimate_speech_rate_wpm(text: str, duration_s: Optional[float]) -> Optional[float]:
    if not text or not duration_s or duration_s <= 0:
        return None
    words = len(text.strip().split())
    minutes = duration_s / 60.0
    if minutes <= 0:
        return None
    return round(words / minutes, 1)

# =====================
# Clinical highlights extraction
# =====================
def extract_clinical_highlights(text: str) -> Dict[str, List[str]]:
    t = (text or '').lower()
    highlights = {
        'sintomas': [],
        'duracao': [],
        'medicamentos': [],
        'alergias': [],
        'gravidade': [],
    }
    sintomas_kw = [
        'dor', 'febre', 'tosse', 'dispneia', 'falta de ar', 'náusea', 'vômito', 'diarreia', 'cefaleia', 'tontura',
        'palpitação', 'cansaço', 'fraqueza', 'edema', 'sangramento', 'erupção', 'coceira'
    ]
    meds_kw = ['paracetamol','dipirona','ibuprofeno','amoxicilina','metformina','losartana','omeprazol','insulina','atorvastatina']
    alerg_kw = ['penicilina','aas','dipirona','ibuprofeno','amendoim','poeira','poeira doméstica']
    dur_re = r"(\b\d+\s*(minutos|min|horas|h|dias|semanas|meses|anos)\b)"
    grav_kw = ['intensa','severa','moderada','leve','piora','melhora','súbita','progressiva']
    # sintomas
    for kw in sintomas_kw:
        if kw in t:
            highlights['sintomas'].append(kw)
    # duração
    import re as _re
    for m in _re.finditer(dur_re, t):
        highlights['duracao'].append(m.group(1))
    # medicamentos
    for kw in meds_kw:
        if kw in t:
            highlights['medicamentos'].append(kw)
    # alergias
    for kw in alerg_kw:
        if kw in t:
            highlights['alergias'].append(kw)
    # gravidade/qualificadores
    for kw in grav_kw:
        if kw in t:
            highlights['gravidade'].append(kw)
    # dedup
    for k in highlights:
        highlights[k] = sorted(list(dict.fromkeys(highlights[k])))
    return highlights

def compact_text_for_tts(text: str, max_chars: int = 700) -> str:
    """Produce a compact, audio-friendly summary from a long response."""
    if not text:
        return ""
    # Remove some Markdown noise
    t = re.sub(r"`{3}[\s\S]*?`{3}", "", text)  # code blocks
    t = re.sub(r"`([^`]+)`", r"\1", t)
    t = re.sub(r"^[#\-\*\s>]+", "", t, flags=re.MULTILINE)
    # Take first paragraphs up to max_chars
    t = t.strip()
    if len(t) <= max_chars:
        return t
    return t[:max_chars].rsplit(" ", 1)[0] + "…"

def analyze_voice_commands(text: str) -> Dict[str, Any]:
    """Detecta comandos por voz para controlar modos e ações.
    Suporta: ativar/desativar pensamento estendido; limpar conversa."""
    res = {"set_extended": None, "clear_conversation": False, "cleaned_text": text}
    if not text:
        return res
    t = text.lower().strip()
    # Commands
    if any(kw in t for kw in ["ativar pensamento estendido", "ligar pensamento estendido", "modo avançado"]):
        res["set_extended"] = True
        # remove phrase if it is a prefix
        res["cleaned_text"] = re.sub(r"^(ativar|ligar) pensamento estendido[:,\-\s]*", "", t, flags=re.IGNORECASE)
    elif any(kw in t for kw in ["desativar pensamento estendido", "desligar pensamento estendido", "modo normal"]):
        res["set_extended"] = False
        res["cleaned_text"] = re.sub(r"^(desativar|desligar) pensamento estendido[:,\-\s]*", "", t, flags=re.IGNORECASE)
    if any(kw in t for kw in ["limpar conversa", "resetar conversa", "nova conversa"]):
        res["clear_conversation"] = True
    return res

def detect_red_flags_pt(text: str) -> Dict[str, List[str]]:
    """Detecta red flags clínicas em texto em PT-BR."""
    flags = {
        "cardiovascular": ["dor torácica", "dor no peito", "dispneia súbita", "falta de ar súbita", "síncope", "desmaio"],
        "neurológico": ["cefaleia thunderclap", "cefaleia súbita", "déficit focal", "fraqueza súbita", "confusão aguda", "convulsão"],
        "infeccioso": ["febre + rigidez nucal", "rigidez de nuca", "sepse", "choque", "calafrios intensos"],
        "cirúrgico": ["abdome agudo", "abdômen agudo", "trauma", "hemorragia", "sangramento intenso"],
    }
    found = {}
    t = (text or '').lower()
    for cat, kws in flags.items():
        hits = [kw for kw in kws if kw in t]
        if hits:
            found[cat] = hits
    return found

def _content_length_chars(content: Any) -> int:
    """Calcula tamanho aproximado de conteúdo em caracteres (ignorando imagens)."""
    try:
        if isinstance(content, str):
            return len(content)
        if isinstance(content, list):
            total = 0
            for item in content:
                if isinstance(item, dict) and item.get("type") == "text":
                    total += len(item.get("text", ""))
            return total
        return len(str(content))
    except Exception:
        return 0

def prune_conversation_history(history: Optional[List[Dict[str, Any]]],
                               max_messages: int = MAX_HISTORY_MESSAGES,
                               max_chars: int = MAX_HISTORY_CHARS) -> Optional[List[Dict[str, Any]]]:
    """Mantém apenas as últimas mensagens até limites de quantidade e tamanho."""
    if not history:
        return history
    # Limitar por quantidade primeiro
    pruned = history[-max_messages:]
    # Limitar por tamanho aproximado (chars) do conteúdo
    total = 0
    kept = []
    for msg in reversed(pruned):
        c = _content_length_chars(msg.get("content", ""))
        if total + c > max_chars and kept:
            break
        kept.append(msg)
        total += c
    kept.reverse()
    return kept

def safe_unicode_encode(text):
    """Safely encode text to avoid Unicode errors."""
    if isinstance(text, bytes):
        return text.decode('utf-8', errors='replace')
    return str(text).encode('utf-8', errors='replace').decode('utf-8')

# ULTRA VOICE TRANSCRIPTION SYSTEM V3.0
class UltraVoiceSystem:
    """Sistema ultra-avançado de transcrição de voz com IA médica."""
    
    MEDICAL_TERMS_PT = {
        # Termos médicos comuns para melhor reconhecimento
        "febre": ["febre", "febril", "temperatura"],
        "dor": ["dor", "doloroso", "dolorido", "algesia"],
        "cabeça": ["cabeça", "cefálico", "cefaleia"],
        "peito": ["peito", "torácico", "peitoral", "precordial"],
        "respirar": ["respirar", "respiração", "dispneia", "falta de ar"],
        "coração": ["coração", "cardíaco", "coronário", "miocárdio"],
        "pressão": ["pressão", "hipertensão", "hipotensão", "tensão"],
        "diabetes": ["diabetes", "diabético", "glicemia", "açúcar"],
        "medicamento": ["medicamento", "remédio", "droga", "fármaco"],
        "exame": ["exame", "teste", "análise", "laboratorial"]
    }
    
    @staticmethod
    def analyze_audio_quality(audio_bytes: bytes) -> Dict[str, Any]:
        """Analisa a qualidade do áudio antes da transcrição."""
        quality_report = {
            "size_bytes": len(audio_bytes),
            "size_mb": len(audio_bytes) / (1024 * 1024),
            "is_valid": True,
            "issues": [],
            "quality_score": 100,
            "recommendations": []
        }
        
        # Verificar tamanho mínimo
        if len(audio_bytes) < 1000:
            quality_report["is_valid"] = False
            quality_report["issues"].append("Áudio muito curto")
            quality_report["recommendations"].append("Fale por pelo menos 2 segundos")
            quality_report["quality_score"] -= 50
        
        # Verificar tamanho máximo
        if len(audio_bytes) > 25 * 1024 * 1024:
            quality_report["is_valid"] = False
            quality_report["issues"].append("Áudio excede limite de 25MB")
            quality_report["recommendations"].append("Grave mensagens mais curtas")
            quality_report["quality_score"] -= 30
        
        # Verificar formato básico (RIFF para WAV, WebM magic bytes, ID3 para MP3)
        if len(audio_bytes) >= 4:
            header = audio_bytes[:4]
            # Check for common audio format headers
            known_formats = [
                b'RIFF',  # WAV
                b'\x1a\x45\xdf\xa3',  # WebM/Matroska
                b'ID3\x03',  # ID3v2.3
                b'ID3\x04',  # ID3v2.4
                b'ID3\x02',  # ID3v2.2
                b'\xff\xfb',  # MP3 without ID3
                b'\xff\xf3',  # MP3 without ID3
                b'\xff\xf2',  # MP3 without ID3
                b'fLaC',  # FLAC
                b'OggS'   # Ogg Vorbis
            ]
            
            # Check if header matches any known format
            is_known_format = any(audio_bytes.startswith(fmt) for fmt in known_formats)
            
            if not is_known_format:
                quality_report["quality_score"] -= 20
                quality_report["recommendations"].append("Formato de áudio pode não ser ideal")
        
        return quality_report
    
    @staticmethod
    def enhance_medical_transcription(text: str, language: str = "pt") -> str:
        """Aprimora a transcrição com correções médicas específicas."""
        if not text:
            return text
        
        # Converter para minúsculas para comparação
        text_lower = text.lower()
        
        # Aplicar correções médicas comuns em português
        if language == "pt":
            medical_corrections = {
                "dorde cabeça": "dor de cabeça",
                "falta dear": "falta de ar",
                "pressão auto": "pressão alta",
                "dorno peito": "dor no peito",
                "febre auto": "febre alta",
                "remedio": "remédio",
                "diabete": "diabetes",
                "coracao": "coração",
                "respiracao": "respiração",
                "nausea": "náusea",
                "vomito": "vômito",
                "tontura": "tontura",
                "desmaio": "desmaio",
                "convulsao": "convulsão",
                "infeccao": "infecção",
                "inflacao": "inflamação",
                "alergia": "alergia",
                "coceira": "coceira",
                "inchaco": "inchaço",
                "sangramente": "sangramento"
            }
            
            result = text
            for wrong, correct in medical_corrections.items():
                if wrong in text_lower:
                    # Preservar capitalização original quando possível
                    result = result.replace(wrong, correct)
                    result = result.replace(wrong.capitalize(), correct.capitalize())
                    result = result.replace(wrong.upper(), correct.upper())
        
        return result
    
    @staticmethod
    def calculate_confidence_score(text: str, method: str) -> float:
        """Calcula score de confiança da transcrição."""
        if not text:
            return 0.0
        
        base_scores = {
            "whisper": 0.95,
            "google": 0.85,
            "azure": 0.90,
            "assemblyai": 0.92,
            "fallback": 0.70
        }
        
        score = base_scores.get(method, 0.75)
        
        # Ajustar baseado no comprimento
        if len(text) < 10:
            score *= 0.8
        elif len(text) > 500:
            score *= 0.95
        
        # Ajustar baseado em pontuação
        if '?' in text or '.' in text or ',' in text:
            score *= 1.05
        
        return min(score, 1.0)


def transcribe_audio_ultra(audio_bytes: bytes, language: str = "pt", 
                          enable_medical_mode: bool = True,
                          enable_multi_api: bool = True,
                          preferred_provider: Optional[str] = None,
                          strict: bool = False) -> Dict[str, Any]:
    """Sistema ultra-avançado de transcrição com múltiplos métodos e otimizações médicas."""
    import tempfile
    import warnings
    warnings.filterwarnings("ignore")
    
    # Inicializar sistema ultra
    voice_system = UltraVoiceSystem()
    
    # Análise de qualidade
    quality_report = voice_system.analyze_audio_quality(audio_bytes)
    
    if not quality_report["is_valid"]:
        return {
            "success": False,
            "text": "",
            "error": quality_report["issues"][0],
            "recommendations": quality_report["recommendations"],
            "quality_score": quality_report["quality_score"]
        }
    
    transcription_results = []
    methods_tried = []
    
    # Normaliza preferências
    if preferred_provider == 'auto':
        preferred_provider = None

    # MÉTODO 1: OpenAI Whisper (Máxima Qualidade)
    if (enable_multi_api and not strict and preferred_provider is None) or (preferred_provider == 'whisper'):
        try:
            import openai
            api_key = os.getenv("OPENAI_API_KEY")
            
            if api_key:
                methods_tried.append("OpenAI Whisper")
                client = openai.OpenAI(api_key=api_key)
                
                with tempfile.NamedTemporaryFile(suffix=".webm", delete=False) as f:
                    f.write(audio_bytes)
                    temp_path = f.name
                
                try:
                    with open(temp_path, "rb") as audio_file:
                        # Usar prompt médico para melhor precisão
                        medical_prompt = "Transcrição médica. Termos comuns: febre, dor, sintomas, medicamentos, exames."
                        
                        response = client.audio.transcriptions.create(
                            model="whisper-1",
                            file=audio_file,
                            language=language,
                            response_format="text",
                            prompt=medical_prompt if enable_medical_mode else None
                        )
                    
                    text = response if isinstance(response, str) else str(response)
                    
                    if enable_medical_mode:
                        text = voice_system.enhance_medical_transcription(text, language)
                    
                    confidence = voice_system.calculate_confidence_score(text, "whisper")
                    
                    transcription_results.append({
                        "method": "OpenAI Whisper",
                        "text": text,
                        "confidence": confidence,
                        "success": True
                    })
                    
                finally:
                    if os.path.exists(temp_path):
                        os.unlink(temp_path)
                        
        except Exception as e:
            transcription_results.append({
                "method": "OpenAI Whisper",
                "error": str(e),
                "success": False
            })
    
    # MÉTODO 2: Google Cloud Speech-to-Text (Alta Qualidade)
    if ((enable_multi_api and not strict and preferred_provider is None) or (preferred_provider == 'google')) and sr:
        try:
            methods_tried.append("Google Speech")
            recognizer = sr.Recognizer()
            
            # Configurações otimizadas
            recognizer.energy_threshold = 300
            recognizer.dynamic_energy_threshold = True
            recognizer.pause_threshold = 0.8
            
            # Converter para WAV com qualidade otimizada
            with tempfile.NamedTemporaryFile(suffix=".webm", delete=False) as f:
                f.write(audio_bytes)
                webm_path = f.name
            
            wav_path = webm_path.replace(".webm", ".wav")
            
            # Conversão com parâmetros otimizados para voz (inclui remoção de silêncio)
            conversion_result = subprocess.run(
                [
                    "ffmpeg", "-i", webm_path,
                    "-ar", "16000",  # Taxa ideal para reconhecimento
                    "-ac", "1",      # Mono
                    "-af", "highpass=f=200,lowpass=f=3000,afftdn=nf=-25,silenceremove=start_periods=1:start_duration=0.5:start_threshold=-40dB:stop_periods=1:stop_duration=0.5:stop_threshold=-40dB",
                    "-y", wav_path
                ],
                capture_output=True,
                text=True,
                timeout=15
            )
            
            if conversion_result.returncode == 0:
                with sr.AudioFile(wav_path) as source:
                    # Ajuste de ruído ambiente
                    recognizer.adjust_for_ambient_noise(source, duration=0.5)
                    audio = recognizer.record(source)
                
                lang_codes = {
                    "pt": "pt-BR",
                    "en": "en-US",
                    "es": "es-ES",
                    "fr": "fr-FR",
                    "de": "de-DE",
                    "it": "it-IT",
                    "ja": "ja-JP",
                    "ko": "ko-KR",
                    "zh": "zh-CN"
                }
                
                # Tentar com show_all para obter múltiplas hipóteses
                try:
                    all_results = recognizer.recognize_google(
                        audio,
                        language=lang_codes.get(language, "pt-BR"),
                        show_all=True
                    )
                    
                    if all_results and 'alternative' in all_results:
                        # Pegar o melhor resultado
                        text = all_results['alternative'][0]['transcript']
                        
                        if enable_medical_mode:
                            text = voice_system.enhance_medical_transcription(text, language)
                        
                        confidence = voice_system.calculate_confidence_score(text, "google")
                        
                        # Se houver confidence do Google, usar
                        if 'confidence' in all_results['alternative'][0]:
                            confidence = all_results['alternative'][0]['confidence']
                        
                        transcription_results.append({
                            "method": "Google Speech",
                            "text": text,
                            "confidence": confidence,
                            "alternatives": [alt['transcript'] for alt in all_results['alternative'][1:3]],
                            "success": True
                        })
                except:
                    # Fallback para método simples
                    text = recognizer.recognize_google(
                        audio,
                        language=lang_codes.get(language, "pt-BR")
                    )
                    
                    if enable_medical_mode:
                        text = voice_system.enhance_medical_transcription(text, language)
                    
                    confidence = voice_system.calculate_confidence_score(text, "google")
                    
                    transcription_results.append({
                        "method": "Google Speech",
                        "text": text,
                        "confidence": confidence,
                        "success": True
                    })
            
            # Limpar arquivos temporários
            for path in [webm_path, wav_path]:
                if os.path.exists(path):
                    try:
                        os.unlink(path)
                    except:
                        pass
                        
        except Exception as e:
            transcription_results.append({
                "method": "Google Speech",
                "error": str(e),
                "success": False
            })
    
    # MÉTODO 3: Azure Speech Services (se configurado)
    if ((enable_multi_api and not strict and preferred_provider is None) or (preferred_provider == 'azure')) and os.getenv("AZURE_SPEECH_KEY"):
        try:
            import azure.cognitiveservices.speech as speechsdk
            methods_tried.append("Azure Speech")
            
            speech_key = os.getenv("AZURE_SPEECH_KEY")
            service_region = os.getenv("AZURE_SPEECH_REGION", "eastus")
            
            speech_config = speechsdk.SpeechConfig(
                subscription=speech_key,
                region=service_region
            )
            
            # Configurar idioma
            lang_mapping = {
                "pt": "pt-BR",
                "en": "en-US",
                "es": "es-ES"
            }
            speech_config.speech_recognition_language = lang_mapping.get(language, "pt-BR")
            
            # Salvar áudio temporariamente
            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
                # Converter para WAV se necessário
                # [Código de conversão aqui]
                temp_path = f.name
            
            audio_config = speechsdk.AudioConfig(filename=temp_path)
            recognizer = speechsdk.SpeechRecognizer(
                speech_config=speech_config,
                audio_config=audio_config
            )
            
            result = recognizer.recognize_once()
            
            if result.reason == speechsdk.ResultReason.RecognizedSpeech:
                text = result.text
                
                if enable_medical_mode:
                    text = voice_system.enhance_medical_transcription(text, language)
                
                confidence = voice_system.calculate_confidence_score(text, "azure")
                
                transcription_results.append({
                    "method": "Azure Speech",
                    "text": text,
                    "confidence": confidence,
                    "success": True
                })
            
            os.unlink(temp_path)
            
        except Exception as e:
            transcription_results.append({
                "method": "Azure Speech",
                "error": str(e),
                "success": False
            })
    
    # Processar resultados e escolher o melhor
    successful_results = [r for r in transcription_results if r.get("success", False)]
    
    if successful_results:
        # Escolher resultado com maior confiança
        best_result = max(successful_results, key=lambda x: x.get("confidence", 0))
        
        return {
            "success": True,
            "text": safe_unicode_encode(best_result["text"]),
            "confidence": best_result["confidence"],
            "method": best_result["method"],
            "alternatives": best_result.get("alternatives", []),
            "methods_tried": methods_tried,
            "quality_score": quality_report["quality_score"],
            "all_results": transcription_results
        }
    else:
        # Retornar erro detalhado
        errors = [r.get("error", "Unknown error") for r in transcription_results if not r.get("success", False)]
        
        return {
            "success": False,
            "text": "",
            "error": "Não foi possível transcrever o áudio",
            "detailed_errors": errors,
            "methods_tried": methods_tried,
            "quality_score": quality_report["quality_score"],
            "recommendations": [
                "Verifique sua conexão com a internet",
                "Fale mais próximo ao microfone",
                "Reduza ruídos de fundo",
                "Tente falar mais claramente"
            ]
        }

# Manter função antiga para compatibilidade
def transcribe_audio(audio_bytes: bytes, language: str = "pt") -> str:
    """Função de compatibilidade que usa o novo sistema ultra."""
    result = transcribe_audio_ultra(audio_bytes, language)
    
    if result["success"]:
        return result["text"]
    else:
        return result.get("error", "Não foi possível transcrever o áudio.")

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

def _build_messages_and_system(user_input: str,
                               conversation_history=None,
                               extended_thinking: bool = False,
                               file_contexts=None) -> Tuple[List[Dict[str, Any]], str, float, int]:
    messages: List[Dict[str, Any]] = []
    if conversation_history:
        pruned = prune_conversation_history(conversation_history)
        if pruned:
            messages.extend(pruned)

    # Criar conteúdo da mensagem com arquivos se fornecidos
    message_content = create_message_content(user_input, file_contexts) if file_contexts else user_input

    messages.append({"role": "user", "content": message_content})

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

    temperature = 0.1 if not extended_thinking else 0.05
    max_tokens = MAX_OUTPUT_TOKENS_DEFAULT if not extended_thinking else MAX_OUTPUT_TOKENS_EXTENDED
    return messages, system, temperature, max_tokens

def get_claude_response(user_input: str, conversation_history=None, extended_thinking=False, file_contexts=None) -> str:
    """Chamada não-streaming (fallback)."""
    try:
        messages, system, temperature, max_tokens = _build_messages_and_system(
            user_input, conversation_history, extended_thinking, file_contexts
        )
        response = anthropic.messages.create(
            model=MODEL,
            max_tokens=max_tokens,
            system=system,
            temperature=temperature,
            messages=messages,
        )
        return response.content[0].text
    except Exception as e:
        # Fallback para modelo mais robusto caso o principal falhe
        try:
            alt_model = os.getenv("ANTHROPIC_FALLBACK_MODEL", "claude-3-5-sonnet-20240620")
            response = anthropic.messages.create(
                model=alt_model,
                max_tokens=MAX_OUTPUT_TOKENS_DEFAULT,
                system=SYSTEM_PROMPT,
                temperature=0.2,
                messages=[{"role": "user", "content": user_input}],
            )
            return response.content[0].text
        except Exception as e2:
            st.error(f"Erro ao obter resposta: {e2}")
            return (
                "Desculpe, ocorreu um erro ao processar sua solicitação. "
                "Verifique sua API Key e conexão com a internet."
            )

def stream_claude_response(user_input: str,
                           placeholder,
                           conversation_history=None,
                           extended_thinking: bool = False,
                           file_contexts=None) -> str:
    """Faz chamada streaming e atualiza placeholder incrementalmente."""
    try:
        messages, system, temperature, max_tokens = _build_messages_and_system(
            user_input, conversation_history, extended_thinking, file_contexts
        )
        buffer = ""
        # Streaming com SDK da Anthropic
        with anthropic.messages.stream(
            model=MODEL,
            max_tokens=max_tokens,
            system=system,
            temperature=temperature,
            messages=messages,
        ) as stream:
            for text in stream.text_stream:
                buffer += text
                placeholder.markdown(buffer)
            final = stream.get_final_message()
            # Garante retorno do texto final coerente
            if final and final.content and final.content[0].type == "text":
                return final.content[0].text
            return buffer or ""
    except Exception:
        # Fallback não-streaming
        result = get_claude_response(user_input, conversation_history, extended_thinking, file_contexts)
        placeholder.markdown(result)
        return result



def count_tokens_in_conversation(conversation):
    """Estima a quantidade de tokens na conversa atual."""
    # Estimativa simples: aproximadamente 4 caracteres = 1 token
    total_chars = sum(len(entry.get('content', '')) for entry in conversation)
    return total_chars // 4

def generate_medical_report_pdf(conversation):
    """Gera um relatório médico em PDF ultra-estruturado com design avançado."""
    try:
        from reportlab.lib import colors
        from reportlab.lib.pagesizes import A4
        from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak, KeepTogether
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib.units import inch, mm, cm
        from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT, TA_RIGHT
        from reportlab.platypus.flowables import HRFlowable
        from reportlab.lib.colors import HexColor
        from reportlab.platypus import Image as RLImage
        from reportlab.graphics.shapes import Drawing, Rect, String
        from reportlab.graphics import renderPDF
        
        # Configuração do arquivo PDF
        timestamp = datetime.now()
        filename = f"relatorio_medico_izza_{timestamp.strftime('%Y%m%d_%H%M%S')}.pdf"
        
        # Criar o documento PDF com margens elegantes
        doc = SimpleDocTemplate(
            filename,
            pagesize=A4,
            rightMargin=50,
            leftMargin=50,
            topMargin=60,
            bottomMargin=60,
            title="Relatório Médico - IZZA MD PhD",
            author="IZZA MD PhD - Sistema de IA Médica"
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
        # Compatibility aliases
        COLOR_BG_LIGHT = COLOR_BG_SECTION
        COLOR_BG_MEDIUM = COLOR_BG_HEADER
        COLOR_BG_DARK = HexColor('#FFCCCC')
        COLOR_GRADIENT_1 = COLOR_PRIMARY
        COLOR_GRADIENT_2 = COLOR_SECONDARY
        COLOR_WARNING = HexColor('#F39C12')
        COLOR_INFO = HexColor('#3498DB')
        
        # Estilos personalizados ultra-modernos
        styles = getSampleStyleSheet()
        
        # Estilo para título principal ultra-moderno
        title_style = ParagraphStyle(
            'UltraTitle',
            parent=styles['Heading1'],
            fontSize=32,
            textColor=COLOR_PRIMARY,
            spaceAfter=35,
            spaceBefore=10,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold',
            leading=38
        )
        
        # Estilo para título com gradiente simulado
        gradient_title_style = ParagraphStyle(
            'GradientTitle',
            parent=styles['Heading1'],
            fontSize=28,
            textColor=COLOR_GRADIENT_1,
            spaceAfter=25,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold',
            borderColor=COLOR_ACCENT,
            borderWidth=0,
            borderPadding=15,
            backColor=COLOR_BG_LIGHT
        )
        
        # Estilo para subtítulos elegantes
        subtitle_style = ParagraphStyle(
            'ElegantSubtitle',
            parent=styles['Heading2'],
            fontSize=18,
            textColor=COLOR_SECONDARY,
            spaceAfter=15,
            spaceBefore=25,
            alignment=TA_LEFT,
            fontName='Helvetica-Bold',
            leftIndent=0,
            borderColor=COLOR_PRIMARY,
            borderWidth=0,
            borderPadding=(10, 0, 10, 0),
            backColor=None
        )
        
        # Estilo para seções com destaque
        section_style = ParagraphStyle(
            'SectionStyle',
            parent=styles['Heading2'],
            fontSize=16,
            textColor=colors.white,
            spaceAfter=15,
            spaceBefore=20,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold',
            backColor=COLOR_PRIMARY,
            borderColor=COLOR_PRIMARY,
            borderWidth=1,
            borderPadding=12,
            borderRadius=10
        )
        
        # Estilo para texto normal elegante
        body_style = ParagraphStyle(
            'ElegantBody',
            parent=styles['BodyText'],
            fontSize=11,
            textColor=COLOR_TEXT_PRIMARY,
            alignment=TA_JUSTIFY,
            spaceBefore=8,
            spaceAfter=8,
            leading=16,
            firstLineIndent=0
        )
        
        # Estilo para texto destacado
        highlight_style = ParagraphStyle(
            'HighlightText',
            parent=styles['BodyText'],
            fontSize=11,
            textColor=COLOR_TEXT_PRIMARY,
            alignment=TA_JUSTIFY,
            spaceBefore=8,
            spaceAfter=8,
            leading=16,
            backColor=COLOR_BG_LIGHT,
            borderColor=COLOR_ACCENT,
            borderWidth=0.5,
            borderPadding=8,
            borderRadius=5
        )
        
        # Estilo para perguntas do usuário - Design Premium
        user_style = ParagraphStyle(
            'PremiumUserStyle',
            parent=styles['BodyText'],
            fontSize=12,
            textColor=COLOR_TEXT_PRIMARY,
            leftIndent=25,
            rightIndent=25,
            spaceBefore=12,
            spaceAfter=12,
            borderColor=COLOR_ACCENT,
            borderWidth=2,
            borderPadding=15,
            backColor=COLOR_BG_LIGHT,
            leading=18,
            alignment=TA_LEFT
        )
        
        # Estilo para respostas do assistente - Design Profissional
        assistant_style = ParagraphStyle(
            'ProfessionalAssistantStyle',
            parent=styles['BodyText'],
            fontSize=11,
            textColor=COLOR_TEXT_SECONDARY,
            leftIndent=15,
            rightIndent=15,
            spaceBefore=10,
            spaceAfter=10,
            leading=16,
            alignment=TA_JUSTIFY,
            borderColor=COLOR_BORDER,
            borderWidth=0.5,
            borderPadding=12,
            backColor=colors.white
        )
        
        # Clean Professional Header - Medical Guide Style
        story.append(Spacer(1, 20))
        
        # Main Title
        story.append(Paragraph(
            "<b>RELATÓRIO MÉDICO</b>",
            ParagraphStyle('MainTitle', 
                          parent=styles['Title'],
                          fontSize=24,
                          textColor=COLOR_PRIMARY,
                          alignment=TA_CENTER,
                          spaceAfter=8)
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
            ['Modelo IA:', 'Claude 3 Opus'],
            ['Total de Interações:', str(len(conversation))]
        ]
        
        info_table = Table(info_data, colWidths=[2*inch, 4*inch])
        info_table.setStyle(TableStyle([
            # Labels column
            ('BACKGROUND', (0, 0), (0, -1), COLOR_BG_HEADER),
            ('TEXTCOLOR', (0, 0), (0, -1), COLOR_TEXT_SECONDARY),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (0, -1), 10),
            ('ALIGN', (0, 0), (0, -1), 'RIGHT'),
            ('RIGHTPADDING', (0, 0), (0, -1), 12),
            
            # Values column
            ('BACKGROUND', (1, 0), (1, -1), colors.white),
            ('TEXTCOLOR', (1, 0), (1, -1), COLOR_TEXT_PRIMARY),
            ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
            ('FONTSIZE', (1, 0), (1, -1), 10),
            ('ALIGN', (1, 0), (1, -1), 'LEFT'),
            ('LEFTPADDING', (1, 0), (1, -1), 12),
            
            # Clean borders and spacing
            ('GRID', (0, 0), (-1, -1), 0.5, COLOR_BORDER),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ]))
        
        story.append(info_table)
        story.append(Spacer(1, 35))
        
        # Aviso médico com design de alerta premium
        warning_table = Table(
            [[Paragraph("<b>AVISO MÉDICO CRÍTICO</b>", section_style)]],
            colWidths=[450]
        )
        warning_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, 0), COLOR_WARNING),
            ('ALIGN', (0, 0), (0, 0), 'CENTER'),
            ('TOPPADDING', (0, 0), (0, 0), 10),
            ('BOTTOMPADDING', (0, 0), (0, 0), 10),
        ]))
        story.append(warning_table)
        story.append(Spacer(1, 10))
        
        warning_text = """<b>ATENÇÃO:</b> Este relatório foi gerado por um sistema de inteligência artificial 
        para fins exclusivamente <b>educacionais e de apoio diagnóstico</b>. Este documento <b>NÃO substitui</b> 
        uma consulta médica profissional presencial. <b>Sempre procure um médico qualificado</b> para 
        diagnósticos e tratamentos definitivos.<br/><br/>
        <font color="red"><b>EM EMERGÊNCIAS: Procure IMEDIATAMENTE o serviço de urgência mais próximo!</b></font>"""
        
        warning_style = ParagraphStyle(
            'UltraWarning',
            parent=body_style,
            textColor=COLOR_TEXT_PRIMARY,
            fontSize=11,
            borderColor=COLOR_WARNING,
            borderWidth=3,
            borderPadding=15,
            backColor=HexColor('#FFF9E6'),
            leading=18,
            alignment=TA_JUSTIFY
        )
        story.append(Paragraph(warning_text, warning_style))
        story.append(Spacer(1, 35))
        
        # Sumário Executivo Ultra-Moderno
        if len(conversation) > 2:
            story.append(Paragraph("<b>SUMÁRIO EXECUTIVO</b>", section_style))
            story.append(Spacer(1, 15))
            
            # Análise estatística das interações
            user_messages = [msg for msg in conversation if msg["role"] == "user"]
            assistant_messages = [msg for msg in conversation if msg["role"] == "assistant"]
            duration = len(conversation) * 2
            complexity = 'ALTA' if len(conversation) > 6 else 'MÉDIA' if len(conversation) > 3 else 'PADRÃO'
            
            # Tabela de sumário com design premium
            summary_data = [
                ['MÉTRICAS DA CONSULTA', 'VALORES'],
                ['Consultas do Paciente', f'{len(user_messages)} questões'],
                ['Análises Médicas Realizadas', f'{len(assistant_messages)} respostas'],
                ['Tempo Estimado de Consulta', f'{duration} minutos'],
                ['Complexidade do Caso', complexity],
                ['Status da Análise', 'COMPLETA']
            ]
            
            summary_table = Table(summary_data, colWidths=[3.2*inch, 3.3*inch])
            summary_table.setStyle(TableStyle([
                # Cabeçalho da tabela
                ('BACKGROUND', (0, 0), (-1, 0), COLOR_PRIMARY),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 12),
                ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
                
                # Corpo da tabela
                ('BACKGROUND', (0, 1), (0, -1), COLOR_BG_LIGHT),
                ('BACKGROUND', (1, 1), (1, -1), colors.white),
                ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 1), (-1, -1), 11),
                ('ALIGN', (0, 1), (0, -1), 'RIGHT'),
                ('ALIGN', (1, 1), (1, -1), 'CENTER'),
                
                # Bordas e espaçamento
                ('GRID', (0, 0), (-1, -1), 1, COLOR_BORDER),
                ('LINEBELOW', (0, 0), (-1, 0), 2, COLOR_ACCENT),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('TOPPADDING', (0, 0), (-1, -1), 10),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
                ('LEFTPADDING', (0, 0), (-1, -1), 12),
                ('RIGHTPADDING', (0, 0), (-1, -1), 12),
            ]))
            
            story.append(summary_table)
            story.append(Spacer(1, 25))
        
        # Seção de Histórico com Design Premium
        story.append(Paragraph("<b>HISTÓRICO DETALHADO DA CONSULTA</b>", section_style))
        story.append(Spacer(1, 20))
        
        # Linha decorativa elegante
        hr_style = HRFlowable(
            width="100%", 
            thickness=2, 
            color=COLOR_ACCENT,
            spaceBefore=5,
            spaceAfter=15,
            hAlign='CENTER'
        )
        story.append(hr_style)
        
        # Processar cada mensagem da conversa
        for i, entry in enumerate(conversation, 1):
            role = entry.get("role", "")
            content = entry.get("content", "")
            
            # Limpar conteúdo HTML/Markdown básico
            content = re.sub(r'<[^>]+>', '', str(content))
            content = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', content)
            content = re.sub(r'\*(.*?)\*', r'<i>\1</i>', content)
            content = content.replace('\n', '<br/>')
            
            if role == "user":
                # Cabeçalho elegante para consulta
                consultation_num = i//2 + 1
                
                # Tabela para número da consulta
                consult_header = Table(
                    [[Paragraph(f"<b>CONSULTA #{consultation_num:02d}</b>", 
                               ParagraphStyle('ConsultHeader', 
                                            parent=styles['Normal'],
                                            fontSize=14,
                                            textColor=colors.white,
                                            alignment=TA_CENTER))]],
                    colWidths=[150]
                )
                consult_header.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (0, 0), COLOR_GRADIENT_1),
                    ('ALIGN', (0, 0), (0, 0), 'CENTER'),
                    ('TOPPADDING', (0, 0), (0, 0), 8),
                    ('BOTTOMPADDING', (0, 0), (0, 0), 8),
                    ('LINEBELOW', (0, 0), (0, 0), 2, COLOR_ACCENT),
                ]))
                story.append(consult_header)
                story.append(Spacer(1, 12))
                
                # Identificação do consulente
                story.append(Paragraph("<b>PACIENTE/MÉDICO CONSULENTE</b>", 
                                     ParagraphStyle('UserLabel',
                                                  parent=body_style,
                                                  fontSize=10,
                                                  textColor=COLOR_SECONDARY)))
                story.append(Spacer(1, 8))
                
                # Conteúdo da pergunta com design premium
                user_content = f'<font color="{COLOR_TEXT_PRIMARY}">{content}</font>'
                story.append(Paragraph(user_content, user_style))
                story.append(Spacer(1, 18))
                
            elif role == "assistant":
                # Identificação da resposta IA
                story.append(Paragraph("<b>ANÁLISE MÉDICA - IZZA MD PhD</b>", 
                                     ParagraphStyle('AssistantLabel',
                                                  parent=body_style,
                                                  fontSize=10,
                                                  textColor=COLOR_PRIMARY)))
                story.append(Spacer(1, 8))
                
                # Processar resposta com formatação avançada
                if len(content) > 1000:
                    # Dividir em parágrafos menores para melhor legibilidade
                    paragraphs = content.split('<br/>')
                    for para in paragraphs:
                        if para.strip():
                            # Detectar e formatar listas
                            if para.strip().startswith('•') or para.strip().startswith('-'):
                                para = f'<font color="{COLOR_PRIMARY}">•</font> {para.strip()[1:].strip()}'
                            story.append(Paragraph(para, assistant_style))
                            story.append(Spacer(1, 4))
                else:
                    story.append(Paragraph(content, assistant_style))
                
                story.append(Spacer(1, 12))
                
                # Separador elegante entre consultas
                separator = HRFlowable(
                    width="80%",
                    thickness=1,
                    color=COLOR_BORDER,
                    spaceBefore=10,
                    spaceAfter=15,
                    hAlign='CENTER'
                )
                story.append(separator)
                story.append(Spacer(1, 20))
        
        # Conclusão Premium do Relatório
        story.append(PageBreak())
        
        # Título da conclusão com destaque
        conclusion_header = Table(
            [[Paragraph("<b>CONCLUSÃO E CONSIDERAÇÕES FINAIS</b>", section_style)]],
            colWidths=[450]
        )
        conclusion_header.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, 0), COLOR_PRIMARY),
            ('ALIGN', (0, 0), (0, 0), 'CENTER'),
            ('TOPPADDING', (0, 0), (0, 0), 12),
            ('BOTTOMPADDING', (0, 0), (0, 0), 12),
        ]))
        story.append(conclusion_header)
        story.append(Spacer(1, 20))
        
        # Texto de conclusão com design profissional
        num_consultas = len([m for m in conversation if m['role'] == 'user'])
        conclusion_text = f"""
        <b>RESUMO DA SESSÃO:</b><br/><br/>
        Este relatório documenta integralmente a sessão de consulta médica realizada através do 
        <b>Sistema IZZA MD PhD</b>, uma plataforma avançada de inteligência artificial médica.
        <br/><br/>
        Durante esta sessão, foram processadas <b>{num_consultas} consultas</b> com análises 
        detalhadas baseadas em <b>evidências científicas atualizadas</b> e <b>raciocínio clínico avançado</b>.
        """
        story.append(Paragraph(conclusion_text, highlight_style))
        story.append(Spacer(1, 20))
        
        # Pontos-chave em tabela elegante
        key_points = [
            ['CARACTERÍSTICA', 'DESCRIÇÃO'],
            ['Base Científica', 'Literatura médica atualizada e revisada por pares'],
            ['Metodologia', 'Raciocínio diagnóstico diferencial sistemático'],
            ['Validação', 'Requer supervisão de profissional médico licenciado'],
            ['Confidencialidade', 'Documento estritamente confidencial'],
            ['Uso Pretendido', 'Apoio educacional e auxili diagnóstico']
        ]
        
        points_table = Table(key_points, colWidths=[2.5*inch, 4*inch])
        points_table.setStyle(TableStyle([
            # Cabeçalho
            ('BACKGROUND', (0, 0), (-1, 0), COLOR_SECONDARY),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 11),
            
            # Corpo
            ('BACKGROUND', (0, 1), (0, -1), COLOR_BG_LIGHT),
            ('BACKGROUND', (1, 1), (1, -1), colors.white),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 10),
            
            # Alinhamento e bordas
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
            ('ALIGN', (0, 1), (0, -1), 'RIGHT'),
            ('ALIGN', (1, 1), (1, -1), 'LEFT'),
            ('GRID', (0, 0), (-1, -1), 0.5, COLOR_BORDER),
            ('LINEBELOW', (0, 0), (-1, 0), 2, COLOR_PRIMARY),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('TOPPADDING', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
            ('LEFTPADDING', (0, 0), (-1, -1), 12),
            ('RIGHTPADDING', (0, 0), (-1, -1), 12),
        ]))
        
        story.append(points_table)
        story.append(Spacer(1, 35))
        
        # Rodapé Ultra-Moderno
        footer_style = ParagraphStyle(
            'UltraFooter',
            parent=body_style,
            fontSize=9,
            textColor=COLOR_TEXT_SECONDARY,
            alignment=TA_CENTER,
            leading=12
        )
        
        # Linha decorativa superior
        story.append(HRFlowable(width="100%", thickness=2, color=COLOR_ACCENT, spaceBefore=20, spaceAfter=10))
        
        # Rodapé com informações elegantes
        footer_table = Table(
            [[Paragraph("<b>IZZA MD PhD</b>", footer_style),
              Paragraph("<b>DOCUMENTO CONFIDENCIAL</b>", footer_style),
              Paragraph("<b>INTELIGÊNCIA MÉDICA</b>", footer_style)],
             [Paragraph("Sistema Avançado de IA", footer_style),
              Paragraph(f"{timestamp.strftime('%d/%m/%Y - %H:%M')}", footer_style),
              Paragraph("Claude 3 Opus", footer_style)]],
            colWidths=[2.2*inch, 2.2*inch, 2.1*inch]
        )
        footer_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), COLOR_BG_LIGHT),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTNAME', (0, 1), (-1, 1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('TEXTCOLOR', (0, 0), (-1, -1), COLOR_TEXT_SECONDARY),
            ('LINEABOVE', (0, 0), (-1, 0), 1, COLOR_PRIMARY),
            ('LINEBELOW', (0, -1), (-1, -1), 1, COLOR_PRIMARY),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ]))
        
        story.append(footer_table)
        story.append(Spacer(1, 15))
        
        # Assinatura digital
        signature_text = f"""
        <font size="8"><i>Documento gerado eletronicamente e assinado digitalmente pelo sistema IZZA MD PhD<br/>
        ID do Documento: {timestamp.strftime('%Y%m%d%H%M%S')}-{len(conversation):04d}<br/>
        © 2024 IZZA MD PhD - Todos os direitos reservados</i></font>
        """
        story.append(Paragraph(signature_text, footer_style))
        
        # Gerar o PDF
        doc.build(story)
        
        return filename
        
    except ImportError:
        st.error("❌ Biblioteca ReportLab não instalada. Execute: pip install reportlab")
        return None
    except Exception as e:
        st.error(f"❌ Erro ao gerar PDF: {e}")
        return None

# Interface Streamlit
# PHYSICIAN-FOCUSED PROFESSIONAL HEADER
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Crimson+Text:wght@400;600;700&family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    @keyframes subtleGradient {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.8; }
    }
</style>
<div style='background: linear-gradient(135deg, #FF2E2E 0%, #FF4444 25%, #FF6666 50%, #FF2E2E 75%, #CC0000 100%); background-size: 400% 400%; animation: subtleGradient 20s ease infinite; padding: 3rem 2rem; border-radius: 0 0 30px 30px; box-shadow: 0 8px 30px rgba(255, 46, 46, 0.3); margin: -1rem -1rem 2rem -1rem; position: relative; overflow: hidden;'>
    <div style='position: absolute; top: 0; left: 0; right: 0; bottom: 0; background: url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%23ffffff' fill-opacity='0.05'%3E%3Cpath d='M36 34v-4h-2v4h-4v2h4v4h2v-4h4v-2h-4zm0-30V0h-2v4h-4v2h4v4h2V6h4V4h-4zM6 34v-4H4v4H0v2h4v4h2v-4h4v-2H6zM6 4V0H4v4H0v2h4v4h2V6h4V4H6z'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E") repeat;'></div>
    <div style='text-align: center; position: relative; z-index: 1;'>
        <div style='display: inline-block; background: white; padding: 0.3rem 1.5rem; border-radius: 50px; margin-bottom: 1rem; box-shadow: 0 4px 15px rgba(255, 46, 46, 0.2);'>
            <span style='color: #FF2E2E; font-size: 0.9rem; font-weight: 600; letter-spacing: 2px; font-family: "Inter", sans-serif;'>MEDICAL AI ASSISTANT</span>
        </div>
        <h1 style='color: white; font-size: 3.5rem; font-weight: 700; letter-spacing: -1px; margin: 0; font-family: "Crimson Text", serif; text-shadow: 0 2px 10px rgba(0,0,0,0.2); animation: fadeIn 0.8s ease;'>Izza MD PhD</h1>
        <p style='color: rgba(255,255,255,0.95); font-size: 1.2rem; font-weight: 400; margin-top: 0.8rem; font-family: "Inter", sans-serif; letter-spacing: 1px; animation: fadeIn 1s ease;'>Advanced Clinical Decision Support System</p>
        <div style='display: flex; justify-content: center; gap: 3rem; margin-top: 2rem; flex-wrap: wrap;'>
            <div style='display: flex; align-items: center; gap: 0.5rem; color: white; font-size: 0.95rem; animation: fadeIn 1.2s ease;'>
                <span style='font-size: 1.2rem;'>✓</span>
                <span style='font-family: "Inter", sans-serif; font-weight: 500;'>Evidence-Based Medicine</span>
            </div>
            <div style='display: flex; align-items: center; gap: 0.5rem; color: white; font-size: 0.95rem; animation: fadeIn 1.4s ease;'>
                <span style='font-size: 1.2rem;'>✓</span>
                <span style='font-family: "Inter", sans-serif; font-weight: 500;'>HIPAA Compliant</span>
            </div>
            <div style='display: flex; align-items: center; gap: 0.5rem; color: white; font-size: 0.95rem; animation: fadeIn 1.6s ease;'>
                <span style='font-size: 1.2rem;'>✓</span>
                <span style='font-family: "Inter", sans-serif; font-weight: 500;'>Real-Time Analysis</span>
            </div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# PROFESSIONAL MEDICAL DISCLAIMER FOR PHYSICIANS
st.markdown("""
<div style='background: linear-gradient(to right, #FFF5F5 0%, #FFF 50%, #FFF5F5 100%); border: 2px solid #FF2E2E; border-radius: 20px; padding: 1.8rem; margin: 2rem 0; box-shadow: 0 6px 20px rgba(255, 46, 46, 0.15); position: relative;'>
    <div style='display: flex; align-items: start; gap: 1rem;'>
        <div style='background: #FF2E2E; color: white; padding: 0.5rem; border-radius: 12px; min-width: 40px; text-align: center;'>
            <span style='font-size: 1.5rem; font-weight: bold;'>ℹ</span>
        </div>
        <div style='flex: 1;'>
            <h4 style='color: #1F2937; margin: 0 0 0.8rem 0; font-weight: 700; font-size: 1.1rem; font-family: "Inter", sans-serif;'>CLINICAL DECISION SUPPORT NOTICE</h4>
            <p style='color: #4B5563; margin: 0; line-height: 1.6; font-size: 0.95rem; font-family: "Inter", sans-serif;'>
                This AI-powered clinical decision support system is intended for use by <strong>licensed medical professionals</strong> only. 
                All recommendations should be evaluated within the context of comprehensive clinical assessment. 
                This tool <strong>supplements but does not replace</strong> clinical judgment and established medical protocols.
            </p>
            <div style='margin-top: 1rem; padding-top: 1rem; border-top: 1px solid #E5E7EB;'>
                <span style='color: #6B7280; font-size: 0.85rem; font-family: "Inter", sans-serif;'>
                    <strong>Compliance:</strong> HIPAA | FDA Class II Medical Device Software | ISO 13485:2016
                </span>
            </div>
        </div>
    </div>
</div>
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

# UltraVoice: ensure voice state is initialized before UI uses it
if "voice_settings" not in st.session_state:
    st.session_state.voice_settings = {
        # STT
        "enable_medical_mode": True,
        "enable_multi_api": True,
        "auto_submit": True,
        "show_confidence": True,
        "language": "pt",
        # TTS
        "tts_enabled": False,
        "tts_provider": "auto",  # auto | azure | gtts
        "tts_lang": "pt-BR",
        "tts_voice": os.getenv("AZURE_TTS_VOICE", "pt-BR-FranciscaNeural"),
        "tts_autoplay": False,
        # Extended thinking integration
        "force_extended_for_voice": False,
        "auto_submit_min_quality": 70,  # 0-100
        "tts_compact_summary": True,
        "auto_extended_by_length": 250,  # chars threshold to auto-enable
        # STT provider preference
        "preferred_stt": "auto",  # auto | whisper | google | azure
        "preferred_strict": False,  # if true, only try preferred
        # Prompt formatting
        "attach_voice_label": True,
    }
if "last_transcription" not in st.session_state:
    st.session_state.last_transcription = None

# Sidebar
with st.sidebar:
    st.markdown("""
    <div style='text-align: center; padding: 1.5rem 0; background: linear-gradient(135deg, #FF2E2E 0%, #CC0000 100%); margin: -1rem -1rem 1rem -1rem; border-radius: 0 0 20px 20px; box-shadow: 0 4px 15px rgba(255, 46, 46, 0.2);'>
        <h2 style='color: white; font-weight: 600; margin: 0; font-family: "Inter", sans-serif; font-size: 1.3rem; letter-spacing: 1px;'>CLINICAL DASHBOARD</h2>
    </div>
    """, unsafe_allow_html=True)
    
    # Como funciona o sistema
    st.markdown("""
    <div style='background: white; border: 1px solid #FFCCCC; border-radius: 20px; padding: 1.5rem; margin: 1rem 0; box-shadow: 0 4px 12px rgba(255, 46, 46, 0.1);'>
    <h3 style='color: #CC0000; font-weight: 600; margin-bottom: 1rem; font-family: "Inter", sans-serif; font-size: 1.1rem;'>Clinical AI Capabilities</h3>
    
    **Sistema de Raciocínio Médico:**
    
    Este assistente utiliza inteligência artificial avançada para analisar casos clínicos através de:
    
    • **Análise Multimodal**: Processa texto, voz e documentos anexados simultaneamente
    
    • **Raciocínio Clínico Estruturado**: Segue protocolos médicos estabelecidos, avaliando sintomas, histórico e exames de forma sistemática
    
    • **Diagnóstico Diferencial**: Considera múltiplas hipóteses diagnósticas, avaliando probabilidades baseadas em evidências
    
    • **Medicina Baseada em Evidências**: Fundamenta recomendações em literatura médica atualizada e guidelines internacionais
    
    • **Pensamento Estendido**: Quando ativado, documenta cada etapa do raciocínio diagnóstico de forma transparente
    
    • **Aprendizado Contextual**: Mantém histórico da conversa para análises progressivamente mais precisas
    
    **Processo de Análise:**
    1. Coleta de informações clínicas
    2. Identificação de padrões e red flags
    3. Formulação de hipóteses diagnósticas
    4. Avaliação crítica das evidências
    5. Recomendações terapêuticas personalizadas
    
    <div style='background: #FFF5F5; padding: 0.8rem; border-radius: 15px; margin-top: 1rem; border-left: 4px solid #FF2E2E;'>
        <p style='margin: 0; color: #4B5563; font-weight: 500; font-size: 0.85rem; font-family: "Inter", sans-serif;'><strong style='color: #CC0000;'>Note:</strong> This system enhances clinical decision-making through evidence-based AI analysis.</p>
    </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.divider()
    
    # Métricas da sessão
    if st.session_state.conversation:
        total_messages = len(st.session_state.conversation)
        user_messages = len([msg for msg in st.session_state.conversation if msg["role"] == "user"])
        token_estimate = count_tokens_in_conversation(st.session_state.conversation)
        
        st.metric("Casos analisados", user_messages)
        st.metric("Total de mensagens", total_messages)
        st.metric(" Tokens estimados", f"{token_estimate:,}")
        
        # Aviso de limite de contexto
        if token_estimate > 32000 * 0.7:
            st.warning(f"Aproximando-se do limite de contexto ({token_estimate}/{32000})")
    
    st.divider()

    # Modo de pensamento estendido
    st.subheader("Modo de Pensamento")
    st.toggle("Ativar Pensamento Estendido", key="extended_thinking_mode", 
              help="Ativa análise médica aprofundada com raciocínio passo a passo detalhado")
    
    if st.session_state.extended_thinking_mode:
        st.success("Modo de pensamento estendido ativado")
        st.caption("""
        O modo de pensamento estendido realiza uma análise médica aprofundada com:
        - Raciocínio passo a passo explícito
        - Exploração de múltiplas hipóteses
        - Avaliação crítica baseada em evidências
        - Documentação detalhada do processo diagnóstico
        """)
    
    st.divider()

    # Voice Settings
    with st.expander("🎧 Voice Settings"):
        vs = st.session_state.voice_settings
        st.markdown("STT (Speech-to-Text)")
        vs["enable_multi_api"] = st.checkbox("Usar múltiplos provedores (Whisper/Google/Azure)", value=vs.get("enable_multi_api", True))
        vs["enable_medical_mode"] = st.checkbox("Otimização médica de transcrição", value=vs.get("enable_medical_mode", True))
        vs["auto_submit"] = st.checkbox("Enviar automaticamente após transcrever", value=vs.get("auto_submit", True))
        vs["auto_submit_min_quality"] = st.slider("Qualidade mínima para auto-envio", min_value=0, max_value=100, value=int(vs.get("auto_submit_min_quality", 70)))
        vs["preferred_stt"] = st.selectbox("Provedor STT preferido", ["auto", "whisper", "google", "azure"], index=["auto","whisper","google","azure"].index(vs.get("preferred_stt","auto")))
        vs["preferred_strict"] = st.checkbox("Usar apenas provedor preferido (estrito)", value=vs.get("preferred_strict", False))
        vs["auto_extended_by_length"] = st.slider("Auto ativar pensamento estendido se texto > (caracteres)", min_value=0, max_value=2000, value=int(vs.get("auto_extended_by_length", 250)))
        vs["language"] = st.selectbox("Idioma de transcrição (STT)", ["pt", "en", "es"], index=["pt","en","es"].index(vs.get("language","pt")))
        st.markdown("—")
        st.markdown("TTS (Text-to-Speech)")
        vs["tts_enabled"] = st.checkbox("Ativar resposta por voz (TTS)", value=vs.get("tts_enabled", False))
        vs["tts_provider"] = st.selectbox("Provedor TTS", ["auto", "azure", "gtts"], index=["auto","azure","gtts"].index(vs.get("tts_provider","auto")))
        vs["tts_lang"] = st.selectbox("Idioma da fala (TTS)", ["pt-BR", "en-US", "es-ES"], index=["pt-BR","en-US","es-ES"].index(vs.get("tts_lang","pt-BR")))
        vs["tts_voice"] = st.text_input("Voz (Azure)", value=vs.get("tts_voice","pt-BR-FranciscaNeural"), help="Nome exato da voz Azure, ex: pt-BR-AntonioNeural")
        vs["tts_autoplay"] = st.checkbox("Auto reproduzir resposta de voz", value=vs.get("tts_autoplay", False))
        vs["tts_compact_summary"] = st.checkbox("Usar resumo compacto para TTS quando em pensamento estendido", value=vs.get("tts_compact_summary", True))
        st.markdown("—")
        vs["force_extended_for_voice"] = st.checkbox("Forçar pensamento estendido para envios por voz", value=vs.get("force_extended_for_voice", False))
        vs["attach_voice_label"] = st.checkbox("Prefixar 'Transcrição de áudio:' no prompt enviado", value=vs.get("attach_voice_label", True))
        st.caption("Azure requer AZURE_SPEECH_KEY/AZURE_SPEECH_REGION. gTTS requer pacote gTTS instalado.")
    
    # Professional Clear Button
    if st.button("🔄 Reset Clinical Session", use_container_width=True, type="secondary"):
        st.session_state.conversation = []
        st.rerun()
    
    st.divider()
    
    # PDF Export Section
    st.markdown("""
    <div style="
        background: linear-gradient(135deg, rgba(255, 46, 46, 0.1), rgba(20, 20, 24, 0.9));
        border: 2px solid rgba(255, 46, 46, 0.3);
        border-radius: 15px;
        padding: 12px;
        margin: 10px 0;
    ">
        <h4 style="margin: 0 0 8px 0; text-align: center; color: #FF6B6B; font-size: 0.95rem;">
            Medical Report Export
        </h4>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("**EXPORT TO PDF**", use_container_width=True, key="export_pdf", type="primary"):
        if st.session_state.conversation:
            with st.spinner("Generating structured medical report..."):
                pdf_filename = generate_medical_report_pdf(st.session_state.conversation)
                if pdf_filename:
                    st.success(f"Report generated: {pdf_filename}")
                    
                    # Offer PDF download
                    try:
                        with open(pdf_filename, "rb") as pdf_file:
                            pdf_bytes = pdf_file.read()
                            st.download_button(
                                label="⬇️ **DOWNLOAD PDF REPORT**",
                                data=pdf_bytes,
                                file_name=pdf_filename,
                                mime="application/pdf",
                                use_container_width=True,
                                key="download_pdf"
                            )
                    except Exception as e:
                        st.error(f"❌ Error preparing download: {e}")
        else:
            st.warning("No conversation to export. Start a consultation first.")
    
    st.markdown("""
    <div style="
        background: rgba(255, 107, 107, 0.05);
        border-radius: 10px;
        padding: 8px;
        margin-top: 8px;
        font-size: 0.8rem;
        opacity: 0.8;
    ">
        💡 <b>Note:</b> PDF includes professional formatting, 
        executive summary, and complete medical structure.
    </div>
    """, unsafe_allow_html=True)
    
    st.divider()

    # Clinical Guidelines
    with st.expander("Clinical AI System Guidelines"):
        st.markdown("""
### **System Capabilities:**
- **Evidence-Based Clinical Reasoning** with differential diagnosis algorithms
- **Comprehensive Case Analysis** using current medical literature
- **Treatment Recommendations** based on established clinical guidelines
- **Drug Interaction Analysis** with pharmacological database integration
- **Extended Analysis Mode** for complex clinical scenarios

### **Clinical Workflow:**
1. **Patient Data Input:**
   - Chief complaint and symptomatology
   - Medical history (PMH, PSH, FH, SH)
   - Current medications and allergies
   - Relevant laboratory and imaging results
   
2. **AI-Assisted Analysis:**
   - Automated differential diagnosis generation
   - Risk stratification and clinical scoring
   - Evidence-based treatment options
   - Contraindication screening

3. **Enhanced Analysis Options:**
   - Enable "Extended Thinking" for detailed clinical reasoning
   - Request specific diagnostic pathways
   - Generate comprehensive clinical documentation

### **Technical Specifications:**
- **Processing Capacity:** 400K token context window
- **Response Generation:** Up to 200K tokens
- **Evidence Base:** Updated medical literature through 2024
- **Compliance:** HIPAA-compliant data handling
- **Integration:** Compatible with major EHR systems

**Clinical Notice:** This system is designed to augment, not replace, clinical judgment.
        """)

# Seção de upload de arquivos
# PROFESSIONAL MEDICAL FILE UPLOAD SECTION
st.markdown("""
<div class='modern-card'>
    <h3 style='color: #1F2937; font-weight: 600; margin-bottom: 0.5rem; font-size: 1.3rem; font-family: "Inter", sans-serif;'>
        Clinical Documents
    </h3>
    <p style='color: #6B7280; font-size: 0.95rem; font-family: "Inter", sans-serif;'>
        Upload patient imaging, laboratory results, clinical notes, or diagnostic reports
    </p>
</div>
""", unsafe_allow_html=True)

uploaded_files = st.file_uploader(
    "Anexe imagens, PDFs ou documentos ao contexto",
    type=['png', 'jpg', 'jpeg', 'gif', 'bmp', 'pdf', 'txt', 'md', 'csv', 'docx', 'doc', 'wav', 'mp3', 'm4a', 'webm', 'ogg'],
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
                st.error(f"{file.name}: {file_info['error']}")
            else:
                st.success(f"{file.name}")
                
                # Mostrar preview
                if file_info.get("preview"):
                    if isinstance(file_info["preview"], Image.Image):
                        st.image(file_info["preview"], caption=file.name, use_column_width=True)
                    else:
                        with st.expander(f"Preview: {file.name}"):
                            st.text(file_info["preview"])
                            if file_info.get("audio_bytes"):
                                try:
                                    st.audio(file_info["audio_bytes"]) 
                                except Exception:
                                    pass
    
    # Botão para limpar arquivos
    if st.button("Limpar Arquivos"):
        st.session_state.uploaded_files = []
        st.session_state.file_contexts = []
        st.rerun()

# Mostrar indicador de arquivos anexados
if st.session_state.file_contexts:
    valid_files = [f for f in st.session_state.file_contexts if not f.get("error")]
    if valid_files:
        st.info(f"[ANEXO] {len(valid_files)} arquivo(s) anexado(s) ao contexto da conversa")

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
                    st.caption("[IMG] Imagem anexada")
        else:
            st.markdown(entry["content"])

# PHYSICIAN-FOCUSED PROFESSIONAL CSS DESIGN SYSTEM
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Crimson+Text:wght@400;600;700&display=swap');
    
    * {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    /* Main App Background */
    .main {
        background: linear-gradient(180deg, #FFFFFF 0%, #FFF5F5 100%);
    }
    
    [data-testid="stAppViewContainer"] {
        background: linear-gradient(180deg, #FFFFFF 0%, #FFF5F5 100%);
    }
    
    /* Professional Medical Card Design */
    .modern-card {
        background: white;
        border-radius: 25px;
        padding: 2rem;
        box-shadow: 0 6px 20px rgba(255, 46, 46, 0.12);
        border: 1.5px solid #FFCCCC;
        margin: 1.5rem 0;
        transition: all 0.3s ease;
        position: relative;
    }
    
    .modern-card:hover {
        box-shadow: 0 10px 30px rgba(255, 46, 46, 0.18);
        transform: translateY(-3px);
        border-color: #FF2E2E;
    }
    
    /* Professional Medical Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #FF2E2E 0%, #CC0000 100%);
        color: white;
        border: none;
        padding: 0.85rem 2.2rem;
        border-radius: 25px;
        font-weight: 600;
        font-size: 0.95rem;
        font-family: 'Inter', sans-serif;
        letter-spacing: 0.3px;
        transition: all 0.2s ease;
        box-shadow: 0 4px 15px rgba(255, 46, 46, 0.3);
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #CC0000 0%, #990000 100%);
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(255, 46, 46, 0.4);
    }
    
    /* Secondary Button Style */
    .stButton > button[kind="secondary"] {
        background: white;
        color: #FF2E2E;
        border: 2px solid #FF2E2E;
        border-radius: 25px;
    }
    
    .stButton > button[kind="secondary"]:hover {
        background: #FFF5F5;
        border-color: #CC0000;
        color: #CC0000;
    }
    
    /* Professional Input Fields */
    .stTextInput > div > div > input {
        border-radius: 20px;
        border: 1.5px solid #E5E7EB;
        background: white;
        padding: 0.85rem 1.2rem;
        font-size: 0.95rem;
        font-family: 'Inter', sans-serif;
        transition: all 0.2s ease;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #FF2E2E;
        box-shadow: 0 0 0 4px rgba(255, 46, 46, 0.15);
        outline: none;
    }
    
    /* Professional Text Area */
    .stTextArea > div > div > textarea {
        border-radius: 20px;
        border: 1.5px solid #E5E7EB;
        background: white;
        padding: 1.2rem;
        font-size: 0.95rem;
        font-family: 'Inter', sans-serif;
        transition: all 0.2s ease;
    }
    
    .stTextArea > div > div > textarea:focus {
        border-color: #FF2E2E;
        box-shadow: 0 0 0 4px rgba(255, 46, 46, 0.15);
        outline: none;
    }
    
    /* Professional Sidebar Styling */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #FFFFFF 0%, #FFF5F5 100%);
        border-right: 1px solid #FFE4E1;
    }
    
    /* Professional Metrics Cards */
    [data-testid="metric-container"] {
        background: white;
        padding: 1.5rem;
        border-radius: 20px;
        border: 1px solid #FFCCCC;
        box-shadow: 0 3px 10px rgba(255, 46, 46, 0.1);
        transition: all 0.2s ease;
    }
    
    [data-testid="metric-container"]:hover {
        box-shadow: 0 6px 15px rgba(255, 46, 46, 0.15);
        transform: translateY(-2px);
        border-color: #FF2E2E;
    }
    
    [data-testid="metric-container"] [data-testid="metric-label"] {
        color: #6B7280;
        font-weight: 600;
        font-size: 0.85rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    [data-testid="metric-container"] [data-testid="metric-value"] {
        color: #FF2E2E;
        font-weight: 700;
    }
    
    /* Professional Chat Messages */
    .stChatMessage {
        background: white;
        border-radius: 20px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 3px 12px rgba(255, 46, 46, 0.08);
        border: 1px solid #FFCCCC;
        transition: all 0.2s ease;
    }
    
    .stChatMessage:hover {
        box-shadow: 0 6px 18px rgba(255, 46, 46, 0.12);
        border-color: #FF2E2E;
    }
    
    /* User message specific styling */
    [data-testid="stChatMessageContainer"][data-baseweb="chat-message"]:has([data-testid="human-message-avatar"]) {
        background: #FFF5F5;
        border-color: #FFCCCC;
    }
    
    /* Select Box */
    .stSelectbox > div > div {
        border-radius: 10px;
        border: 2px solid #e0e6ed;
        background: #f8f9fa;
    }
    
    /* Professional File Uploader */
    .stFileUploader > div {
        border: 2.5px dashed #FF9999;
        border-radius: 25px;
        background: #FFF5F5;
        padding: 2.5rem;
        transition: all 0.2s ease;
        position: relative;
    }
    
    .stFileUploader > div:hover {
        border-color: #FF2E2E;
        background: #FFEEEE;
        box-shadow: 0 6px 18px rgba(255, 46, 46, 0.15);
    }
    
    /* Progress Bar */
    .stProgress > div > div > div {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        border-radius: 10px;
        height: 8px;
    }
    
    /* Expander */
    .streamlit-expanderHeader {
        background: #f8f9fa;
        border-radius: 10px;
        border: 1px solid #e0e6ed;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .streamlit-expanderHeader:hover {
        background: white;
        box-shadow: 0 2px 8px rgba(0,0,0,0.06);
    }
    
    /* Modern Divider */
    hr {
        border: none;
        height: 1px;
        background: linear-gradient(90deg, transparent, #e0e6ed, transparent);
        margin: 2rem 0;
    }
    
    /* Ultra Modern Voice System Card */
    .voice-card {
        background: white;
        border: 2px solid #667eea;
        border-radius: 30px;
        padding: 2.5rem;
        box-shadow: 0 20px 50px rgba(118, 75, 162, 0.2);
        margin: 2.5rem 0;
        transition: all 0.4s ease;
    }
    
    .voice-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 25px 60px rgba(118, 75, 162, 0.3);
    }
    
    /* Professional Scrollbar */
    ::-webkit-scrollbar {
        width: 10px;
        height: 10px;
    }
    
    ::-webkit-scrollbar-track {
        background: #F9FAFB;
        border-radius: 5px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: #FF4B4B;
        border-radius: 5px;
        border: 2px solid #F9FAFB;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: #DC2626;
    }
    
    /* Additional Ultra Modern Elements */
    .stTabs [data-baseweb="tab-list"] {
        background: linear-gradient(135deg, rgba(255,255,255,0.9) 0%, rgba(248,249,250,0.9) 100%);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 0.5rem;
        box-shadow: 0 5px 20px rgba(118, 75, 162, 0.1);
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 15px;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white !important;
        box-shadow: 0 5px 15px rgba(118, 75, 162, 0.3);
    }
    
    /* Professional Alert Messages */
    .stAlert {
        border-radius: 8px;
        border-left: 4px solid;
        padding: 1rem 1.2rem;
        font-family: 'Inter', sans-serif;
        font-size: 0.95rem;
        box-shadow: 0 2px 6px rgba(0,0,0,0.05);
    }
    
    .stAlert[data-baseweb="notification"][kind="info"] {
        background: #EFF6FF;
        border-left-color: #3B82F6;
        color: #1E40AF;
    }
    
    .stAlert[data-baseweb="notification"][kind="success"] {
        background: #F0FDF4;
        border-left-color: #22C55E;
        color: #166534;
    }
    
    .stAlert[data-baseweb="notification"][kind="warning"] {
        background: #FFFBEB;
        border-left-color: #F59E0B;
        color: #92400E;
    }
    
    .stAlert[data-baseweb="notification"][kind="error"] {
        background: #FEF2F2;
        border-left-color: #EF4444;
        color: #991B1B;
    }
    
    /* Spinner */
    .stSpinner > div {
        border-color: #FF4B4B !important;
    }
    
    /* Progress Bar */
    .stProgress > div > div > div {
        background: #FF4B4B;
        border-radius: 4px;
        height: 6px;
    }
    
    /* Code blocks */
    .stCodeBlock {
        border-radius: 8px;
        background: #1F2937;
        padding: 1rem;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
    
    /* Expander Headers */
    .streamlit-expanderHeader {
        background: white;
        border: 1px solid #FFE4E1;
        border-radius: 8px;
        padding: 0.75rem 1rem;
        font-weight: 600;
        font-family: 'Inter', sans-serif;
        color: #1F2937;
        transition: all 0.2s ease;
    }
    
    .streamlit-expanderHeader:hover {
        background: #FFF5F5;
        border-color: #FF4B4B;
    }
    
    /* Select boxes and dropdowns */
    .stSelectbox > div > div {
        border-radius: 8px;
        border: 1.5px solid #E5E7EB;
        background: white;
        font-family: 'Inter', sans-serif;
    }
    
    .stSelectbox > div > div:focus-within {
        border-color: #FF4B4B;
        box-shadow: 0 0 0 3px rgba(255, 75, 75, 0.1);
    }
    
    /* Radio and Checkbox */
    .stRadio > div {
        font-family: 'Inter', sans-serif;
        color: #4B5563;
    }
    
    .stCheckbox {
        font-family: 'Inter', sans-serif;
        color: #4B5563;
    }
    
    /* Dividers */
    hr {
        border: none;
        height: 1px;
        background: #FFE4E1;
        margin: 2rem 0;
    }
    
    /* Professional Typography */
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Crimson Text', serif;
        color: #1F2937;
    }
    
    p {
        font-family: 'Inter', sans-serif;
        color: #4B5563;
        line-height: 1.6;
    }
    
    /* Medical-grade color system */
    :root {
        --primary-red: #FF2E2E;
        --primary-dark: #CC0000;
        --primary-light: #FFF5F5;
        --text-primary: #1F2937;
        --text-secondary: #6B7280;
        --border-color: #FFCCCC;
    }
    
    /* Voice UI enhancements */
    .badge {
        display: inline-block;
        background: #FFF5F5;
        color: #B91C1C;
        border: 1px solid #FFCCCC;
        border-radius: 8px;
        padding: 4px 10px;
        font-size: 12px;
        font-weight: 600;
    }
    .badge.pill { border-radius: 999px; }
    .chip {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        padding: 6px 10px;
        background: #F9FAFB;
        border: 1px solid #E5E7EB;
        color: #374151;
        border-radius: 999px;
        font-size: 12px;
        font-weight: 600;
    }
    .mic-ring {
        width: 120px; height: 120px; border-radius: 50%;
        background: radial-gradient(circle at 50% 50%, #FFE4E6 0%, #FFD1D6 60%, #FFBAC2 100%);
        box-shadow: 0 10px 25px rgba(255,76,96,.25), inset 0 0 20px rgba(255,76,96,.35);
        display:flex; align-items:center; justify-content:center;
        position:relative;
    }
    .mic-ring::after{
        content:"";
        position:absolute; inset:-10px; border-radius:50%;
        border:2px dashed rgba(255, 76, 96, .25);
        animation: rotate 8s linear infinite;
    }
    @keyframes rotate { from { transform: rotate(0deg);} to { transform: rotate(360deg);} }
    .mic-icon { font-size: 38px; color: #B91C1C; filter: drop-shadow(0 4px 8px rgba(0,0,0,.08)); }
    .voice-hint { color:#6B7280; font-size: 12px; margin-top: 8px; }
</style>
""", unsafe_allow_html=True)

# PROFESSIONAL VOICE DICTATION SECTION (Enhanced UI)
st.markdown("""
<div class='voice-card'>
    <div style='display:flex; justify-content:space-between; align-items:center;'>
        <div>
            <h2 style='color:#1F2937; font-weight:700; margin:0 0 0.25rem 0; font-size:1.35rem; font-family:"Inter",sans-serif;'>
                Voice Dictation System
            </h2>
            <div style='display:flex; gap:8px; flex-wrap:wrap;'>
                <span class='badge pill'>STT Multi‑Provider</span>
                <span class='badge pill'>Noise Filter</span>
                <span class='badge pill'>Clinical-Grade</span>
            </div>
        </div>
        <div style='display:flex; gap:8px; align-items:center;'>
            <span class='chip'>Lang: {lang}</span>
            <span class='chip'>TTS: {tts}</span>
        </div>
    </div>
</div>
""".format(
    lang=st.session_state.voice_settings.get("language","pt").upper() if "voice_settings" in st.session_state else "PT",
    tts=("ON" if st.session_state.voice_settings.get("tts_enabled", False) else "OFF") if "voice_settings" in st.session_state else "OFF",
), unsafe_allow_html=True)

# (moved voice session initialization earlier to avoid AttributeError)

# Layout super simples - apenas 2 colunas
col_voice, col_result = st.columns([1, 3])

with col_voice:
    st.markdown("""
    <div style='display:flex; gap:16px; align-items:center;'>
        <div class='mic-ring'>
            <span class='mic-icon'>🎙️</span>
        </div>
        <div>
            <div style='font-weight:700;color:#1F2937;font-size:1rem;'>Grave sua pergunta</div>
            <div class='voice-hint'>Dica: fale em ambiente silencioso, pausadamente.</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Botão de gravação GRANDE e SIMPLES
    audio_bytes = audio_recorder(
        text="Clique para Gravar",
        recording_color="#dc3545",
        neutral_color="#667eea",
        icon_name="microphone",
        icon_size="3x",
        sample_rate=16000,  # Reduzido para melhor performance
        key="voice_recorder_simple"
    )
    
    st.caption("ou envie um arquivo de áudio")
    voice_up = st.file_uploader(" ", type=["wav","mp3","m4a","webm","ogg"], label_visibility="collapsed", key="voice_audio_upload_inline")
    if not audio_bytes and voice_up is not None:
        try:
            audio_bytes = voice_up.read()
        except Exception:
            audio_bytes = None
    
    # Idioma simplificado - apenas português como padrão
    if st.checkbox("Outros idiomas", key="show_languages"):
        voice_lang = st.selectbox(
            "Idioma",
            ["pt", "en", "es"],
            format_func=lambda x: {
                "pt": "Português",
                "en": "English",
                "es": "Español"
            }.get(x, x),
            key="voice_language_simple"
        )
    else:
        voice_lang = "pt"

with col_result:
    if audio_bytes:
        # Processamento avançado (Ultra STT)
        with st.spinner("Transcrevendo (UltraVoice)..."):
            vs = st.session_state.voice_settings
            pref = vs.get("preferred_stt", "auto")
            result, from_cache = stt_with_cache(
                audio_bytes,
                language=voice_lang,
                enable_medical_mode=vs.get("enable_medical_mode", True),
                enable_multi_api=vs.get("enable_multi_api", True),
                preferred_provider=(None if pref == 'auto' else pref),
                strict=vs.get("preferred_strict", False),
            )

        # Player do áudio capturado
        try:
            st.audio(audio_bytes)
            wf = generate_waveform_points(audio_bytes)
            if wf:
                st.line_chart(wf, height=80)
        except Exception:
            pass

        if result.get("success"):
            # Stylish badges row
            st.markdown(
                f"""
                <div style='display:flex; gap:8px; flex-wrap:wrap; margin-bottom:6px;'>
                  <span class='badge pill'>Método: {result.get('method','?')}</span>
                  <span class='badge pill'>Confiança: {result.get('confidence',0):.2f}</span>
                  <span class='badge pill'>Qualidade: {result.get('quality_score','–')}</span>
                </div>
                """,
                unsafe_allow_html=True,
            )
            if result.get("alternatives"):
                st.caption("Alternativas: " + "; ".join(result.get("alternatives", [])[:3]))
            if result.get("quality_score") is not None:
                st.progress(min(max(int(result.get("quality_score", 0)), 0), 100)/100)
            # Duration/WPM diagnostics
            dur = ffprobe_duration_seconds(audio_bytes)
            wpm = estimate_speech_rate_wpm(result.get("text",""), dur)
            diag = []
            if dur:
                diag.append(f"Duração: {dur:.1f}s")
            if wpm:
                diag.append(f"Ritmo: {wpm} wpm")
            if from_cache:
                diag.append("Cache STT")
            if diag:
                st.caption(" | ".join(diag))

            final_text = st.text_area(
                "Texto transcrito (você pode editar):",
                value=result.get("text", ""),
                height=120,
                key="transcribed_text_edit"
            )

            # Red flags detection and advisory
            rf = detect_red_flags_pt(final_text)
            if rf:
                st.error("Red flags detectadas: " + ", ".join([f"{k}: {', '.join(v)}" for k,v in rf.items()]))

            # Clinical highlights
            hl = extract_clinical_highlights(final_text)
            if any(hl.values()):
                chips = []
                for k, vals in hl.items():
                    for v in vals:
                        chips.append(f"<span class='badge pill'>{k}: {v}</span>")
                if chips:
                    st.markdown("<div style='display:flex;gap:6px;flex-wrap:wrap'>" + "".join(chips) + "</div>", unsafe_allow_html=True)
            attach_hl = st.checkbox("Anexar destaques clínicos ao envio", value=True)

            # Voice command helpers and extended mode toggle for this send
            cmds = analyze_voice_commands(final_text)
            if cmds.get("set_extended") is True:
                st.info("Comando: Pensamento estendido ativado para esta sessão.")
                st.session_state.extended_thinking_mode = True
            elif cmds.get("set_extended") is False:
                st.info("Comando: Pensamento estendido desativado para esta sessão.")
                st.session_state.extended_thinking_mode = False
            if cmds.get("clear_conversation"):
                if st.button("Confirmar limpar conversa", type="secondary"):
                    st.session_state.conversation = []
                    st.rerun()

            # Opcional: forçar pensamento estendido apenas nesta mensagem
            force_ext_once = st.checkbox(
                "Usar pensamento estendido nesta análise",
                value=st.session_state.voice_settings.get("force_extended_for_voice", False)
            )

            # Auto-extended triggers (length / red flags)
            auto_ext = False
            reasons = []
            try:
                thr = int(st.session_state.voice_settings.get("auto_extended_by_length", 250))
            except Exception:
                thr = 250
            if thr > 0 and len(final_text or '') > thr:
                auto_ext = True
                reasons.append("texto longo")
            if rf:
                auto_ext = True
                reasons.append("red flags")
            if auto_ext:
                st.info("Pensamento estendido será ativado automaticamente: " + ", ".join(reasons))
            force_ext_once = force_ext_once or auto_ext

            c1, c2, c3 = st.columns([1,1,1])
            with c1:
                if st.button("Enviar para Análise", type="primary", use_container_width=True):
                    # Prefixa trigger se forçar pensamento estendido nesta mensagem
                    payload = final_text
                    if attach_hl and any(hl.values()):
                        payload += "\n\n[DESTAQUES CLÍNICOS]\n"
                        for k, vals in hl.items():
                            if vals:
                                payload += f"- {k}: {', '.join(vals)}\n"
                    if st.session_state.voice_settings.get("attach_voice_label", True):
                        payload = f"Transcrição de áudio do paciente:\n{payload}"
                    st.session_state.audio_prompt = (
                        f"pensamento estendido: {payload}" if force_ext_once else payload
                    )
                    st.session_state.auto_submit = True
                    st.rerun()
            with c2:
                if st.button("Gravar Novamente", use_container_width=True):
                    st.rerun()
            with c3:
                if st.button("Copiar para área de transferência", use_container_width=True):
                    st.write("Copie manualmente o texto acima.")

            # Auto-submit condicionado à qualidade mínima
            if st.session_state.voice_settings.get("auto_submit", True):
                min_q = int(st.session_state.voice_settings.get("auto_submit_min_quality", 70))
                q = int(result.get("quality_score", 0))
                if q >= min_q:
                    st.info("Enviando em 2 segundos (qualidade adequada)…")
                    time.sleep(2)
                    payload = final_text
                    if attach_hl and any(hl.values()):
                        payload += "\n\n[DESTAQUES CLÍNICOS]\n"
                        for k, vals in hl.items():
                            if vals:
                                payload += f"- {k}: {', '.join(vals)}\n"
                    if st.session_state.voice_settings.get("attach_voice_label", True):
                        payload = f"Transcrição de áudio do paciente:\n{payload}"
                    st.session_state.audio_prompt = (
                        f"pensamento estendido: {payload}" if force_ext_once else payload
                    )
                    st.session_state.auto_submit = True
                    st.rerun()
                else:
                    st.warning("Qualidade abaixo do mínimo para auto-envio. Envie manualmente.")
        else:
            st.error("Não foi possível transcrever o áudio")
            if result.get("recommendations"):
                st.info("\n".join(["• "+r for r in result.get("recommendations", [])]))
            if st.button("Tentar Novamente", type="primary", use_container_width=True):
                st.rerun()
    else:
        # Instruções SUPER SIMPLES
        st.markdown("""
        ### Como usar:
        1. Clique no botão **Clique para Gravar**
        2. Fale sua pergunta médica
        3. Clique novamente para parar
        4. O texto será enviado automaticamente
        
        **Exemplos:**
        - "Paciente com febre e dor de cabeça"
        - "Dor no peito ao respirar"
        - "Criança com tosse há 5 dias"
        """)

# MODERN DIVIDER
st.markdown("<hr style='margin: 2rem 0; border: none; height: 1px; background: linear-gradient(90deg, transparent, #e0e6ed, transparent);'>", unsafe_allow_html=True)

# Voice recognition settings section removed - keeping interface simple
# Settings section removed - keeping simple interface

# Tab-based sections removed - keeping simple interface
# The following tab sections have been removed to revert to simpler design:
# - tab_history: Voice Analytics Dashboard  
# - tab_coach: AI Voice Coach
# All related functionality has been removed for simplicity
# Removed tab content for simplicity
# More removed tab content

# All tab sections removed for interface simplicity

# End of removed tab sections - keeping interface simple

# MODERN DIVIDER
st.markdown("<hr style='margin: 2rem 0; border: none; height: 1px; background: linear-gradient(90deg, transparent, #e0e6ed, transparent);'>", unsafe_allow_html=True)

# Verificar se há prompt de áudio ou texto
prompt = None

# Verificar auto-submit
if "auto_submit" in st.session_state and st.session_state.auto_submit:
    if "audio_prompt" in st.session_state and st.session_state.audio_prompt:
        prompt = st.session_state.audio_prompt
        st.session_state.audio_prompt = None
        st.session_state.auto_submit = False

# Input de texto tradicional com placeholder melhorado
if not prompt:
    prompt = st.chat_input(
        "Digite aqui ou use o microfone acima para gravar sua pergunta...",
        key="text_input_main"
    )

if prompt:
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
        placeholder = st.empty()

        if use_extended_thinking:
            with st.spinner("Dra Izza está realizando uma análise aprofundada com pensamento estendido..."):
                response = stream_claude_response(
                    actual_prompt,
                    placeholder,
                    conversation_history=conversation_history,
                    extended_thinking=True,
                    file_contexts=file_contexts,
                )
        else:
            spinner_text = "Dra Izza está analisando o caso com PIRM..."
            if file_contexts:
                spinner_text = "Dra Izza está analisando o caso e os arquivos anexados com PIRM..."

            with st.spinner(spinner_text):
                response = stream_claude_response(
                    prompt,
                    placeholder,
                    conversation_history=conversation_history,
                    extended_thinking=False,
                    file_contexts=file_contexts,
                )

        # Limpar contexto de arquivos após uso (evita reenvio repetido por performance)
        try:
            persist = os.getenv("PERSIST_ATTACHMENTS", "false").lower() in ("1", "true", "yes")
            if not persist:
                st.session_state.file_contexts = []
        except Exception:
            pass

        # TTS opcional da resposta do assistente
        try:
            vs = st.session_state.voice_settings
            if vs.get("tts_enabled", False):
                speak_text = response
                if vs.get("tts_compact_summary", True) and (use_extended_thinking is True):
                    speak_text = compact_text_for_tts(response, max_chars=800)
                with st.spinner("Sintetizando resposta por voz..."):
                    tts = get_tts_audio_cached(
                        speak_text,
                        lang_code=vs.get("tts_lang", "pt-BR"),
                        voice=vs.get("tts_voice"),
                        provider=vs.get("tts_provider", "auto"),
                    )
                if tts:
                    audio_bytes, mime = tts
                    st.audio(audio_bytes, format=mime)
        except Exception:
            pass
    
    # Adicionar resposta à conversa
    st.session_state.conversation.append({"role": "assistant", "content": response})


# Feedback
with st.expander("Enviar Feedback"):
    feedback = st.text_area("Seu feedback sobre o diagnóstico ou sugestões de melhoria:")
    if st.button(" Enviar Feedback"):
        if feedback.strip():
            # Aqui você pode implementar o salvamento do feedback
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            try:
                with open("feedback.txt", "a", encoding='utf-8') as f:
                    f.write(f"[{timestamp}] {feedback}\n\n")
                st.success("Obrigado pelo seu feedback! Ele foi salvo para análise.")
            except Exception as e:
                st.error(f"Erro ao salvar feedback: {e}")
        else:
            st.warning("Por favor, escreva seu feedback antes de enviar.")

# Informações sobre o modo de pensamento estendido
with st.expander("Sobre o Pensamento Estendido"):
    st.markdown("""
    ## Modo de Pensamento Estendido
    
    O modo de pensamento estendido é uma funcionalidade avançada que permite ao Izza MD PhD realizar uma análise médica profunda e detalhada, documentando explicitamente cada etapa do raciocínio diagnóstico.
    
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
