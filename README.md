# Employee Management API

A RESTful API for employee management built with Python, FastAPI, SQLite, and Clean Architecture principles.

## 🏗️ Architecture

This project follows **Clean Architecture** principles with clear separation of concerns across four layers:

### 1. Domain Layer (`src/domain/`)
- **Entities**: Core business entities (`Employee`, `Position`)
- **Interfaces**: Repository contracts defining data access patterns
- **Business Logic**: Domain rules and validation

### 2. Application Layer (`src/application/`)
- **Use Cases**: Business logic implementation (`EmployeeUseCase`, `PositionUseCase`, `AuthUseCase`)
- **DTOs**: Data Transfer Objects for API communication
- **Service Coordination**: Orchestrates domain entities and infrastructure

### 3. Infrastructure Layer (`src/infrastructure/`)
- **Database**: SQLite implementation of repository interfaces
- **Authentication**: JWT token management and user authentication
- **External Services**: Database connections and third-party integrations

### 4. Interface Layer (`src/interface/`)
- **Controllers**: FastAPI route handlers
- **Dependencies**: Dependency injection configuration
- **API Models**: Request/response serialization

## 🚀 Features

### Authentication System
- JWT-based authentication
- User registration and login
- Protected endpoints with token validation

### Employee Management
- Create, read, update, and delete employees
- Link employees to positions
- Full CRUD operations with validation

### Position Management
- Manage job positions/roles
- Create, read, update, and delete positions
- Referenced by employee records

### API Documentation
- Interactive Swagger/OpenAPI documentation
- Comprehensive endpoint descriptions
- Request/response schemas

## 🛠️ Technology Stack

- **Backend Framework**: FastAPI 0.104.1
- **Database**: SQLite with aiosqlite
- **Authentication**: JWT with python-jose
- **Password Hashing**: bcrypt
- **Testing**: pytest with asyncio support
- **API Documentation**: OpenAPI/Swagger (built-in)

## 📦 Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd demo-py-agent
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**:
   ```bash
   python main.py
   ```

The API will be available at `http://localhost:8000`

## 📚 API Documentation

Once the application is running, visit:
- **Interactive API Docs**: http://localhost:8000/docs
- **ReDoc Documentation**: http://localhost:8000/redoc

## 🔐 Authentication

### Register a new user
```bash
POST /auth/register
{
  "username": "your_username",
  "password": "your_password"
}
```

### Login to get access token
```bash
POST /auth/login
{
  "username": "your_username", 
  "password": "your_password"
}

Response:
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "token_type": "bearer"
}
```

### Use the token in requests
Include the token in the Authorization header:
```bash
Authorization: Bearer <your_access_token>
```

## 📖 API Endpoints

### Health Check
- `GET /` - Basic health check
- `GET /health` - Detailed health information

### Authentication
- `POST /auth/register` - Register new user
- `POST /auth/login` - Login and get access token

### Positions
- `POST /positions/` - Create new position
- `GET /positions/` - Get all positions
- `GET /positions/{position_id}` - Get position by ID
- `PUT /positions/{position_id}` - Update position
- `DELETE /positions/{position_id}` - Delete position

### Employees
- `POST /employees/` - Create new employee
- `GET /employees/` - Get all employees
- `GET /employees/{emp_id}` - Get employee by ID
- `PUT /employees/{emp_id}` - Update employee
- `DELETE /employees/{emp_id}` - Delete employee

## 💾 Database Schema

### Positions Table
```sql
CREATE TABLE positions (
    position_id TEXT PRIMARY KEY,
    position_name TEXT NOT NULL
);
```

### Employees Table
```sql
CREATE TABLE employees (
    emp_id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    position_id TEXT NOT NULL,
    FOREIGN KEY (position_id) REFERENCES positions (position_id)
);
```

### Users Table
```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL
);
```

## 🧪 Testing

Run the test suite:

```bash
# Run all tests
pytest

# Run unit tests only
pytest tests/unit/

# Run integration tests only
pytest tests/integration/

# Run with coverage
pytest --cov=src

# Run specific test file
pytest tests/unit/test_entities.py -v
```

### Test Structure
- **Unit Tests**: Test individual components in isolation
- **Integration Tests**: Test API endpoints and database interactions
- **Mocking**: External dependencies are mocked for reliable testing

## 📝 Example Usage

### 1. Register and Login
```bash
# Register
curl -X POST "http://localhost:8000/auth/register" \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "admin123"}'

# Login
curl -X POST "http://localhost:8000/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "admin123"}'
```

### 2. Create a Position
```bash
curl -X POST "http://localhost:8000/positions/" \
  -H "Authorization: Bearer <your_token>" \
  -H "Content-Type: application/json" \
  -d '{"position_name": "Software Engineer"}'
```

### 3. Create an Employee
```bash
curl -X POST "http://localhost:8000/employees/" \
  -H "Authorization: Bearer <your_token>" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "position_id": "uuid-from-previous-step"
  }'
```

## 🔧 Configuration

Key configuration options in `src/interface/dependencies/__init__.py`:

```python
SECRET_KEY = "your-secret-key-here-change-in-production"
DATABASE_PATH = "employees.db"
```

**Important**: Change the `SECRET_KEY` in production for security!

## 🗂️ Project Structure

```
demo-py-agent/
├── src/
│   ├── domain/
│   │   ├── entities/           # Business entities
│   │   └── interfaces/         # Repository interfaces
│   ├── application/
│   │   ├── dtos/              # Data transfer objects
│   │   └── use_cases/         # Business logic
│   ├── infrastructure/
│   │   ├── database/          # Database implementations
│   │   └── auth/              # Authentication services
│   └── interface/
│       ├── controllers/        # API controllers
│       └── dependencies/       # Dependency injection
├── tests/
│   ├── unit/                  # Unit tests
│   └── integration/           # Integration tests
├── main.py                    # Application entry point
├── requirements.txt           # Dependencies
└── README.md                 # This file
```

## 🚦 Development

### Code Style
- Follow PEP 8 Python style guidelines
- Use type hints for better code documentation
- Implement proper error handling and validation

### Contributing
1. Fork the repository
2. Create a feature branch
3. Make your changes with tests
4. Ensure all tests pass
5. Submit a pull request

## 📄 License

This project is created for demonstration purposes.

## 🔮 Future Enhancements

- [ ] Add role-based access control (RBAC)
- [ ] Implement employee search and filtering
- [ ] Add employee performance metrics
- [ ] Create department management
- [ ] Add file upload for employee photos
- [ ] Implement audit logging
- [ ] Add email notifications
- [ ] Create reporting dashboard