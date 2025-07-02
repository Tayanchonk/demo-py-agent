from .employee_controller import router as employee_router
from .position_controller import router as position_router
from .auth_controller import router as auth_router
from .address_controller import router as address_router
from .maintenance_controller import router as maintenance_router

__all__ = ["employee_router", "position_router", "auth_router", "address_router", "maintenance_router"]