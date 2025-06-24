import pytest
import pytest_asyncio
import tempfile
import os
from fastapi.testclient import TestClient
from uuid import uuid4
from main import app
from src.interface.dependencies import get_database, db_connection


# Override database dependency for testing
@pytest.fixture
async def test_db():
    """Create test database"""
    fd, path = tempfile.mkstemp(suffix=".db")
    os.close(fd)
    
    # Import here to avoid circular imports
    from src.infrastructure.database import DatabaseConnection
    test_db_connection = DatabaseConnection(path)
    await test_db_connection.initialize()
    
    # Override the dependency
    app.dependency_overrides[get_database] = lambda: test_db_connection
    
    yield test_db_connection
    
    # Cleanup
    app.dependency_overrides.clear()
    os.unlink(path)


@pytest.fixture
def client():
    """Create test client"""
    return TestClient(app)


@pytest.fixture
async def auth_token(client, test_db):
    """Create a test user and return auth token"""
    # Make sure database is initialized
    await test_db.initialize()
    
    # สร้างชื่อผู้ใช้งานที่เป็นเอกลักษณ์มากขึ้น
    import uuid
    unique_username = f"auth_user_{uuid.uuid4().hex[:8]}"
    print(f"Registering auth user: {unique_username}")
    
    # Register user
    response = client.post(
        "/auth/register",
        json={"username": unique_username, "password": "testpass123"}
    )
    assert response.status_code == 201
    
    # Login and get token
    response = client.post(
        "/auth/login",
        json={"username": unique_username, "password": "testpass123"}
    )
    assert response.status_code == 200
    token = response.json()["access_token"]
    return f"Bearer {token}"


@pytest.fixture
async def test_position(client, auth_token):
    """Create a test position"""
    response = client.post(
        "/positions/",
        json={"position_name": "Test Developer"},
        headers={"Authorization": auth_token}
    )
    assert response.status_code == 201
    return response.json()


class TestAuthEndpoints:
    """Test authentication endpoints"""

    async def test_register_user_success(self, client, test_db):
        """Test successful user registration"""
        # Make sure database is initialized
        await test_db.initialize()
        
        # ตรวจสอบว่าตาราง users ถูกสร้างแล้วหรือไม่
        async with test_db.get_connection() as conn:
            cursor = await conn.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users';")
            table_exists = await cursor.fetchone()
            print(f"Table users exists: {table_exists is not None}")
            
            # ถ้าตารางมีอยู่แล้ว ให้ตรวจสอบว่ามีข้อมูลอะไรบ้าง
            if table_exists:
                cursor = await conn.execute("SELECT username FROM users;")
                users = await cursor.fetchall()
                print(f"Existing users: {users}")
        
        # สร้างชื่อผู้ใช้งานที่เป็นเอกลักษณ์มากขึ้น
        import uuid
        unique_username = f"test_user_{uuid.uuid4().hex[:8]}"
        print(f"Trying to register unique username: {unique_username}")
        
        response = client.post(
            "/auth/register",
            json={"username": unique_username, "password": "password123"}
        )
        
        print(f"Response status code: {response.status_code}")
        print(f"Response body: {response.json()}")
        
        assert response.status_code == 201
        assert response.json()["message"] == "User created successfully"

    def test_register_user_duplicate(self, client, test_db):
        """Test duplicate user registration"""
        # Register first user
        client.post(
            "/auth/register",
            json={"username": "testuser", "password": "password123"}
        )
        
        # Try to register again
        response = client.post(
            "/auth/register",
            json={"username": "testuser", "password": "password123"}
        )
        
        assert response.status_code == 400

    def test_login_success(self, client, test_db):
        """Test successful login"""
        # Register user first
        client.post(
            "/auth/register",
            json={"username": "testuser", "password": "password123"}
        )
        
        # Login
        response = client.post(
            "/auth/login",
            json={"username": "testuser", "password": "password123"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"

    def test_login_invalid_credentials(self, client, test_db):
        """Test login with invalid credentials"""
        response = client.post(
            "/auth/login",
            json={"username": "nonexistent", "password": "wrongpass"}
        )
        
        assert response.status_code == 401


class TestPositionEndpoints:
    """Test position endpoints"""

    def test_create_position_success(self, client, auth_token, test_db):
        """Test successful position creation"""
        response = client.post(
            "/positions/",
            json={"position_name": "Software Engineer"},
            headers={"Authorization": auth_token}
        )
        
        assert response.status_code == 201
        data = response.json()
        assert data["position_name"] == "Software Engineer"
        assert "position_id" in data

    def test_create_position_unauthorized(self, client, test_db):
        """Test position creation without auth"""
        response = client.post(
            "/positions/",
            json={"position_name": "Software Engineer"}
        )
        
        assert response.status_code == 403

    def test_get_position_success(self, client, auth_token, test_position, test_db):
        """Test successful position retrieval"""
        position_id = test_position["position_id"]
        
        response = client.get(
            f"/positions/{position_id}",
            headers={"Authorization": auth_token}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["position_id"] == position_id
        assert data["position_name"] == "Test Developer"

    def test_get_position_not_found(self, client, auth_token, test_db):
        """Test position retrieval when not found"""
        non_existent_id = str(uuid4())
        
        response = client.get(
            f"/positions/{non_existent_id}",
            headers={"Authorization": auth_token}
        )
        
        assert response.status_code == 404

    def test_get_all_positions(self, client, auth_token, test_position, test_db):
        """Test getting all positions"""
        response = client.get(
            "/positions/",
            headers={"Authorization": auth_token}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) >= 1

    def test_update_position_success(self, client, auth_token, test_position, test_db):
        """Test successful position update"""
        position_id = test_position["position_id"]
        
        response = client.put(
            f"/positions/{position_id}",
            json={"position_name": "Senior Developer"},
            headers={"Authorization": auth_token}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["position_name"] == "Senior Developer"

    def test_delete_position_success(self, client, auth_token, test_position, test_db):
        """Test successful position deletion"""
        position_id = test_position["position_id"]
        
        response = client.delete(
            f"/positions/{position_id}",
            headers={"Authorization": auth_token}
        )
        
        assert response.status_code == 204


class TestEmployeeEndpoints:
    """Test employee endpoints"""

    def test_create_employee_success(self, client, auth_token, test_position, test_db):
        """Test successful employee creation"""
        response = client.post(
            "/employees/",
            json={
                "name": "John Doe",
                "position_id": test_position["position_id"]
            },
            headers={"Authorization": auth_token}
        )
        
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == "John Doe"
        assert data["position_id"] == test_position["position_id"]
        assert data["position_name"] == "Test Developer"

    def test_create_employee_invalid_position(self, client, auth_token, test_db):
        """Test employee creation with invalid position"""
        non_existent_position_id = str(uuid4())
        
        response = client.post(
            "/employees/",
            json={
                "name": "John Doe",
                "position_id": non_existent_position_id
            },
            headers={"Authorization": auth_token}
        )
        
        assert response.status_code == 400

    def test_create_employee_unauthorized(self, client, test_position, test_db):
        """Test employee creation without auth"""
        response = client.post(
            "/employees/",
            json={
                "name": "John Doe",
                "position_id": test_position["position_id"]
            }
        )
        
        assert response.status_code == 403

    def test_get_employee_success(self, client, auth_token, test_position, test_db):
        """Test successful employee retrieval"""
        # Create employee first
        create_response = client.post(
            "/employees/",
            json={
                "name": "Jane Doe",
                "position_id": test_position["position_id"]
            },
            headers={"Authorization": auth_token}
        )
        employee = create_response.json()
        
        # Get employee
        response = client.get(
            f"/employees/{employee['emp_id']}",
            headers={"Authorization": auth_token}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Jane Doe"
        assert data["position_name"] == "Test Developer"

    def test_get_employee_not_found(self, client, auth_token, test_db):
        """Test employee retrieval when not found"""
        non_existent_id = str(uuid4())
        
        response = client.get(
            f"/employees/{non_existent_id}",
            headers={"Authorization": auth_token}
        )
        
        assert response.status_code == 404

    def test_get_all_employees(self, client, auth_token, test_position, test_db):
        """Test getting all employees"""
        # Create employee first
        client.post(
            "/employees/",
            json={
                "name": "Test Employee",
                "position_id": test_position["position_id"]
            },
            headers={"Authorization": auth_token}
        )
        
        response = client.get(
            "/employees/",
            headers={"Authorization": auth_token}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) >= 1

    def test_update_employee_success(self, client, auth_token, test_position, test_db):
        """Test successful employee update"""
        # Create employee first
        create_response = client.post(
            "/employees/",
            json={
                "name": "Original Name",
                "position_id": test_position["position_id"]
            },
            headers={"Authorization": auth_token}
        )
        employee = create_response.json()
        
        # Update employee
        response = client.put(
            f"/employees/{employee['emp_id']}",
            json={"name": "Updated Name"},
            headers={"Authorization": auth_token}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Updated Name"

    def test_delete_employee_success(self, client, auth_token, test_position, test_db):
        """Test successful employee deletion"""
        # Create employee first
        create_response = client.post(
            "/employees/",
            json={
                "name": "To Be Deleted",
                "position_id": test_position["position_id"]
            },
            headers={"Authorization": auth_token}
        )
        employee = create_response.json()
        
        # Delete employee
        response = client.delete(
            f"/employees/{employee['emp_id']}",
            headers={"Authorization": auth_token}
        )
        
        assert response.status_code == 204


class TestHealthEndpoints:
    """Test health check endpoints"""

    def test_root_endpoint(self, client):
        """Test root endpoint"""
        response = client.get("/")
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"

    def test_health_check_endpoint(self, client):
        """Test health check endpoint"""
        response = client.get("/health")
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert data["service"] == "Employee Management API"