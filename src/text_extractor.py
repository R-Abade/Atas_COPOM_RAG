from bs4 import BeautifulSoup
from pathlib import Path

PROCESSED_DATA_PATH = Path(__file__).parent.parent / "data" / "processed"

def extract_text_from_html(html_content: str):
    soup = BeautifulSoup(html_content, 'html.parser')
    return soup.get_text(separator="\n", strip=True)

def save_extracted_text(extracted_text: str, minute_number: int):
    file_path = PROCESSED_DATA_PATH / f"ata_{minute_number}.txt"
    file_path.write_text(extracted_text, encoding="utf-8")


