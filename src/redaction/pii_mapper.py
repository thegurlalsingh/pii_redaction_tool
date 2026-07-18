from typing import Dict
from data_structure import pii_type
from .fake_generator import fake_generator

class pii_mapper:
    def __init__(self):
        self.generator = fake_generator()
        self.mapping: Dict[tuple[str, pii_type], str] = {}

    def get_replacement(self, original_text: str, pii_type: pii_type) -> str:
        print("MAPPER IN =>", pii_type, "|", repr(original_text))
        key = (original_text.lower().strip(), pii_type)
        if key not in self.mapping:
            self.mapping[key] = self.generator.generate_fake(pii_type)
        
        return self.mapping[key]