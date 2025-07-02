# Interface layer exports
from .controllers import employee_router, position_router, auth_router, address_router, maintenance_router
from .dependencies import get_database, get_current_user

__all__ = [
    "employee_router",
    "position_router", 
    "auth_router",
    "address_router",
    "maintenance_router",
    "get_database",
    "get_current_user",
]