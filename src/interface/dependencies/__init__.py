from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from ...infrastructure import (
    DatabaseConnection,
    SQLiteEmployeeRepository,
    SQLitePositionRepository,
    SQLiteAuthRepository,
    JWTService,
)
from ...application import (
    EmployeeUseCase,
    PositionUseCase,
    AuthUseCase,
)

# Security scheme
security = HTTPBearer()

# Configuration
SECRET_KEY = "your-secret-key-here-change-in-production"
DATABASE_PATH = "employees.db"

# Database connection
db_connection = DatabaseConnection(DATABASE_PATH)

# Services
jwt_service = JWTService(SECRET_KEY)

# Repositories
employee_repository = SQLiteEmployeeRepository(db_connection)
position_repository = SQLitePositionRepository(db_connection)
auth_repository = SQLiteAuthRepository(db_connection)

# Use cases
employee_use_case = EmployeeUseCase(employee_repository, position_repository)
position_use_case = PositionUseCase(position_repository)
auth_use_case = AuthUseCase(auth_repository, jwt_service)


async def get_database():
    """Get database connection dependency"""
    return db_connection


async def get_employee_use_case() -> EmployeeUseCase:
    """Get employee use case dependency"""
    return employee_use_case


async def get_position_use_case() -> PositionUseCase:
    """Get position use case dependency"""
    return position_use_case


async def get_auth_use_case() -> AuthUseCase:
    """Get auth use case dependency"""
    return auth_use_case


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> str:
    """Get current authenticated user"""
    token = credentials.credentials
    payload = jwt_service.verify_token(token)
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    username: str = payload.get("sub")
    if username is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return username