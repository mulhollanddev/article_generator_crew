from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
import sys
import os
from dotenv import load_dotenv
load_dotenv()


# Caminha um nível acima do 'app' para chegar na raiz do projeto
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Importações dos módulos do projeto
from app.models import ArtigoOutput # Modelo Pydantic de saída
from app.services.crew_runner import run_article_crew # Função de execução da Crew

# Inicializa o aplicativo FastAPI
app = FastAPI(
    title="Gerador de Artigos CrewAI",
    description="API para automatizar a geração de artigos usando um sistema multiagente CrewAI.",
    version="1.0.0"
)

# -----------------------------------------------------------
# Modelos da API
# -----------------------------------------------------------

class ArtigoInput(BaseModel):
    """
    Define o modelo de entrada para a API (o tema do artigo).
    """
    assunto: str = Field(
        ..., 
        description="O tema ou assunto principal sobre o qual o artigo deve ser gerado.",
        # LINHA CORRIGIDA
        json_schema_extra={"example": "O impacto da Inteligência Artificial na educação."}
    )

# -----------------------------------------------------------
# Endpoint Principal da API
# -----------------------------------------------------------

@app.post(
    "/gerar-artigo", 
    response_model=ArtigoOutput, # Garante que o output seja validado pelo Pydantic
    summary="Gera um artigo completo com base em um tema",
    description="Inicia o processo multiagente (Pesquisador e Escritor) para buscar informações na Wikipedia e redigir um artigo de no mínimo 300 palavras."
)

async def gerar_artigo_endpoint(data: ArtigoInput):
    """
    Recebe um assunto e retorna o artigo gerado pelo sistema CrewAI.
    """
    assunto = data.assunto.strip()
    
    if not assunto:
        raise HTTPException(status_code=400, detail="O campo 'assunto' não pode estar vazio.")

    try:
        # Chama a função de serviço que executa a CrewAI
        # Esta função retorna um objeto ArtigoOutput já validado
        artigo_final: ArtigoOutput = run_article_crew(assunto=assunto)
        
        # O FastAPI automaticamente serializa o objeto ArtigoOutput para JSON
        return artigo_final

    except Exception as e:
        # Captura e trata erros gerais durante a execução da Crew
        print(f"Erro durante a execução da CrewAI: {e}")
        raise HTTPException(
            status_code=500, 
            detail=f"Falha na geração do artigo. Erro interno: {str(e)}"
        )

# -----------------------------------------------------------
# Endpoint de Teste (Health Check)
# -----------------------------------------------------------

@app.get("/")
def health_check():
    """Verifica se a API está online."""
    return {"status": "ok", "service": "CrewAI Article Generator"}