from uuid import UUID
from typing import Optional
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
class Employee:
    """Employee domain entity"""
    emp_id: UUID
    name: str
    position_id: UUID
    position: Optional[Position] = None

    def __post_init__(self):
        if not self.name or not self.name.strip():
            raise ValueError("Employee name cannot be empty")