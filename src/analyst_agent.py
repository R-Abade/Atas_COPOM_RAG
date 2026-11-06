class AnalystAgent:

    def __init__(self, llm: BaseLLM, tool: RagTools, memory: ShortTermMemory):
        self.llm = llm
        self.tool = tool
        self.memory = memory
        self.system_prompt = """Você é um Analista de Política Monetária.
        Recebe dados brutos do Pesquisador e deve:
        1. Identificar tendências da taxa de juros(ex: 'o tom hawkish está suavizando')
        2. Comparar decisões entre reuniões
        3. Detectar inconsistências ou mudanças de retórica
        4. Analisar se há sinais de mudança na política monetária
        5. Analisar se houve decisão unânime entre os membros do copom
        6. Sintetize uma resposta final com base nas análises feitas
        Use a ferramenta compare_minutes quando necessário."""
    
    def run(self, research_data: str, user_question: str) -> str:
        prompt = f"""{self.system_prompt}

        Dados coletados pelo Pesquisador:
        {research_data}

        Pergunta original do usuário: {user_question}

        Produza sua análise com base nos dados acima."""

        response = self.llm.generate([{"role": "user", "content": prompt}])
        self.memory.add(f"Analyst: {response}", agent="analyst", importance=0.8)
        return response