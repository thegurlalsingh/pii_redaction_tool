import spacy
from typing import List
from data_structure import pii_type, pii_entity

class ner_detector:
    def __init__(self, model_name = "en_core_web_sm"):
        try:
            self.nlp = spacy.load(model_name)
        except OSError:
            raise RuntimeError(f"Model '{model_name}' not found.")

        self.label_map = {
            "PERSON": pii_type.NAME,
            "ORG": pii_type.COMPANY,
            "GPE": pii_type.ADDRESS,
            "LOC": pii_type.ADDRESS,
            "FAC": pii_type.ADDRESS
        }

    def detect(self, text: str) -> List[pii_entity]:
        doc = self.nlp(text)
        entries = []

        for ent in doc.ents:
            if ent.label_ in self.label_map:
                pii_type = self.label_map[ent.label_]
                entries.append(pii_entity(
                    text = ent.text,
                    entity_type = pii_type,
                    start_char = ent.start_char,
                    end_char = ent.end_char,
                    confidence_score = 0.80
                ))

        return entries
