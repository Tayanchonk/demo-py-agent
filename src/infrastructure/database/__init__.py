import sqlite3
import aiosqlite
from typing import List, Optional
from uuid import UUID
from ...domain import Employee, Position, Address, EmployeeRepositoryInterface, PositionRepositoryInterface, AddressRepositoryInterface


class DatabaseConnection:
    """Database connection manager"""

    def __init__(self, db_path: str = "employees.db"):
        self.db_path = db_path

    async def initialize(self):
        """Initialize database tables"""
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(
                """
                CREATE TABLE IF NOT EXISTS positions (
                    position_id TEXT PRIMARY KEY,
                    position_name TEXT NOT NULL
                )
                """
            )
            await db.execute(
                """
                CREATE TABLE IF NOT EXISTS employees (
                    emp_id TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    position_id TEXT NOT NULL,
                    FOREIGN KEY (position_id) REFERENCES positions (position_id)
                )
                """
            )
            await db.execute(
                """
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    password_hash TEXT NOT NULL
                )
                """
            )
            await db.execute(
                """
                CREATE TABLE IF NOT EXISTS addresses (
                    address_id TEXT PRIMARY KEY,
                    employee_id TEXT NOT NULL,
                    street TEXT NOT NULL,
                    city TEXT NOT NULL,
                    state TEXT NOT NULL,
                    postal_code TEXT NOT NULL,
                    country TEXT NOT NULL,
                    FOREIGN KEY (employee_id) REFERENCES employees (emp_id)
                )
                """
            )
            await db.commit()

    def get_connection(self):
        """Get database connection"""
        return aiosqlite.connect(self.db_path)


class SQLiteEmployeeRepository(EmployeeRepositoryInterface):
    """SQLite implementation of Employee repository"""

    def __init__(self, db_connection: DatabaseConnection):
        self._db = db_connection

    async def create(self, employee: Employee) -> Employee:
        async with self._db.get_connection() as db:
            await db.execute(
                "INSERT INTO employees (emp_id, name, position_id) VALUES (?, ?, ?)",
                (str(employee.emp_id), employee.name, str(employee.position_id)),
            )
            await db.commit()
        return employee

    async def get_by_id(self, emp_id: UUID) -> Optional[Employee]:
        async with self._db.get_connection() as db:
            cursor = await db.execute(
                "SELECT emp_id, name, position_id FROM employees WHERE emp_id = ?",
                (str(emp_id),),
            )
            row = await cursor.fetchone()
            if row:
                return Employee(
                    emp_id=UUID(row[0]),
                    name=row[1],
                    position_id=UUID(row[2]),
                )
        return None

    async def get_all(self) -> List[Employee]:
        async with self._db.get_connection() as db:
            cursor = await db.execute(
                "SELECT emp_id, name, position_id FROM employees"
            )
            rows = await cursor.fetchall()
            return [
                Employee(
                    emp_id=UUID(row[0]),
                    name=row[1],
                    position_id=UUID(row[2]),
                )
                for row in rows
            ]

    async def update(self, employee: Employee) -> Optional[Employee]:
        async with self._db.get_connection() as db:
            await db.execute(
                "UPDATE employees SET name = ?, position_id = ? WHERE emp_id = ?",
                (employee.name, str(employee.position_id), str(employee.emp_id)),
            )
            await db.commit()
            if db.total_changes > 0:
                return employee
        return None

    async def delete(self, emp_id: UUID) -> bool:
        async with self._db.get_connection() as db:
            await db.execute("DELETE FROM employees WHERE emp_id = ?", (str(emp_id),))
            await db.commit()
            return db.total_changes > 0


class SQLitePositionRepository(PositionRepositoryInterface):
    """SQLite implementation of Position repository"""

    def __init__(self, db_connection: DatabaseConnection):
        self._db = db_connection

    async def create(self, position: Position) -> Position:
        async with self._db.get_connection() as db:
            await db.execute(
                "INSERT INTO positions (position_id, position_name) VALUES (?, ?)",
                (str(position.position_id), position.position_name),
            )
            await db.commit()
        return position

    async def get_by_id(self, position_id: UUID) -> Optional[Position]:
        async with self._db.get_connection() as db:
            cursor = await db.execute(
                "SELECT position_id, position_name FROM positions WHERE position_id = ?",
                (str(position_id),),
            )
            row = await cursor.fetchone()
            if row:
                return Position(
                    position_id=UUID(row[0]),
                    position_name=row[1],
                )
        return None

    async def get_all(self) -> List[Position]:
        async with self._db.get_connection() as db:
            cursor = await db.execute(
                "SELECT position_id, position_name FROM positions"
            )
            rows = await cursor.fetchall()
            return [
                Position(
                    position_id=UUID(row[0]),
                    position_name=row[1],
                )
                for row in rows
            ]

    async def update(self, position: Position) -> Optional[Position]:
        async with self._db.get_connection() as db:
            await db.execute(
                "UPDATE positions SET position_name = ? WHERE position_id = ?",
                (position.position_name, str(position.position_id)),
            )
            await db.commit()
            if db.total_changes > 0:
                return position
        return None

    async def delete(self, position_id: UUID) -> bool:
        async with self._db.get_connection() as db:
            await db.execute(
                "DELETE FROM positions WHERE position_id = ?", (str(position_id),)
            )
            await db.commit()
            return db.total_changes > 0
            
            
class SQLiteAddressRepository(AddressRepositoryInterface):
    """SQLite implementation of Address repository"""

    def __init__(self, db_connection: DatabaseConnection):
        self._db = db_connection

    async def create(self, address: Address) -> Address:
        async with self._db.get_connection() as db:
            await db.execute(
                """
                INSERT INTO addresses 
                (address_id, employee_id, street, city, state, postal_code, country) 
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    str(address.address_id),
                    str(address.employee_id),
                    address.street,
                    address.city,
                    address.state,
                    address.postal_code,
                    address.country,
                ),
            )
            await db.commit()
        return address

    async def get_by_id(self, address_id: UUID) -> Optional[Address]:
        async with self._db.get_connection() as db:
            cursor = await db.execute(
                """
                SELECT address_id, employee_id, street, city, state, postal_code, country 
                FROM addresses WHERE address_id = ?
                """,
                (str(address_id),),
            )
            row = await cursor.fetchone()
            if row:
                return Address(
                    address_id=UUID(row[0]),
                    employee_id=UUID(row[1]),
                    street=row[2],
                    city=row[3],
                    state=row[4],
                    postal_code=row[5],
                    country=row[6],
                )
        return None

    async def get_by_employee_id(self, employee_id: UUID) -> List[Address]:
        async with self._db.get_connection() as db:
            cursor = await db.execute(
                """
                SELECT address_id, employee_id, street, city, state, postal_code, country 
                FROM addresses WHERE employee_id = ?
                """,
                (str(employee_id),),
            )
            rows = await cursor.fetchall()
            return [
                Address(
                    address_id=UUID(row[0]),
                    employee_id=UUID(row[1]),
                    street=row[2],
                    city=row[3],
                    state=row[4],
                    postal_code=row[5],
                    country=row[6],
                )
                for row in rows
            ]

    async def get_all(self) -> List[Address]:
        async with self._db.get_connection() as db:
            cursor = await db.execute(
                """
                SELECT address_id, employee_id, street, city, state, postal_code, country 
                FROM addresses
                """
            )
            rows = await cursor.fetchall()
            return [
                Address(
                    address_id=UUID(row[0]),
                    employee_id=UUID(row[1]),
                    street=row[2],
                    city=row[3],
                    state=row[4],
                    postal_code=row[5],
                    country=row[6],
                )
                for row in rows
            ]

    async def update(self, address: Address) -> Optional[Address]:
        async with self._db.get_connection() as db:
            await db.execute(
                """
                UPDATE addresses 
                SET street = ?, city = ?, state = ?, postal_code = ?, country = ? 
                WHERE address_id = ?
                """,
                (
                    address.street,
                    address.city,
                    address.state,
                    address.postal_code,
                    address.country,
                    str(address.address_id),
                ),
            )
            await db.commit()
            if db.total_changes > 0:
                return address
        return None

    async def delete(self, address_id: UUID) -> bool:
        async with self._db.get_connection() as db:
            await db.execute(
                "DELETE FROM addresses WHERE address_id = ?", (str(address_id),)
            )
            await db.commit()
            return db.total_changes > 0