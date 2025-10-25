from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
from src.tools.wikipedia_tool import WikipediaSearchTool_Instance
from app.models import ArtigoOutput
from config import OPENROUTER_MODEL, OPENROUTER_URL


llm = LLM(
    model=OPENROUTER_MODEL,
    base_url=OPENROUTER_URL,
    temperature=0.5,
)

@CrewBase
class ArticleCrew:
    # Arquivos YAML de configuração
    agents_config = "agents.yaml"
    tasks_config = "tasks.yaml"

    @agent
    def pesquisador(self) -> Agent:
        return Agent(
            config=self.agents_config["pesquisador"], 
            verbose=True, 
            tools=[WikipediaSearchTool_Instance], # Agente Pesquisador usa a Custom Tool
            llm=llm,
        )
    
    @agent
    def escritor(self) -> Agent:
        return Agent(
            config=self.agents_config["escritor"], 
            verbose=True, 
            tools=[],
            llm=llm,
        )

    @task
    def pesquisar_contexto(self) -> Task:
        return Task(
            config=self.tasks_config["pesquisar_contexto"],
            agent=self.pesquisador(),
        )
    
    @task
    def redigir_artigo_final(self) -> Task:
        # A Tarefa do Escritor PRECISA do Output Pydantic
        return Task(
            config=self.tasks_config["redigir_artigo_final"],
            agent=self.escritor(),
            output_pydantic=ArtigoOutput, # Define o formato de saída estruturado
            context=[self.pesquisar_contexto()], # Define o contexto (output da tarefa de pesquisa)
        )
    
    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=[self.pesquisador(), self.escritor()],
            tasks=[
                self.pesquisar_contexto(),
                self.redigir_artigo_final(),
            ],
            process=Process.sequential, 
            verbose=True, 
        )