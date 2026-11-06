class RAGTools:
    def __init__(self, vector_db: VectorDatabase, embedding_model: EmbeddingModel):
        self.db = vector_db
        self.embedder = embedding_model
    
    def search_atas(self, query: str, n_results: int = 5, filter_minute: Optional[int] = None):
        query_embedding = self.embedder.generate_embeddings(query)
        results = self.db.query(query_embedding, n_results=n_results)
        return self._format_results(results)
    
    def compare_minutes(self, minute_a: int, minute_b: int, theme: str) -> str:
        pass
    
    def get_latest_minute_number(self) -> int:
        pass