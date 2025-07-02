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
    AddressCreateDTO,
    AddressUpdateDTO,
    AddressResponseDTO,
)
from ...domain import (
    Employee,
    Position,
    Address,
    EmployeeRepositoryInterface,
    PositionRepositoryInterface,
    AuthRepositoryInterface,
    AddressRepositoryInterface,
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
        
        
class AddressUseCase:
    """Use case for address operations"""

    def __init__(
        self,
        address_repo: AddressRepositoryInterface,
        employee_repo: EmployeeRepositoryInterface,
    ):
        self._address_repo = address_repo
        self._employee_repo = employee_repo

    async def create_address(self, dto: AddressCreateDTO) -> AddressResponseDTO:
        """Create a new address"""
        # Verify employee exists
        employee = await self._employee_repo.get_by_id(dto.employee_id)
        if not employee:
            raise ValueError("Employee not found")

        address = Address(
            address_id=uuid4(),
            employee_id=dto.employee_id,
            street=dto.street,
            city=dto.city,
            state=dto.state,
            postal_code=dto.postal_code,
            country=dto.country,
        )

        created_address = await self._address_repo.create(address)
        return AddressResponseDTO(
            address_id=created_address.address_id,
            employee_id=created_address.employee_id,
            street=created_address.street,
            city=created_address.city,
            state=created_address.state,
            postal_code=created_address.postal_code,
            country=created_address.country,
        )

    async def get_address(self, address_id: UUID) -> Optional[AddressResponseDTO]:
        """Get address by ID"""
        address = await self._address_repo.get_by_id(address_id)
        if not address:
            return None

        return AddressResponseDTO(
            address_id=address.address_id,
            employee_id=address.employee_id,
            street=address.street,
            city=address.city,
            state=address.state,
            postal_code=address.postal_code,
            country=address.country,
        )

    async def get_addresses_by_employee(self, employee_id: UUID) -> List[AddressResponseDTO]:
        """Get addresses by employee ID"""
        # Verify employee exists
        employee = await self._employee_repo.get_by_id(employee_id)
        if not employee:
            raise ValueError("Employee not found")
            
        addresses = await self._address_repo.get_by_employee_id(employee_id)
        return [
            AddressResponseDTO(
                address_id=address.address_id,
                employee_id=address.employee_id,
                street=address.street,
                city=address.city,
                state=address.state,
                postal_code=address.postal_code,
                country=address.country,
            )
            for address in addresses
        ]

    async def get_all_addresses(self) -> List[AddressResponseDTO]:
        """Get all addresses"""
        addresses = await self._address_repo.get_all()
        return [
            AddressResponseDTO(
                address_id=address.address_id,
                employee_id=address.employee_id,
                street=address.street,
                city=address.city,
                state=address.state,
                postal_code=address.postal_code,
                country=address.country,
            )
            for address in addresses
        ]

    async def update_address(
        self, address_id: UUID, dto: AddressUpdateDTO
    ) -> Optional[AddressResponseDTO]:
        """Update address"""
        address = await self._address_repo.get_by_id(address_id)
        if not address:
            return None

        if dto.street:
            address.street = dto.street
        if dto.city:
            address.city = dto.city
        if dto.state:
            address.state = dto.state
        if dto.postal_code:
            address.postal_code = dto.postal_code
        if dto.country:
            address.country = dto.country

        updated_address = await self._address_repo.update(address)
        if not updated_address:
            return None

        return AddressResponseDTO(
            address_id=updated_address.address_id,
            employee_id=updated_address.employee_id,
            street=updated_address.street,
            city=updated_address.city,
            state=updated_address.state,
            postal_code=updated_address.postal_code,
            country=updated_address.country,
        )

    async def delete_address(self, address_id: UUID) -> bool:
        """Delete address"""
        return await self._address_repo.delete(address_id)