from pathlib import Path
from requester import get_request
import json

RAW_DATA_PATH = Path(__file__).parent.parent / "data" / "raw"

def get_latest_minute_number():
    response = get_request('https://www.bcb.gov.br/api/servico/sitebcb/copom/atas', {'quantidade': 1})
    return response.json()["conteudo"][0]["nroReuniao"]

def minute_exists(minute_number: int):
    return (RAW_DATA_PATH / f"ata_{minute_number}.json").exists()

def download_minute(minute_number: int):
    response = get_request(
        'https://www.bcb.gov.br/api/servico/sitebcb/copom/atas_detalhes',
        {'nro_reuniao': minute_number}
    )
    file_path = RAW_DATA_PATH / f"ata_{minute_number}.json"
    formatted = json.dumps(response.json(), indent=4, ensure_ascii=False)
    file_path.write_text(formatted, encoding="utf-8")
