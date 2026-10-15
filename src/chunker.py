from dataclasses import dataclass
import re

@dataclass

class Chunk:
    text: str
    minute_number: int
    section: str
    paragraph_number: int

    def create_chunks(text_minute: str, minute_number: int):
        chunks = []
        current_section = ""
        paragraph_number = 0

        