import json
from pathlib import Path
from requester import RequestsHttpClient
from json_handler import CopomAPIClient, minute_exists
from text_handler import extract_paragraphs_from_html, save_extracted_text, get_processed_minute
from chunker import Chunk
from embedding import EmbeddingModel
from vector_database import VectorDatabase
from llm_base import GeminiLLM, OllamaLLM
from memory import ShortTermMemory
from tools import RAGTools
from researcher_agent import ResearcherAgent
from analyst_agent import AnalystAgent
from creator_agent import CreatorAgent
from orchestrator_agent import OrchestratorAgent
import os

def index_minutes(copom_client, embedding_model, vector_database):
    RAW_DATA_PATH = Path(__file__).parent.parent / "data" / "raw"
    print("Obtendo números das 5 atas mais recentes...")
    minute_numbers = copom_client.get_latest_minute_numbers()

    for minute in minute_numbers:
        if minute_exists(minute):
            print(f"Ata n°{minute} já existe, pulando indexação.")
            continue

        print(f"Baixando ata n°{minute}...")
        copom_client.download_minute(minute)

        print(f"Extraindo texto da ata n°{minute}...")
        with open(RAW_DATA_PATH / f"ata_{minute}.json", "r") as file:
            json_file = json.load(file)
        html_content = json_file["conteudo"][0]["textoAta"]
        extract_minute = extract_paragraphs_from_html(html_content)

        print(f"Salvando texto extraído da ata n°{minute}...")
        save_extracted_text(extract_minute, minute)
        processed_minute = get_processed_minute(minute)
        chunks = Chunk.create_chunks(processed_minute, minute)

        for chunk in chunks:
            embeddings = embedding_model.generate_embeddings(chunk.text)
            vector_database.add(embeddings, chunk.text, chunk.minute_number, chunk.section, chunk.paragraph_number)

    print("Indexação concluída.\n")


def run_interface(embedding_model, vector_database):
    print("=" * 60)
    print("  Assistente Copom — RAG")
    print("  Digite 'sair' para encerrar.")
    print("=" * 60)

    while True:
        question = input("\nPergunta: ").strip()

        if not question:
            continue

        if question.lower() == "sair":
            print("Até logo!")
            break

        print("Buscando...")
        query_embedding = embedding_model.generate_embeddings(question)
        query_results = vector_database.query(query_embedding)

        print("Gerando resposta...\n")
        answer = get_interaction(query_results, question)

        print("-" * 60)
        print(answer)
        print("-" * 60)


def main():
    # Setup
    vector_db = VectorDatabase()
    embedding_model = EmbeddingModel()
    llm_orchestrator = GeminiLLM(api_key=os.getenv("API_KEY"))  # Nuvem para decisões complexas
    llm_specialist = OllamaLLM(model="qwen2.5:3b")  # Local para especialistas (opcional)
    
    memory = ShortTermMemory(max_items=30)
    tools = RAGTools(vector_db, embedding_model)
    
    # Agentes
    researcher = ResearcherAgent(llm_orchestrator, tools, memory)#(llm_specialist, tools, memory)
    analyst = AnalystAgent(llm_orchestrator, tools, memory)#(llm_specialist, tools, memory)
    creator = CreatorAgent(llm_orchestrator, memory)#(llm_orchestrator, memory)
    
    orchestrator = OrchestratorAgent(llm_orchestrator, researcher, analyst, creator, memory)

    
    # Interface
    while True:
        question = input("\nPergunta: ")
        if question.lower() == 'sair':
            break
        
        response = orchestrator.route(question)
        print(f"\n🤖 Assistente: {response}")
        
        # Salva na memória compartilhada
        memory.add(f"Q: {question} | A: {response}", agent="orchestrator", importance=0.9)


if __name__ == "__main__":
    main()
