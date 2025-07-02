from pydantic import BaseModel, Field
from uuid import UUID
from typing import Optional


class EmployeeCreateDTO(BaseModel):
    """DTO for creating a new employee"""
    name: str = Field(..., min_length=1, max_length=100)
    position_id: UUID


class EmployeeUpdateDTO(BaseModel):
    """DTO for updating an employee"""
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    position_id: Optional[UUID] = None


class EmployeeResponseDTO(BaseModel):
    """DTO for employee response"""
    emp_id: UUID
    name: str
    position_id: UUID
    position_name: Optional[str] = None


class PositionCreateDTO(BaseModel):
    """DTO for creating a new position"""
    position_name: str = Field(..., min_length=1, max_length=100)


class PositionUpdateDTO(BaseModel):
    """DTO for updating a position"""
    position_name: str = Field(..., min_length=1, max_length=100)


class PositionResponseDTO(BaseModel):
    """DTO for position response"""
    position_id: UUID
    position_name: str


class LoginDTO(BaseModel):
    """DTO for login request"""
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=6)


class TokenResponseDTO(BaseModel):
    """DTO for token response"""
    access_token: str
    token_type: str = "bearer"


class UserCreateDTO(BaseModel):
    """DTO for creating a new user"""
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=6)
    
    
class AddressCreateDTO(BaseModel):
    """DTO for creating a new address"""
    employee_id: UUID
    street: str = Field(..., min_length=1, max_length=200)
    city: str = Field(..., min_length=1, max_length=100)
    state: str = Field(..., min_length=1, max_length=100)
    postal_code: str = Field(..., min_length=1, max_length=20)
    country: str = Field(..., min_length=1, max_length=100)


class AddressUpdateDTO(BaseModel):
    """DTO for updating an address"""
    street: Optional[str] = Field(None, min_length=1, max_length=200)
    city: Optional[str] = Field(None, min_length=1, max_length=100)
    state: Optional[str] = Field(None, min_length=1, max_length=100)
    postal_code: Optional[str] = Field(None, min_length=1, max_length=20)
    country: Optional[str] = Field(None, min_length=1, max_length=100)


class AddressResponseDTO(BaseModel):
    """DTO for address response"""
    address_id: UUID
    employee_id: UUID
    street: str
    city: str
    state: str
    postal_code: str
    country: str