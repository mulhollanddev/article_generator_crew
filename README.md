# 📄 Sistema Multiagentes para Geração de Artigos
Este projeto implementa um sistema multiagente utilizando o framework CrewAI para automatizar a criação de artigos para um website1. O sistema pesquisa informações contextuais na API da Wikipedia para obter contexto relevante 2e utiliza Large Language Models (LLMs) para redigir artigos estruturados e com no mínimo 300 palavras.
A interface é fornecida através de um servidor FastAPI e uma aplicação cliente Streamlit.

## ⚙️ Tecnologias Utilizadas
| **Componente** | **Tecnologia**              | **Finalidade**                                                   |
|----------------|-----------------------------|------------------------------------------------------------------|
| Orquestração   | CrewAI                      | Tool customizada para consultar a API da Wikipedia.              |
| Agentes        | Pesquisador e Escritor      | O sistema contém dois ou mais agentes                            |
| Pesquisa       | Custom CrewAI Tool          | Tool customizada para consultar a API da Wikipedia.              |
| LLM            | OpenRouter (ou Gemini/Groq) | Modelo de linguagem grande para raciocínio e geração de conteúdo |
| Estrutura      | Pydantic                    | Validação e formatação do output final da Crew                   |
| API Web        | FastAPI                     | Servidor REST para execução do sistema                           |
| Frontend       | Streamlit                   | Interface de usuário (ChatBot)                                   |
| Linguagem      | Python                      | Linguagem principal do projeto.                                  |

## 🚀 Estrutura do Projeto
O projeto segue a estrutura de pacotes recomendada (app/ para serviços de API, src/ para a lógica principal do sistema de agentes): article_generator_crew/
```text
article_generator_crew/
├── app/
│ ├── main.py # ➡️ Ponto de entrada da API (FastAPI)
│ ├── models.py # Modelos Pydantic (Input/Output)
│ └── services/
│ └── crew_runner.py # Serviço que inicia a CrewAI
├── src/
│ ├── article_crew.py # ➡️ Definição da Crew, Agentes e Tarefas (@CrewBase)
│ ├── tools/
│ └── wikipedia_tool.py # ➡️ Custom CrewAI Tool (BaseTool)
│ └── config/
│ ├── agents.yaml # Configuração de Role/Goal dos Agentes
│ └── tasks.yaml # Configuração das Tarefas
├── .env # Variáveis de Ambiente (API Keys)
├── app.py # ➡️ Aplicação Streamlit (Frontend)
└── requirements.txt # Dependências
```

## 📋 Como Configurar e Executar
Siga os passos abaixo para colocar o sistema em funcionamento.

### 1. Pré-requisitos
- Python 3.10+
- Chave de API do provedor LLM (Ex: OpenRouter).

### 2. Configuração do Ambiente

#### 2.1. Clone o repositório:
<pre><code class="language-bash">
$ git clone https://github.com/mulhollanddev/article_generator_crew.git
$ cd article_generator_crew
</code></pre>

#### 2.2. Crie e ative o ambiente virtual:
<pre><code class="language-bash">
$ python -m venv .venv
$ source .venv/bin/activate  # No Windows use: .venv\Scripts\activate
</code></pre>

#### 2.3. Instale as dependências:
<pre><code class="language-bash">
$ pip install -r requirements.txt
</code></pre>

### 3. Configuração de Chaves de API
Crie um arquivo chamado .env na raiz do projeto (article_generator_crew/.env) e insira suas chaves de API:

<pre><code class="language-bash">
$ # Exemplo para OpenRouter
$ OPENROUTER_API_KEY="sk-seu-token-aqui"
$ # Chave de contorno (necessária para algumas versões do CrewAI)
$ OPENAI_API_KEY="sk-fakekeyforcrewai" 
</code></pre>


### 4. Execução do Sistema
O sistema é dividido em duas partes que devem ser executadas em terminais separados: o Servidor API e a Interface Gráfica.

#### A. Iniciar o Servidor FastAPI (Backend)
Abra o primeiro terminal na raiz do projeto (article_generator_crew/) e inicie o servidor:
<pre><code class="language-bash">
$ uvicorn app.main:app --reload
</code></pre>
O servidor estará ativo em http://127.0.0.1:8000.

#### B. Iniciar a Interface Streamlit (Frontend)
Abra o segundo terminal na raiz do projeto (article_generator_crew/) e inicie a interface:

<pre><code class="language-bash">
$ streamlit run app.py
</code></pre>

O Streamlit abrirá automaticamente a interface no seu navegador, pronta para receber o tema do artigo.
