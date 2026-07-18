import re
from typing import List
from data_structure import pii_entity, pii_type

class regex_detector:
    def __init__(self):

        self.patterns = {
            pii_type.EMAIL: re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'),
            pii_type.PHONE: re.compile(r'(?:\+\s*\d{1,3}[\s-]*)?(?:\(?\d{2,5}\)?[\s-]*)?\d{3,5}[\s-]*\d{3,5}\b'),
            pii_type.SSN: re.compile(r'\b\d{3}-\d{2}-\d{4}\b'),
            pii_type.CREDIT_CARD: re.compile(r'\b(?:\d[ -]*?){13,16}\b'),
            pii_type.DOB: re.compile(r'\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b'),
            pii_type.ADDRESS: re.compile(r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b')
        }

    def detect(self, text: str) -> List[pii_entity]:
        entries = []
        for pii_type, pattern in self.patterns.items():
            for match in pattern.finditer(text):
                if pii_type == pii_type.CREDIT_CARD:
                    cleaned = re.sub(r'[-\s]', '', match.group())
                    if len(cleaned) < 13 or len(cleaned) > 16:
                        continue
                
                if pii_type == pii_type.PHONE:
                    cleaned = re.sub(r'\D', '', match.group())
                    if len(cleaned) < 10 or len(cleaned) > 13:
                        continue

                entries.append(pii_entity(
                    text = match.group(),
                    entity_type = pii_type,
                    start_char = match.start(),
                    end_char = match.end(),
                    confidence_score = 1.0
                ))

        return entries
            