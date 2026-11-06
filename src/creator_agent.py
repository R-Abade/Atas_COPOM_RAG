class CreatorAgent:

    def __init__(self, llm: BaseLLM, memory: ShortTermMemory):
        self.llm = llm
        self.memory = memory
        self.system_prompt = """Você é um Redator Executivo.
        Transforme análises técnicas em textos claros para stakeholders.
        Estruture com: Resumo Executivo, Decisões-Chave, Riscos, Próximos Passos.
        Tente ser conciso e objetivo.
        Evite repetições e use linguagem técnica apropriada.
        Baseie-se APENAS nas informações fornecidas, sem inventar dados."""
    
    def run(self, analysis: str, format_type: str = "resumo") -> str:
        prompt = f"""{self.system_prompt}

        Análise recebida:
        {analysis}

        Formato solicitado: {format_type}

        Produza o texto final."""

        response = self.llm.generate([{"role": "user", "content": prompt}])
        self.memory.add(f"Creator: {response}", agent="creator", importance=0.6)
        return response
