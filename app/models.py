from pydantic import BaseModel, Field, validator
from typing import List

class ArtigoOutput(BaseModel):
    """
    Define a estrutura de output Pydantic para o artigo final.
    """

    titulo: str = Field(
        description="O título final do artigo, otimizado e envolvente."
    )
    
    conteudo: str = Field(
        description="O conteúdo completo do artigo, bem estruturado com Título, Introdução, Corpo e Conclusão. Deve ter no mínimo 300 palavras."
    )
    
    palavras_chave: List[str] = Field(
        description="Uma lista de 3 a 5 palavras-chave relevantes para o artigo."
    )
    
    # Exemplo de validador 
    @validator('conteudo', pre=True)
    def validate_word_count(cls, v):
        """
        Valida se o conteúdo tem no mínimo 300 palavras.
        """
        if isinstance(v, str):
            word_count = len(v.split())
            if word_count < 300:
                print(f"AVISO: O artigo gerado tem apenas {word_count} palavras. O requisito é 300.")
                
        return v