from dataclasses import dataclass
from enum import Enum

class pii_type(Enum):
    NAME = "NAME"
    EMAIL = "EMAIL"
    PHONE = "PHONE"
    ADDRESS = "ADDRESS"
    COMPANY = "COMPANY"
    SSN = "SSN"
    CREDIT_CARD = "CREDIT_CARD"
    DOB = "DOB"
    IP_ADDRESS = "IP_ADDRESS"
    UNKNOWN = "UNKNOWN"

@dataclass
class pii_entity:
    text: str
    entity_type: pii_type
    start_char: int
    end_char: int
    confidence_score: float = 1.0