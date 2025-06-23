import pytest
from uuid import uuid4
from src.domain.entities import Employee, Position


class TestEmployee:
    """Test Employee entity"""

    def test_employee_creation_valid(self):
        """Test valid employee creation"""
        emp_id = uuid4()
        position_id = uuid4()
        employee = Employee(emp_id=emp_id, name="John Doe", position_id=position_id)
        
        assert employee.emp_id == emp_id
        assert employee.name == "John Doe"
        assert employee.position_id == position_id
        assert employee.position is None

    def test_employee_creation_with_position(self):
        """Test employee creation with position"""
        emp_id = uuid4()
        position_id = uuid4()
        position = Position(position_id=position_id, position_name="Developer")
        employee = Employee(
            emp_id=emp_id, 
            name="John Doe", 
            position_id=position_id, 
            position=position
        )
        
        assert employee.position == position

    def test_employee_empty_name_raises_error(self):
        """Test that empty name raises ValueError"""
        with pytest.raises(ValueError, match="Employee name cannot be empty"):
            Employee(emp_id=uuid4(), name="", position_id=uuid4())

    def test_employee_whitespace_name_raises_error(self):
        """Test that whitespace-only name raises ValueError"""
        with pytest.raises(ValueError, match="Employee name cannot be empty"):
            Employee(emp_id=uuid4(), name="   ", position_id=uuid4())


class TestPosition:
    """Test Position entity"""

    def test_position_creation_valid(self):
        """Test valid position creation"""
        position_id = uuid4()
        position = Position(position_id=position_id, position_name="Developer")
        
        assert position.position_id == position_id
        assert position.position_name == "Developer"

    def test_position_empty_name_raises_error(self):
        """Test that empty position name raises ValueError"""
        with pytest.raises(ValueError, match="Position name cannot be empty"):
            Position(position_id=uuid4(), position_name="")

    def test_position_whitespace_name_raises_error(self):
        """Test that whitespace-only position name raises ValueError"""
        with pytest.raises(ValueError, match="Position name cannot be empty"):
            Position(position_id=uuid4(), position_name="   ")