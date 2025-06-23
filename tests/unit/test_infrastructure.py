import pytest
import pytest_asyncio
import tempfile
import os
from uuid import uuid4
from src.infrastructure.database import (
    DatabaseConnection,
    SQLiteEmployeeRepository,
    SQLitePositionRepository,
)
from src.infrastructure.auth import SQLiteAuthRepository, JWTService
from src.domain.entities import Employee, Position


class TestDatabaseConnection:
    """Test database connection"""

    @pytest_asyncio.fixture
    async def temp_db(self):
        """Create temporary database for testing"""
        fd, path = tempfile.mkstemp(suffix=".db")
        os.close(fd)
        db = DatabaseConnection(path)
        await db.initialize()
        yield db
        os.unlink(path)

    @pytest.mark.asyncio
    async def test_database_initialization(self, temp_db):
        """Test database table creation"""
        async with temp_db.get_connection() as conn:
            # Check if tables exist
            cursor = await conn.execute(
                "SELECT name FROM sqlite_master WHERE type='table'"
            )
            tables = [row[0] for row in await cursor.fetchall()]
            
            assert "employees" in tables
            assert "positions" in tables
            assert "users" in tables


class TestSQLitePositionRepository:
    """Test SQLite position repository"""

    @pytest_asyncio.fixture
    async def temp_db(self):
        fd, path = tempfile.mkstemp(suffix=".db")
        os.close(fd)
        db = DatabaseConnection(path)
        await db.initialize()
        yield db
        os.unlink(path)

    @pytest.fixture
    def position_repo(self, temp_db):
        return SQLitePositionRepository(temp_db)

    @pytest.mark.asyncio
    async def test_create_position(self, position_repo):
        """Test position creation"""
        position = Position(position_id=uuid4(), position_name="Developer")
        
        created = await position_repo.create(position)
        
        assert created.position_id == position.position_id
        assert created.position_name == position.position_name

    @pytest.mark.asyncio
    async def test_get_position_by_id(self, position_repo):
        """Test position retrieval by ID"""
        position = Position(position_id=uuid4(), position_name="Developer")
        await position_repo.create(position)
        
        retrieved = await position_repo.get_by_id(position.position_id)
        
        assert retrieved is not None
        assert retrieved.position_id == position.position_id
        assert retrieved.position_name == position.position_name

    @pytest.mark.asyncio
    async def test_get_position_not_found(self, position_repo):
        """Test position retrieval when not found"""
        non_existent_id = uuid4()
        
        result = await position_repo.get_by_id(non_existent_id)
        
        assert result is None

    @pytest.mark.asyncio
    async def test_get_all_positions(self, position_repo):
        """Test getting all positions"""
        position1 = Position(position_id=uuid4(), position_name="Developer")
        position2 = Position(position_id=uuid4(), position_name="Manager")
        
        await position_repo.create(position1)
        await position_repo.create(position2)
        
        positions = await position_repo.get_all()
        
        assert len(positions) == 2
        position_names = [p.position_name for p in positions]
        assert "Developer" in position_names
        assert "Manager" in position_names


class TestSQLiteEmployeeRepository:
    """Test SQLite employee repository"""

    @pytest_asyncio.fixture
    async def temp_db(self):
        fd, path = tempfile.mkstemp(suffix=".db")
        os.close(fd)
        db = DatabaseConnection(path)
        await db.initialize()
        yield db
        os.unlink(path)

    @pytest.fixture
    def employee_repo(self, temp_db):
        return SQLiteEmployeeRepository(temp_db)

    @pytest.fixture
    def position_repo(self, temp_db):
        return SQLitePositionRepository(temp_db)

    @pytest.mark.asyncio
    async def test_create_employee(self, employee_repo, position_repo):
        """Test employee creation"""
        # Create position first
        position = Position(position_id=uuid4(), position_name="Developer")
        await position_repo.create(position)
        
        employee = Employee(
            emp_id=uuid4(),
            name="John Doe",
            position_id=position.position_id
        )
        
        created = await employee_repo.create(employee)
        
        assert created.emp_id == employee.emp_id
        assert created.name == employee.name
        assert created.position_id == employee.position_id

    @pytest.mark.asyncio
    async def test_get_employee_by_id(self, employee_repo, position_repo):
        """Test employee retrieval by ID"""
        # Create position first
        position = Position(position_id=uuid4(), position_name="Developer")
        await position_repo.create(position)
        
        employee = Employee(
            emp_id=uuid4(),
            name="John Doe",
            position_id=position.position_id
        )
        await employee_repo.create(employee)
        
        retrieved = await employee_repo.get_by_id(employee.emp_id)
        
        assert retrieved is not None
        assert retrieved.emp_id == employee.emp_id
        assert retrieved.name == employee.name
        assert retrieved.position_id == employee.position_id


class TestJWTService:
    """Test JWT service"""

    @pytest.fixture
    def jwt_service(self):
        return JWTService("test_secret_key")

    def test_create_access_token(self, jwt_service):
        """Test token creation"""
        data = {"sub": "testuser"}
        token = jwt_service.create_access_token(data)
        
        assert token is not None
        assert isinstance(token, str)

    def test_verify_token_valid(self, jwt_service):
        """Test valid token verification"""
        data = {"sub": "testuser"}
        token = jwt_service.create_access_token(data)
        
        payload = jwt_service.verify_token(token)
        
        assert payload is not None
        assert payload["sub"] == "testuser"

    def test_verify_token_invalid(self, jwt_service):
        """Test invalid token verification"""
        invalid_token = "invalid.token.here"
        
        payload = jwt_service.verify_token(invalid_token)
        
        assert payload is None


class TestSQLiteAuthRepository:
    """Test SQLite auth repository"""

    @pytest_asyncio.fixture
    async def temp_db(self):
        fd, path = tempfile.mkstemp(suffix=".db")
        os.close(fd)
        db = DatabaseConnection(path)
        await db.initialize()
        yield db
        os.unlink(path)

    @pytest.fixture
    def auth_repo(self, temp_db):
        return SQLiteAuthRepository(temp_db)

    @pytest.mark.asyncio
    async def test_create_user(self, auth_repo):
        """Test user creation"""
        result = await auth_repo.create_user("testuser", "password")
        
        assert result is True

    @pytest.mark.asyncio
    async def test_create_duplicate_user(self, auth_repo):
        """Test creating duplicate user fails"""
        await auth_repo.create_user("testuser", "password")
        
        result = await auth_repo.create_user("testuser", "password")
        
        assert result is False

    @pytest.mark.asyncio
    async def test_verify_user_valid(self, auth_repo):
        """Test valid user verification"""
        await auth_repo.create_user("testuser", "password")
        
        result = await auth_repo.verify_user("testuser", "password")
        
        assert result is True

    @pytest.mark.asyncio
    async def test_verify_user_invalid_password(self, auth_repo):
        """Test invalid password verification"""
        await auth_repo.create_user("testuser", "password")
        
        result = await auth_repo.verify_user("testuser", "wrongpassword")
        
        assert result is False

    @pytest.mark.asyncio
    async def test_verify_user_not_found(self, auth_repo):
        """Test verification of non-existent user"""
        result = await auth_repo.verify_user("nonexistent", "password")
        
        assert result is False