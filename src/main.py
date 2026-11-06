def main():
    # Setup
    llm_orchestrator = GeminiLLM(api_key=os.getenv("API_KEY"))
    llm_specialist = OllamaLLM(model="qwen2.5:3b")
    
    memory = ShortTermMemory(max_items=30)
    tools = RAGTools(vector_db, embedding_model)
    
    # Agentes
    researcher = ResearcherAgent(llm_specialist, tools, memory)
    analyst = AnalystAgent(llm_specialist, tools, memory)
    creator = CreatorAgent(llm_orchestrator, memory)  
    
    orchestrator = OrchestratorAgent(llm_orchestrator, researcher, analyst, creator, memory)
    
    # Interface
    while True:
        question = input("\nPergunta: ")
        if question.lower() == 'sair':
            break
        
        response = orchestrator.route(question)
        print(f"\n🤖 Assistente: {response}")
        
        memory.add(f"Q: {question} | A: {response}", agent="orchestrator", importance=0.9)