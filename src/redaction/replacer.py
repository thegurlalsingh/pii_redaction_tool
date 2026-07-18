from typing import List
from data_structure import pii_entity
from .pii_mapper import pii_mapper

class replacer: 
    def __init__(self):
        self.mapper = pii_mapper()
    
    def redact_text(self, text: str, entries: List[pii_entity]) -> str:
        entries.sort(key = lambda e: e.start_char, reverse = True)
        redacted_text = text
        for entry in entries:
            replacement = self.mapper.get_replacement(entry.text, entry.entity_type)
            redacted_text = (redacted_text[:entry.start_char] + replacement + redacted_text[entry.end_char:])

        return redacted_text