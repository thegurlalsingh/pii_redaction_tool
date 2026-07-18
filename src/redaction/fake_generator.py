from faker import Faker
from data_structure import pii_type
import random

class fake_generator:
    def __init__(self, seed: int = 42):
        self.faker = Faker("en_IN")
        Faker.seed(seed)

    def generate_fake(self, pii_type: pii_type) -> str:
        if pii_type == pii_type.NAME:
            return self.faker.name()
        elif pii_type == pii_type.EMAIL:
            return self.faker.safe_email()
        elif pii_type == pii_type.PHONE:
            return self.faker.phone_number()
        elif pii_type == pii_type.ADDRESS:
            return self.faker.address()
        elif pii_type == pii_type.COMPANY:
            suffixes = ["Pvt Ltd", "Limited", "Corp", "Technologies", "Holdings", "Group"]
            base_name = self.faker.company().split()[0]
            return f"{base_name} {random.choice(suffixes)}"
            # return self.faker.company()
        elif pii_type == pii_type.SSN:
            return self.faker.ssn()
        elif pii_type == pii_type.CREDIT_CARD:
            return self.faker.credit_card_number()
        elif pii_type == pii_type.DOB:
            return self.faker.date_of_birth().strftime("%m/%d/%Y")
        elif pii_type == pii_type.IP_ADDRESS:
            return self.faker.ipv4_private()

        return "[redracted]"