import chromadb
from pathlib import Path

DATABASE_PATH = Path(__file__).parent.parent / "data" / "vector_db"
chroma_client = chromadb.PersistentClient(path = DATABASE_PATH)
collection = chroma_client.get_or_create_collection("atas_copom")

class VectorDatabase:
    def __init__(self):
        self.client = chroma_client
        self.collection = collection
    
    def add(self, embedding : EmbeddingModel, text : str, minute_number : int, section : str, paragraph_number : str):
        self.collection.add(
            embeddings = embedding,
            metadatas = [{
                "ata": minute_number, 
                "section": section, 
                "paragraph": paragraph_number
                }],
            documents = text,
            ids = [f"ata_{minute_number}_paragraph_{paragraph_number}"]
        )
        print(f"Os dados da ata_{minute_number} foram adicionados ao banco de dados!")

        
    def query(self, query_embedding, n_results=5):
        results = self.collection.query(
            query_embeddings=[query_embedding],
            include=['metadatas', 'documents'],
            n_results=n_results
        )
        return results

    def store_conversation(self, query, response):
        """Armazena conversa no banco vetorial"""
        embedding = self.embedding_model.generate_embedding(query)
        self.embeddings.append(embedding)
        self.conversations.append({
            "query": query,
            "response": response,
            "embedding": embedding
        })


