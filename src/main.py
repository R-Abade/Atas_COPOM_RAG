import json
from pathlib import Path
from requester import RequestsHttpClient
from json_handler import CopomAPIClient, minute_exists
from text_handler import extract_paragraphs_from_html, save_extracted_text, get_processed_minute
from chunker import Chunk
from embedding import EmbeddingModel
from vector_database import VectorDatabase

def main():
    http = RequestsHttpClient()
    copom_client = CopomAPIClient(http)
    embedding_model = EmbeddingModel()
    vector_database = VectorDatabase()

    RAW_DATA_PATH = Path(__file__).parent.parent / "data" / "raw"
    print("Obtendo números das 5 atas mais recente...")
    minute_numbers = copom_client.get_latest_minute_numbers()
    
    for minute in minute_numbers:
        chunks = {}
        if minute_exists(minute):
            print(f"Ata n°{minute} recente já existe!")
            #processed_minute = get_processed_minute(minute)
            #chunks = Chunk.create_chunks(processed_minute, minute)
            query_embedding = embedding_model.generate_embeddings("o que o Copom decidiu sobre a taxa de juros?")
            results = vector_database.query(query_embedding)
            print(results)
            """ 
                for chunk in chunks:
                    embeddings = embedding_model.generate_embeddings(chunk.text)
                    vector_database.add(embeddings, chunk.text, chunk.minute_number, chunk.section, chunk.paragraph_number)
            """
        
            
        else:
            print(f"Baixando ata n°{minute}...")
            copom_client.download_minute(minute)

            print(f"Extraindo texto da ata n°{minute}...")
            with open(RAW_DATA_PATH / f"ata_{minute}.json", "r") as file:
                json_file = json.load(file)
            html_content = json_file["conteudo"][0]["textoAta"]
            extract_minute = extract_paragraphs_from_html(html_content)

            print(f"Salvando texto extraído da ata n°{minute}...")
            save_extracted_text(extract_minute, minute)

if __name__ == "__main__":
    main()
