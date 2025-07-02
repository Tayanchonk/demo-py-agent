from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID
from ..entities import Employee, Position, Address


class EmployeeRepositoryInterface(ABC):
    """Repository interface for Employee entity"""

    @abstractmethod
    async def create(self, employee: Employee) -> Employee:
        pass

    @abstractmethod
    async def get_by_id(self, emp_id: UUID) -> Optional[Employee]:
        pass

    @abstractmethod
    async def get_all(self) -> List[Employee]:
        pass

    @abstractmethod
    async def update(self, employee: Employee) -> Optional[Employee]:
        pass

    @abstractmethod
    async def delete(self, emp_id: UUID) -> bool:
        pass


class PositionRepositoryInterface(ABC):
    """Repository interface for Position entity"""

    @abstractmethod
    async def create(self, position: Position) -> Position:
        pass

    @abstractmethod
    async def get_by_id(self, position_id: UUID) -> Optional[Position]:
        pass

    @abstractmethod
    async def get_all(self) -> List[Position]:
        pass

    @abstractmethod
    async def update(self, position: Position) -> Optional[Position]:
        pass

    @abstractmethod
    async def delete(self, position_id: UUID) -> bool:
        pass


class AuthRepositoryInterface(ABC):
    """Repository interface for authentication"""

    @abstractmethod
    async def create_user(self, username: str, password: str) -> bool:
        pass

    @abstractmethod
    async def verify_user(self, username: str, password: str) -> bool:
        pass


class AddressRepositoryInterface(ABC):
    """Repository interface for Address entity"""

    @abstractmethod
    async def create(self, address: Address) -> Address:
        pass

    @abstractmethod
    async def get_by_id(self, address_id: UUID) -> Optional[Address]:
        pass

    @abstractmethod
    async def get_by_employee_id(self, employee_id: UUID) -> List[Address]:
        pass

    @abstractmethod
    async def get_all(self) -> List[Address]:
        pass

    @abstractmethod
    async def update(self, address: Address) -> Optional[Address]:
        pass

    @abstractmethod
    async def delete(self, address_id: UUID) -> bool:
        pass