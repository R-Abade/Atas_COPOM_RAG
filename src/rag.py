from typing import Protocol
from dataclasses import dataclass

@dataclass
class DocumentChunk:
    content: str
    source: str
    section: str



