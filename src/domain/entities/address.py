from uuid import UUID
from dataclasses import dataclass


@dataclass
class Address:
    """Address domain entity"""
    address_id: UUID
    employee_id: UUID
    street: str
    city: str
    state: str
    postal_code: str
    country: str

    def __post_init__(self):
        if not self.street or not self.street.strip():
            raise ValueError("Street cannot be empty")
        if not self.city or not self.city.strip():
            raise ValueError("City cannot be empty")
        if not self.postal_code or not self.postal_code.strip():
            raise ValueError("Postal code cannot be empty")
        if not self.country or not self.country.strip():
            raise ValueError("Country cannot be empty")
