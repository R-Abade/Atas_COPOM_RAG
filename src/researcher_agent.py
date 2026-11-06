class ResearcherAgent:

    def __init__(self, llm: BaseLLM, tools: RagTools, memory: ShortTermMemory):
        sel.llm = llm
        self.tools = tools
        self.memory = memory
        self.system_prompt = """Você é um Pesquisador especializado em atas do Copom.
        Sua função é ENCONTRAR informações factuais. Não interprete, não analise.
        Sempre cite a fonte no formato [Ata Nº X, Seção Y, Parágrafo Z].
        Se não encontrar a informação, diga explicitamente 'Não localizado nas atas indexadas'."""


    def run(self, query: str) -> str:
        pass
