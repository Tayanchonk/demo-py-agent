from typing import List, Optional
from uuid import UUID, uuid4
from ..dtos import (
    EmployeeCreateDTO,
    EmployeeUpdateDTO,
    EmployeeResponseDTO,
    PositionCreateDTO,
    PositionUpdateDTO,
    PositionResponseDTO,
    LoginDTO,
    TokenResponseDTO,
    UserCreateDTO,
)
from ...domain import (
    Employee,
    Position,
    EmployeeRepositoryInterface,
    PositionRepositoryInterface,
    AuthRepositoryInterface,
)


class EmployeeUseCase:
    """Use case for employee operations"""

    def __init__(
        self,
        employee_repo: EmployeeRepositoryInterface,
        position_repo: PositionRepositoryInterface,
    ):
        self._employee_repo = employee_repo
        self._position_repo = position_repo

    async def create_employee(self, dto: EmployeeCreateDTO) -> EmployeeResponseDTO:
        """Create a new employee"""
        # Verify position exists
        position = await self._position_repo.get_by_id(dto.position_id)
        if not position:
            raise ValueError("Position not found")

        employee = Employee(
            emp_id=uuid4(),
            name=dto.name,
            position_id=dto.position_id,
        )

        created_employee = await self._employee_repo.create(employee)
        return EmployeeResponseDTO(
            emp_id=created_employee.emp_id,
            name=created_employee.name,
            position_id=created_employee.position_id,
            position_name=position.position_name,
        )

    async def get_employee(self, emp_id: UUID) -> Optional[EmployeeResponseDTO]:
        """Get employee by ID"""
        employee = await self._employee_repo.get_by_id(emp_id)
        if not employee:
            return None

        position = await self._position_repo.get_by_id(employee.position_id)
        return EmployeeResponseDTO(
            emp_id=employee.emp_id,
            name=employee.name,
            position_id=employee.position_id,
            position_name=position.position_name if position else None,
        )

    async def get_all_employees(self) -> List[EmployeeResponseDTO]:
        """Get all employees"""
        employees = await self._employee_repo.get_all()
        result = []

        for employee in employees:
            position = await self._position_repo.get_by_id(employee.position_id)
            result.append(
                EmployeeResponseDTO(
                    emp_id=employee.emp_id,
                    name=employee.name,
                    position_id=employee.position_id,
                    position_name=position.position_name if position else None,
                )
            )

        return result

    async def update_employee(
        self, emp_id: UUID, dto: EmployeeUpdateDTO
    ) -> Optional[EmployeeResponseDTO]:
        """Update employee"""
        employee = await self._employee_repo.get_by_id(emp_id)
        if not employee:
            return None

        if dto.position_id:
            position = await self._position_repo.get_by_id(dto.position_id)
            if not position:
                raise ValueError("Position not found")
            employee.position_id = dto.position_id

        if dto.name:
            employee.name = dto.name

        updated_employee = await self._employee_repo.update(employee)
        if not updated_employee:
            return None

        position = await self._position_repo.get_by_id(updated_employee.position_id)
        return EmployeeResponseDTO(
            emp_id=updated_employee.emp_id,
            name=updated_employee.name,
            position_id=updated_employee.position_id,
            position_name=position.position_name if position else None,
        )

    async def delete_employee(self, emp_id: UUID) -> bool:
        """Delete employee"""
        return await self._employee_repo.delete(emp_id)


class PositionUseCase:
    """Use case for position operations"""

    def __init__(self, position_repo: PositionRepositoryInterface):
        self._position_repo = position_repo

    async def create_position(self, dto: PositionCreateDTO) -> PositionResponseDTO:
        """Create a new position"""
        position = Position(
            position_id=uuid4(),
            position_name=dto.position_name,
        )

        created_position = await self._position_repo.create(position)
        return PositionResponseDTO(
            position_id=created_position.position_id,
            position_name=created_position.position_name,
        )

    async def get_position(self, position_id: UUID) -> Optional[PositionResponseDTO]:
        """Get position by ID"""
        position = await self._position_repo.get_by_id(position_id)
        if not position:
            return None

        return PositionResponseDTO(
            position_id=position.position_id,
            position_name=position.position_name,
        )

    async def get_all_positions(self) -> List[PositionResponseDTO]:
        """Get all positions"""
        positions = await self._position_repo.get_all()
        return [
            PositionResponseDTO(
                position_id=position.position_id,
                position_name=position.position_name,
            )
            for position in positions
        ]

    async def update_position(
        self, position_id: UUID, dto: PositionUpdateDTO
    ) -> Optional[PositionResponseDTO]:
        """Update position"""
        position = await self._position_repo.get_by_id(position_id)
        if not position:
            return None

        position.position_name = dto.position_name
        updated_position = await self._position_repo.update(position)
        if not updated_position:
            return None

        return PositionResponseDTO(
            position_id=updated_position.position_id,
            position_name=updated_position.position_name,
        )

    async def delete_position(self, position_id: UUID) -> bool:
        """Delete position"""
        return await self._position_repo.delete(position_id)


class AuthUseCase:
    """Use case for authentication operations"""

    def __init__(self, auth_repo: AuthRepositoryInterface, jwt_service):
        self._auth_repo = auth_repo
        self._jwt_service = jwt_service

    async def login(self, dto: LoginDTO) -> Optional[TokenResponseDTO]:
        """Login user and generate token"""
        if await self._auth_repo.verify_user(dto.username, dto.password):
            token = self._jwt_service.create_access_token({"sub": dto.username})
            return TokenResponseDTO(access_token=token)
        return None

    async def create_user(self, dto: UserCreateDTO) -> bool:
        """Create a new user"""
        return await self._auth_repo.create_user(dto.username, dto.password)