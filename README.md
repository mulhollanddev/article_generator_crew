# 📄 Sistema Multiagentes para Geração de Artigos (SMUGAU)
Este projeto implementa um sistema multiagente utilizando o framework CrewAI para automatizar a criação de artigos para um website1. O sistema pesquisa informações contextuais na API da Wikipedia para obter contexto relevante 2e utiliza Large Language Models (LLMs) para redigir artigos estruturados e com no mínimo 300 palavras.
A interface é fornecida através de um servidor FastAPI e uma aplicação cliente Streamlit.

## ⚙️ Tecnologias UtilizadasComponenteTecnologiaFinalidadeOrquestraçãoCrewAI 4Framework para gerenciar a colaboração dos agentes5.AgentesPesquisador e EscritorO sistema contém dois ou mais agentes6.PesquisaCustom CrewAI Tool 77Tool customizada para consultar a API da Wikipedia88.LLMOpenRouter (ou Gemini/Groq)Modelo de linguagem grande para raciocínio e geração de conteúdo9.EstruturaPydanticValidação e formatação do output final da Crew10.API WebFastAPIServidor REST para execução do sistema11.FrontendStreamlitInterface de usuário (ChatBot).LinguagemPython 12Linguagem principal do projeto.

## 🚀 Estrutura do ProjetoO projeto segue a estrutura de pacotes recomendada (app/ para serviços de API, src/ para a lógica principal do sistema de agentes):SMUGAU/
├── app/
│   ├── main.py            # ➡️ Ponto de entrada da API (FastAPI)
│   ├── models.py          # Modelos Pydantic (Input/Output)
│   └── services/
│       └── crew_runner.py # Serviço que inicia a CrewAI
├── src/
│   ├── article_crew.py    # ➡️ Definição da Crew, Agentes e Tarefas (@CrewBase)
│   ├── tools/
│       └── wikipedia_tool.py # ➡️ Custom CrewAI Tool (BaseTool)
│   └── config/
│       ├── agents.yaml    # Configuração de Role/Goal dos Agentes
│       └── tasks.yaml     # Configuração das Tarefas
├── .env                   # Variáveis de Ambiente (API Keys)
├── app.py                 # ➡️ Aplicação Streamlit (Frontend)
└── requirements.txt       # Dependências

## 📋 Como Configurar e ExecutarSiga os passos abaixo para colocar o sistema em funcionamento.

1. Pré-requisitos
- Python 3.10+
- O projeto deve estar publicado no GitHub com repositório público
- 3.Chave de API do provedor LLM (Ex: OpenRouter API Key).

2. Configuração do Ambiente

2.1. Clone o repositório:
>> git clone 
>> cd SMUGAU

2.2. Crie e ative o ambiente virtual:
>> python -m venv .venv
>> source .venv/bin/activate  # No Windows use: .venv\Scripts\activate

2.3. Instale as dependências:
>> pip install -r requirements.txt

3. Configuração de Chaves de API
Crie um arquivo chamado .env na raiz do projeto (SMUGAU/.env) e insira suas chaves de API:

>> # Exemplo para OpenRouter
>> OPENROUTER_API_KEY="sk-seu-token-aqui"

>> # Chave de contorno (necessária para algumas versões do CrewAI)
>> OPENAI_API_KEY="sk-fakekeyforcrewai" 

4. Execução do Sistema
O sistema é dividido em duas partes que devem ser executadas em terminais separados: o Servidor API e a Interface Gráfica.

A. Iniciar o Servidor FastAPI (Backend)Abra o primeiro terminal na raiz do projeto (SMUGAU/) e inicie o servidor:
>> uvicorn app.main:app --reload
O servidor estará ativo em http://127.0.0.1:8000.

B. Iniciar a Interface Streamlit (Frontend)
Abra o segundo terminal na raiz do projeto (SMUGAU/) e inicie a interface:

>> streamlit run app.py

O Streamlit abrirá automaticamente a interface no seu navegador, pronta para receber o tema do artigo.
