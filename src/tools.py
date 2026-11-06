class RAGTools:
    def __init__(self, vector_db: VectorDatabase, embedding_model: EmbeddingModel):
        self.db = vector_db
        self.embedder = embedding_model
    
    def search_atas(self, query: str, n_results: int = 5, filter_minute: Optional[int] = None):
        query_embedding = self.embedder.generate_embeddings(query)
        results = self.db.query(query_embedding, n_results=n_results)
        return self.format_results(results)
    
    def format_results(self, results: dict) -> str:
        documents = results.get("documents", [[]])[0]
        metadatas = results.get("metadatas", [[]])[0]

        if not documents:
            return "Nenhum trecho relevante encontrado nas atas indexadas."

        formatted = []
        for doc, meta in zip(documents, metadatas):
            ata = meta.get("ata", "?")
            section = meta.get("section", "?")
            paragraph = meta.get("paragraph", "?")
            formatted.append(f"[Ata {ata}, Seção {section}, Parágrafo {paragraph}]\n{doc}")

        return "\n\n".join(formatted)

    def compare_minutes(self, minute_a: int, minute_b: int, theme: str) -> str:
        results_a = self.search_atas(f"{theme}", n_results=3, filter_minute=minute_a)
        results_b = self.search_atas(f"{theme}", n_results=3, filter_minute=minute_b)
        return f"Ata {minute_a}:\n{results_a}\n\nAta {minute_b}:\n{results_b}"