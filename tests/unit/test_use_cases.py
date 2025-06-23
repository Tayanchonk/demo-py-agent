import pytest
import pytest_asyncio
from unittest.mock import AsyncMock, MagicMock
from uuid import uuid4
from src.application.use_cases import EmployeeUseCase, PositionUseCase, AuthUseCase
from src.application.dtos import (
    EmployeeCreateDTO,
    EmployeeUpdateDTO,
    PositionCreateDTO,
    PositionUpdateDTO,
    LoginDTO,
    UserCreateDTO,
)
from src.domain.entities import Employee, Position


class TestEmployeeUseCase:
    """Test Employee use case"""

    @pytest.fixture
    def employee_repo(self):
        return AsyncMock()

    @pytest.fixture
    def position_repo(self):
        return AsyncMock()

    @pytest.fixture
    def employee_use_case(self, employee_repo, position_repo):
        return EmployeeUseCase(employee_repo, position_repo)

    @pytest.mark.asyncio
    async def test_create_employee_success(self, employee_use_case, employee_repo, position_repo):
        """Test successful employee creation"""
        # Arrange
        position_id = uuid4()
        position = Position(position_id=position_id, position_name="Developer")
        position_repo.get_by_id.return_value = position
        
        created_employee = Employee(emp_id=uuid4(), name="John Doe", position_id=position_id)
        employee_repo.create.return_value = created_employee
        
        dto = EmployeeCreateDTO(name="John Doe", position_id=position_id)
        
        # Act
        result = await employee_use_case.create_employee(dto)
        
        # Assert
        assert result.name == "John Doe"
        assert result.position_id == position_id
        assert result.position_name == "Developer"
        position_repo.get_by_id.assert_called_once_with(position_id)
        employee_repo.create.assert_called_once()

    @pytest.mark.asyncio
    async def test_create_employee_position_not_found(self, employee_use_case, position_repo):
        """Test employee creation with non-existent position"""
        # Arrange
        position_id = uuid4()
        position_repo.get_by_id.return_value = None
        dto = EmployeeCreateDTO(name="John Doe", position_id=position_id)
        
        # Act & Assert
        with pytest.raises(ValueError, match="Position not found"):
            await employee_use_case.create_employee(dto)

    @pytest.mark.asyncio
    async def test_get_employee_success(self, employee_use_case, employee_repo, position_repo):
        """Test successful employee retrieval"""
        # Arrange
        emp_id = uuid4()
        position_id = uuid4()
        employee = Employee(emp_id=emp_id, name="John Doe", position_id=position_id)
        position = Position(position_id=position_id, position_name="Developer")
        
        employee_repo.get_by_id.return_value = employee
        position_repo.get_by_id.return_value = position
        
        # Act
        result = await employee_use_case.get_employee(emp_id)
        
        # Assert
        assert result is not None
        assert result.emp_id == emp_id
        assert result.name == "John Doe"
        assert result.position_name == "Developer"

    @pytest.mark.asyncio
    async def test_get_employee_not_found(self, employee_use_case, employee_repo):
        """Test employee retrieval when not found"""
        # Arrange
        emp_id = uuid4()
        employee_repo.get_by_id.return_value = None
        
        # Act
        result = await employee_use_case.get_employee(emp_id)
        
        # Assert
        assert result is None


class TestPositionUseCase:
    """Test Position use case"""

    @pytest.fixture
    def position_repo(self):
        return AsyncMock()

    @pytest.fixture
    def position_use_case(self, position_repo):
        return PositionUseCase(position_repo)

    @pytest.mark.asyncio
    async def test_create_position_success(self, position_use_case, position_repo):
        """Test successful position creation"""
        # Arrange
        created_position = Position(position_id=uuid4(), position_name="Developer")
        position_repo.create.return_value = created_position
        
        dto = PositionCreateDTO(position_name="Developer")
        
        # Act
        result = await position_use_case.create_position(dto)
        
        # Assert
        assert result.position_name == "Developer"
        position_repo.create.assert_called_once()

    @pytest.mark.asyncio
    async def test_get_position_success(self, position_use_case, position_repo):
        """Test successful position retrieval"""
        # Arrange
        position_id = uuid4()
        position = Position(position_id=position_id, position_name="Developer")
        position_repo.get_by_id.return_value = position
        
        # Act
        result = await position_use_case.get_position(position_id)
        
        # Assert
        assert result is not None
        assert result.position_id == position_id
        assert result.position_name == "Developer"


class TestAuthUseCase:
    """Test Auth use case"""

    @pytest.fixture
    def auth_repo(self):
        return AsyncMock()

    @pytest.fixture
    def jwt_service(self):
        mock = MagicMock()
        mock.create_access_token.return_value = "test_token"
        return mock

    @pytest.fixture
    def auth_use_case(self, auth_repo, jwt_service):
        return AuthUseCase(auth_repo, jwt_service)

    @pytest.mark.asyncio
    async def test_login_success(self, auth_use_case, auth_repo, jwt_service):
        """Test successful login"""
        # Arrange
        auth_repo.verify_user.return_value = True
        dto = LoginDTO(username="testuser", password="password")
        
        # Act
        result = await auth_use_case.login(dto)
        
        # Assert
        assert result is not None
        assert result.access_token == "test_token"
        assert result.token_type == "bearer"

    @pytest.mark.asyncio
    async def test_login_invalid_credentials(self, auth_use_case, auth_repo):
        """Test login with invalid credentials"""
        # Arrange
        auth_repo.verify_user.return_value = False
        dto = LoginDTO(username="testuser", password="wrongpassword")
        
        # Act
        result = await auth_use_case.login(dto)
        
        # Assert
        assert result is None

    @pytest.mark.asyncio
    async def test_create_user_success(self, auth_use_case, auth_repo):
        """Test successful user creation"""
        # Arrange
        auth_repo.create_user.return_value = True
        dto = UserCreateDTO(username="newuser", password="password")
        
        # Act
        result = await auth_use_case.create_user(dto)
        
        # Assert
        assert result is True
        auth_repo.create_user.assert_called_once_with("newuser", "password")