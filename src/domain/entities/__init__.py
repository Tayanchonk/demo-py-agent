from uuid import UUID
from typing import Optional, List
from dataclasses import dataclass


@dataclass
class Position:
    """Position domain entity"""
    position_id: UUID
    position_name: str

    def __post_init__(self):
        if not self.position_name or not self.position_name.strip():
            raise ValueError("Position name cannot be empty")


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


@dataclass
class Employee:
    """Employee domain entity"""
    emp_id: UUID
    name: str
    position_id: UUID
    position: Optional[Position] = None
    addresses: List[Address] = None

    def __post_init__(self):
        if not self.name or not self.name.strip():
            raise ValueError("Employee name cannot be empty")
        if self.addresses is None:
            self.addresses = []