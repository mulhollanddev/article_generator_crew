# app/main.py

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, constr # 1. Importa constr para validação
import sys
import os
import unicodedata # 2. Importa unicodedata para sanitização
import re # 3. Importa re para regex

from dotenv import load_dotenv
load_dotenv()

# Caminha um nível acima do 'app' para chegar na raiz do projeto
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Importações dos módulos do projeto
from app.models import ArtigoOutput
from app.services.crew_runner import run_article_crew

# Inicializa o aplicativo FastAPI
app = FastAPI(
    title="Gerador de Artigos CrewAI",
    description="API para automatizar a geração de artigos usando um sistema multiagente CrewAI.",
    version="1.0.0"
)

# -----------------------------------------------------------
# Constantes e Funções de Segurança
# -----------------------------------------------------------

MAX_ASSUNTO_LENGTH = 200 # Limite de caracteres para o assunto

# Mapeia caracteres de controle invisíveis para None (remoção)
control_chars = {c: None for c in range(sys.maxunicode + 1)
                 if unicodedata.category(chr(c)).startswith('C')}

def sanitize_input(text: str) -> str:
    """Remove caracteres de controle invisíveis e espaços extras."""
    return text.translate(control_chars).strip()

# Padrões regex (exemplos, podem ser expandidos)
INJECTION_PATTERNS = [
    re.compile(r"ignore .* previous instructions", re.IGNORECASE),
    re.compile(r"act as if|you are now", re.IGNORECASE),
    re.compile(r"forget everything", re.IGNORECASE),
    re.compile(r"important instruction:|new goal:|your instructions are", re.IGNORECASE),
    # Adicionar outros padrões se necessário
]

def detect_injection(text: str) -> bool:
    """Verifica se o texto contém padrões suspeitos de prompt injection."""
    for pattern in INJECTION_PATTERNS:
        if pattern.search(text):
            return True
    return False

# -----------------------------------------------------------
# Modelos da API (Com Validação de Tamanho)
# -----------------------------------------------------------

class ArtigoInput(BaseModel):
    """
    Define o modelo de entrada para a API (o tema do artigo).
    """
    # 4. Usa constr para limitar o tamanho do assunto
    assunto: constr(max_length=MAX_ASSUNTO_LENGTH) = Field( 
        ...,
        description=f"O tema do artigo (máx. {MAX_ASSUNTO_LENGTH} caracteres).",
        json_schema_extra={"example": "O impacto da Inteligência Artificial na educação."}
    )

# -----------------------------------------------------------
# Endpoint Principal da API (Com Validação e Sanitização)
# -----------------------------------------------------------

@app.post(
    "/gerar-artigo",
    response_model=ArtigoOutput,
    summary="Gera um artigo completo com base em um tema",
    description="Inicia o processo multiagente, validando e sanitizando a entrada."
)
async def gerar_artigo_endpoint(data: ArtigoInput):
    """
    Recebe um assunto, valida, sanitiza e retorna o artigo gerado.
    """
    # Pydantic já validou o tamanho máximo na entrada (data.assunto)

    # 5. Aplica a sanitização
    sanitized_assunto = sanitize_input(data.assunto)

    # Verifica se o assunto ficou vazio após sanitização
    if not sanitized_assunto:
        raise HTTPException(status_code=400, detail="Assunto inválido ou vazio após sanitização.")

    # 6. Detecta padrões de injeção
    if detect_injection(sanitized_assunto):
        # Logar a tentativa de injeção seria uma boa prática aqui
        print(f"WARN: Potencial Prompt Injection detectado: '{data.assunto}'")
        raise HTTPException(status_code=400, detail="Entrada suspeita detectada. Por favor, forneça apenas o tema do artigo.")

    # Se passou em todas as verificações, prossegue
    try:
        artigo_final: ArtigoOutput = run_article_crew(assunto=sanitized_assunto) # Usa o assunto sanitizado
        return artigo_final

    except Exception as e:
        print(f"Erro durante a execução da CrewAI: {e}")
        # Retorna o erro específico do LiteLLM/API se disponível
        error_detail = f"Falha na geração do artigo. Erro interno: {str(e)}"
        if "litellm.APIError" in str(e):
             error_detail = f"Falha na comunicação com o LLM: {str(e)}"

        raise HTTPException(
            status_code=500,
            detail=error_detail
        )

# -----------------------------------------------------------
# Endpoint de Teste (Health Check)
# -----------------------------------------------------------

@app.get("/")
def health_check():
    """Verifica se a API está online."""
    return {"status": "ok", "service": "CrewAI Article Generator"}