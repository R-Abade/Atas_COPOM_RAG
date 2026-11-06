class OrchestratorAgent:

    def __init__(self, llm: BaseLLM, researcher: ResearcherAgent, analyst: AnalystAgent, creator: CreatorAgent, memory: ShortTermMemory):
        self.llm = llm
        self.agents = {
            "researcher": researcher,
            "analyst": analyst,
            "creator": creator
        }
        self.memory = memory

    def classify_intent(self, user_input: str): # Utiliza LLM para definir intenção de usuário e qual fluxo se agentes seguir
        prompt = f"""Classifique a intenção: [FACTUAL] (busca dado específico), 
        [ANALISE] (comparação/tendência), [CRIACAO] (gerar documento/resumo).
        Pergunta: {user_input}
        Responda apenas: FACTUAL, ANALISE ou CRIACAO"""
        intent = self.llm.generate([{"role": "user", "content": prompt}]).strip()
        return intent


    def route(self, user_input: str):
        intent = self.classify_intent(user_input)

        if intent == "FACTUAL":
            response = self.agents["researcher"].run(user_input)
            return response

        elif intent == "ANALISE":
            response = self.agents["researcher"].run(user_input)
            return self.agents["analyst"].run(response, user_input)

        elif intent == "CRIACAO":
            response = self.agents["researcher"].run(user_input)
            analyst = self.agents["analyst"].run(response, user_input)
            return self.agents["creator"].run(analyst)



        