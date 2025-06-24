import aiosqlite
import bcrypt
import sqlite3
from jose import JWTError, jwt
from datetime import datetime, timedelta, timezone
from typing import Optional
from ...domain import AuthRepositoryInterface


class JWTService:
    """JWT token service"""

    def __init__(self, secret_key: str, algorithm: str = "HS256"):
        self.secret_key = secret_key
        self.algorithm = algorithm

    def create_access_token(self, data: dict, expires_delta: Optional[timedelta] = None):
        """Create JWT access token"""
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(hours=24)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
        return encoded_jwt

    def verify_token(self, token: str) -> Optional[dict]:
        """Verify JWT token"""
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            return payload
        except JWTError:
            return None


class SQLiteAuthRepository(AuthRepositoryInterface):
    """SQLite implementation of Auth repository"""

    def __init__(self, db_connection):
        self._db = db_connection

    def _hash_password(self, password: str) -> str:
        """Hash password using bcrypt"""
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

    def _verify_password(self, password: str, hashed_password: str) -> bool:
        """Verify password against hash"""
        return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))

    async def create_user(self, username: str, password: str) -> bool:
        """Create a new user"""
        try:
            hashed_password = self._hash_password(password)
            async with self._db.get_connection() as db:
                await db.execute(
                    "INSERT INTO users (username, password_hash) VALUES (?, ?)",
                    (username, hashed_password),
                )
                await db.commit()
            return True
        except aiosqlite.IntegrityError as e:
            # จัดการกรณีที่ username ซ้ำ
            print(f"IntegrityError in create_user: {str(e)}")
            return False
        except Exception as e:
            # ในกรณีที่เกิดข้อผิดพลาดอื่นๆ แสดงข้อมูลสำหรับ debug
            print(f"Error in create_user: {type(e).__name__}: {str(e)}")
            return False

    async def verify_user(self, username: str, password: str) -> bool:
        """Verify user credentials"""
        async with self._db.get_connection() as db:
            cursor = await db.execute(
                "SELECT password_hash FROM users WHERE username = ?",
                (username,),
            )
            row = await cursor.fetchone()
            if row:
                return self._verify_password(password, row[0])
        return False