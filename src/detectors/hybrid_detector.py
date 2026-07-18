from typing import List
from data_structure import pii_entity, pii_type
from .regex_detector import regex_detector
from .ner_detector import ner_detector

class hybrid_detector:
    def __init__(self):
        self.regex_detector = regex_detector()
        self.ner_detector = ner_detector()

        self.priority = {
            pii_type.EMAIL: 1,
            pii_type.PHONE: 2,
            pii_type.ADDRESS: 3,
            pii_type.NAME: 4,
            pii_type.COMPANY: 5,
            pii_type.SSN: 6,
            pii_type.CREDIT_CARD: 7,
            pii_type.DOB: 8,
            pii_type.IP_ADDRESS: 9,
            pii_type.UNKNOWN: 99
        }

    def detect(self, text: str) -> List[pii_entity]:
        regex_ents = self.regex_detector.detect(text)
        ner_ents = self.ner_detector.detect(text)

        all_ents = regex_ents + ner_ents
        cleaned_ents = []
        for ent in all_ents:
            if ent.entity_type in [pii_type.NAME, pii_type.COMPANY]:
                prefixes = ["Contact person:", "Contact:", "Name:", "Website:", "E-mail:"]
                for pref in prefixes:
                    if ent.text.lower().startswith(pref.lower()):
                        offset = len(pref)
                        spaces = len(ent.text[offset:]) - len(ent.text[offset:].lstrip())
                        ent.text = ent.text[offset:].strip()
                        ent.start_char += (offset + spaces)
            
            if ent.entity_type == pii_type.NAME:
                context = text[max(0, ent.start_char - 10) : min(len(text), ent.end_char + 10)].lower()
                if "@" in context or "www." in context or ".com" in context or ".in" in context:
                    continue

            if len(ent.text.strip()) > 1:
                cleaned_ents.append(ent)

        return self._resolve_overlaps(cleaned_ents)

    def _resolve_overlaps(self, entries: List[pii_entity]) -> List[pii_entity]:
        if not entries:
            return []
        
        entries.sort(key=lambda e: (e.start_char, self.priority.get(e.entity_type, 99), -(e.end_char - e.start_char)))

        resolved = []
        current = entries[0]
        
        for nxt in entries[1:]:
            if nxt.start_char < current.end_char:
                curr_pri = self.priority.get(current.entity_type, 99)
                nxt_pri = self.priority.get(nxt.entity_type, 99)
                if nxt_pri < curr_pri:
                    current = nxt
                elif nxt_pri == curr_pri:
                    if (nxt.end_char - nxt.start_char) > (current.end_char - current.start_char):
                        current = nxt
                
            else:
                resolved.append(current)
                current = nxt

        resolved.append(current)
        return resolved