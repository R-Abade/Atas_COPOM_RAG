import json
from pathlib import Path
from json_handler import get_latest_minute_number, minute_exists, download_minute
from text_handler import extract_paragraphs_from_html, save_extracted_text

def main():
    RAW_DATA_PATH = Path(__file__).parent.parent / "data" / "raw"
    print("Obtendo número da ata mais recente...")
    minute_number = get_latest_minute_number()
    
    if minute_exists(minute_number):
        print(f"Ata n°{minute_number} recente já existe!")
    else:
        print("Baixando ata mais recente...")
        download_minute(minute_number)

        print("Extraindo texto da ata...")
        with open(RAW_DATA_PATH / f"ata_{minute_number}.json", "r") as file:
            json_file = json.load(file)
        html_content = json_file["conteudo"][0]["textoAta"]
        extract_minute = extract_paragraphs_from_html(html_content)

        print("Salvando texto extraído...")
        save_extracted_text(extract_minute, minute_number)

if __name__ == "__main__":
    main()
