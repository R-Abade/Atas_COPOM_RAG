from dataclasses import dataclass
import re

@dataclass

class Chunk:
    text: str
    minute_number: int
    section: str
    paragraph_number: int

    @staticmethod
    def create_chunks(text_minute: str, minute_number: int):
        chunks = []
        current_section = ""
        paragraph_number = 0

        for line in text_minute:
            print(line)
            line = line.strip()
            if not line:
                continue

            if line.startswith('[') and line.endswith(']'): # verifica a seção   
                current_section = line[4:-1]
                continue

            match = re.match(r'^(\d+)\.\s+(.*)', line) # verifica o número do parágrafo e as demais informações da ata
            if match:
                paragraph_number = int(match.group(1))
                text = match.group(2)

                chunks.append(Chunk(text, minute_number, current_section, paragraph_number))
 
        return chunks
