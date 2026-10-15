from pathlib import Path
import json

RAW_DATA_PATH = Path(__file__).parent.parent / "data" / "raw"


class CopomAPIClient():
    def __init__(self, http_client):
        self.http = http_client

    def get_latest_minute_numbers(self):
        response = self.http.get_request('https://www.bcb.gov.br/api/servico/sitebcb/copom/atas', {'quantidade': 5})

        minute_numbers = []
        for i in response.json()["conteudo"]:
                minute_numbers.append(i["nroReuniao"])

        return minute_numbers

    def download_minute(minute_number: int):
        response = self.http.get_request(
            'https://www.bcb.gov.br/api/servico/sitebcb/copom/atas_detalhes',
            {'nro_reuniao': minute_number}
        )
        file_path = RAW_DATA_PATH / f"ata_{minute_number}.json"
        formatted = json.dumps(response.json(), indent=4, ensure_ascii=False)
        file_path.write_text(formatted, encoding="utf-8")


def minute_exists(minute_number: int):
    return (RAW_DATA_PATH / f"ata_{minute_number}.json").exists()
