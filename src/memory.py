from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional

@dataclass
class MemoryItem:
    content: str
    timestamp: datetime
    agent_origin: str  
    importance: float

class ShortTermMemory:
    def __init__(self, max_items: int = 20):
        self.memories: List[MemoryItem] = []
        self.max_items = max_items
    
    def add(self, content: str, agent: str, importance: float = 0.5):
        item = MemoryItem(content, datetime.now(), agent, importance)
        self.memories.append(item)
        if len(self.memories) > self.max_items:
            self.memories.sort(key=lambda x: (x.importance, x.timestamp), reverse=True)
            self.memories = self.memories[:self.max_items]
    
    def get_context(self, limit: int = 5): # Retorna contexto formatado para injetar no prompt
        recent = sorted(self.memories, key=lambda x: x.timestamp, reverse=True)[:limit]
        return "\n".join([f"[{m.agent_origin}]: {m.content}" for m in recent])