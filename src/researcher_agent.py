class ResearcherAgent:

    def __init__(self, llm: BaseLLM, tools: RagTools, memory: ShortTermMemory):
        self.llm = llm
        self.tools = tools
        self.memory = memory
        self.system_prompt = """Você é um Pesquisador especializado em atas do Copom.
        Sua função é ENCONTRAR informações factuais. Não interprete, não analise.
        Sempre cite a fonte no formato [Ata Nº X, Seção Y, Parágrafo Z].
        Se não encontrar a informação, diga explicitamente 'Não localizado nas atas indexadas'."""


    def run(self, query: str) -> str: # Busca chunks relevantes no vector store
        search_results = self.tools.search_atas(query)

        prompt = f"""{self.system_prompt}

        Contexto encontrado nas atas:
        {search_results}

        Pergunta: {query}

        Responda com base apenas no contexto acima. Cite a fonte quando possível."""

        response = self.llm.generate([{"role": "user", "content": prompt}])
        self.memory.add(f"Researcher: {response}", agent="researcher", importance=0.7)
        return response
