# app/services/crew_runner.py

from app.models import ArtigoOutput
from src.article_crew import ArticleCrew 
from crewai import Crew 


def run_article_crew(assunto: str) -> ArtigoOutput:
    """
    Instancia e executa a Crew de Geração de Artigos usando o padrão @CrewBase.
    
    Args:
        assunto: O tópico sobre o qual o artigo deve ser gerado.

    Returns:
        Um objeto ArtigoOutput estruturado com o resultado final.
    """
    
    # 1. Instancia a Crew definida na classe ArticleCrew
    # O método .crew() da classe ArticleCrew retorna o objeto Crew pronto para ser executado.
    article_crew_instance: Crew = ArticleCrew().crew()
    
    # 2. Define as entradas
    inputs = {
        'assunto': assunto
    }
    
    # 3. Executa a Crew
    # O kickoff executa todas as tarefas na ordem SEQUENTIAL.
    result = article_crew_instance.kickoff(inputs=inputs)
    
    # 4. O resultado final é o Pydantic Object da última Task
    return result.pydantic