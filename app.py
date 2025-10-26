import streamlit as st
import requests
import json
from config import *
from app.models import ArtigoOutput


# --- Configuração da Página ---
st.set_page_config(
    page_title="Gerador de Artigos",
    layout="wide"
)

col_title, col_status = st.columns([10, 2])

with col_title:
    st.title("Sistema Multiagentes para Geração de Artigos")

# 1. Inicializa o Histórico de Conversa (State)
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "assistant", "content": "Olá! Digite o **tema** sobre o qual você gostaria de gerar um artigo."}
    ]

# ----------------------------------------------------
# NOVO: Função para chamar a API e obter o artigo
# ----------------------------------------------------
def get_article_from_api(topic: str) -> ArtigoOutput:
    """Chama o endpoint da API para executar o CrewAI e gerar o artigo."""
    
    # Prepara o payload para a API
    payload = {"assunto": topic}
    
    try:
        # Faz a requisição POST para sua API
        response = requests.post(API_URL, json=payload, timeout=300) # Aumentei o timeout
        response.raise_for_status() # Lança um erro para status 4xx/5xx
        
        # O retorno é um JSON que se encaixa no modelo ArtigoOutput
        article_data = response.json()
        
        # Valida e retorna o objeto Pydantic
        return ArtigoOutput(**article_data)
        
    except requests.exceptions.RequestException as e:
        st.error(f"Erro ao conectar ou receber resposta da API: {e}")
        return None
    except json.JSONDecodeError:
        st.error("Erro ao decodificar a resposta JSON da API. Verifique o formato de saída da sua API.")
        return None
    except Exception as e:
        st.error(f"Erro inesperado: {e}")
        return None


def format_article_output(article: ArtigoOutput) -> str:
    """Formata o objeto Pydantic em uma string Markdown amigável."""
    
    # Título do Artigo
    markdown_output = f"# {article.titulo}\n\n"
    
    # Conteúdo (Artigo)
    markdown_output += article.conteudo + "\n\n"
    
    # Palavras-chave
    markdown_output += "--- \n\n"
    markdown_output += "**Palavras-chave:** " + ", ".join(article.palavras_chave) + "\n\n"
    
    # Metadados de Contagem (Opcional, mas útil para verificação)
    word_count = len(article.conteudo.split())
    markdown_output += f"*(Contagem de Palavras: {word_count})*\n"
    
    return markdown_output

# 3. Exibe o Histórico de Conversa
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 4. Campo de Entrada de Texto
if prompt := st.chat_input(
    f"Envie seu tema (máx. {MAX_ASSUNTO_LENGTH} caracteres)..."
    ): # <-- Atualiza o placeholder
    
    # Adiciona a mensagem do usuário ao histórico
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Exibe a mensagem do usuário imediatamente
    with st.chat_message("user"):
        st.markdown(prompt)

    if len(prompt) > MAX_ASSUNTO_LENGTH:
        # Se o prompt for muito longo, exibe um aviso e NÃO chama a API
        warning_message = f"⚠️ O tema digitado é muito longo ({len(prompt)} caracteres). O máximo permitido é {MAX_ASSUNTO_LENGTH}. Por favor, envie um tema mais curto."
        with st.chat_message("assistant"):
            st.warning(warning_message) # Usa st.warning para destacar
        # Adiciona a mensagem de aviso ao histórico
        st.session_state.messages.append({"role": "assistant", "content": warning_message})

    else:
        # Gera e exibe a resposta do assistente
        with st.chat_message("assistant"):
            with st.spinner("Pesquisando, Redigindo e Formatando o Artigo..."):
                
                # CHAMA A FUNÇÃO CENTRAL DO PROJETO
                article_output = get_article_from_api(prompt)
                
                if article_output:
                    response = format_article_output(article_output)
                    st.markdown(response)
                    
                    # Adiciona a resposta do assistente ao histórico
                    st.session_state.messages.append({"role": "assistant", "content": response})
                else:
                    # Se falhou, adiciona a mensagem de erro que já foi exibida
                    error_message = "Desculpe, não consegui gerar o artigo devido a um erro na API."
                    st.markdown(error_message)
                    st.session_state.messages.append({"role": "assistant", "content": error_message})


# --- Barra Lateral (Sidebar) para Limpeza de conversa ---
with st.sidebar:
    st.header("Ferramentas")
    
    st.info("A pesquisa de contexto é feita *online* usando a Custom Tool da Wikipedia.")
    
    st.markdown("---")
    
    if st.button("Limpar Conversa"):
        st.session_state["messages"] = [
            {"role": "assistant", "content": "Conversa limpa. Faça uma nova pergunta."}
        ]
        st.rerun()