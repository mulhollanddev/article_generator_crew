# src/tools/wikipedia_tool.py

import requests
import json
from crewai.tools import BaseTool # Importação da classe base oficial
from pydantic import BaseModel, Field
from typing import Type
from config import *


# 1. Define o esquema de entrada (INPUT) da ferramenta usando Pydantic
class WikipediaSearchInput(BaseModel):
    """Esquema de entrada para a ferramenta de pesquisa da Wikipedia."""
    topic: str = Field(..., description="O termo exato de pesquisa (o assunto do artigo).")


# 2. Define a Custom Tool
class WikipediaSearchTool(BaseTool):
    """
    Ferramenta customizada para pesquisar e obter um extrato de artigo
    da API da Wikipedia em português.
    """
    name: str = "Pesquisador da Wikipedia"
    description: str = "Busca o contexto e o primeiro parágrafo de um artigo na Wikipedia sobre um tópico específico."
    
    # Define o esquema de entrada obrigatório para o LLM
    args_schema: Type[BaseModel] = WikipediaSearchInput

    def _run(self, topic: str) -> str:
        """
        Executa a pesquisa na API da Wikipedia.
        
        Args:
            topic: O termo de pesquisa (fornecido pelo LLM via args_schema).
            
        Returns:
            O extrato (resumo) do artigo da Wikipedia.
        """
        
        # Parâmetros de requisição
        params = {
            "action": "query",
            "prop": "extracts",
            "exlimit": "1",
            "explaintext": "1",
            "titles": topic,
            "format": "json",
            "utf8": "1",
            "redirects": "1"
        }
        
        try:
            response = requests.get(WIKIPEDIA_API_URL, params=params)
            response.raise_for_status() 
            data = response.json()
            
            pages = data['query']['pages']
            page_id = next(iter(pages))
            extract = pages[page_id].get('extract', 'Nenhuma informação relevante encontrada na Wikipedia.')
            
            if "may refer to:" in extract or "redirect" in extract.lower():
                return f"Pesquisa ambígua. Tente um termo mais específico para '{topic}'."
            
            return f"Pesquisa: {topic}\n\nContexto da Wikipedia:\n{extract}"

        except requests.exceptions.RequestException as e:
            return f"Erro ao consultar a API da Wikipedia: {e}"
        except Exception as e:
            return f"Erro ao processar o resultado da Wikipedia: {e}"

# Cria e exporta a instância da ferramenta
WikipediaSearchTool_Instance = WikipediaSearchTool()