from bs4 import BeautifulSoup, Tag
from pathlib import Path

PROCESSED_DATA_PATH = Path(__file__).parent.parent / "data" / "processed"


def extract_table_as_text(table_tag: Tag):
    headers = [th.get_text(strip=True) for th in table_tag.select('thead th')]
    rows = []
    for tr in table_tag.select('tbody tr'):
        cells = [td.get_text(strip=True) for td in tr.find_all('td')]
        if not cells:
            continue
        row_text = cells[0] + ": " + ", ".join(
            f"{headers[i]}={cells[i]}" for i in range(1, len(cells))
        )
        rows.append(row_text)
    return "Projeções de inflação (IPCA): " + " | ".join(rows)


def extract_paragraphs_from_html(html_content: str):
    soup = BeautifulSoup(html_content, 'html.parser')

    main_content = soup.find('div', id='ataconteudo')
    if not main_content:
        return []

    paragraphs = []
    for tag in main_content.children:
        if not isinstance(tag, Tag):
            continue

        if tag.name == 'h3':
            paragraphs.append(f"[{tag.get_text(strip=True)}]")

        elif tag.name == 'p' and 'paragrafo' in tag.get('class', []):
            paragraphs.append(tag.get_text(strip=True))

        elif tag.name == 'div' and 'arealivre' in tag.get('class', []):
            table = tag.find('table')
            if table:
                paragraphs.append(extract_table_as_text(table))

    return paragraphs


def save_extracted_text(paragraphs: list[str], minute_number: int):
    file_path = PROCESSED_DATA_PATH / f"ata_{minute_number}.txt"
    file_path.write_text("\n\n".join(paragraphs), encoding="utf-8")


def get_processed_minute(minute: int):
    file_path = PROCESSED_DATA_PATH / f"ata_{minute}.txt"
    if not file_path.exists():
        return None

    print(f"Processando a ata {minute}...")
    text = file_path.read_text(encoding="utf-8")
    return text.split("\n\n")
