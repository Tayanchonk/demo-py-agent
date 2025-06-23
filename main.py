from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from src.interface import employee_router, position_router, auth_router
from src.interface.dependencies import get_database


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager"""
    # Startup
    db = await get_database()
    await db.initialize()
    yield
    # Shutdown (if needed)


app = FastAPI(
    title="Employee Management API",
    description="A RESTful API for employee management using Clean Architecture",
    version="1.0.0",
    lifespan=lifespan,
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify actual origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth_router)
app.include_router(employee_router)
app.include_router(position_router)


@app.get("/", tags=["health"])
async def root():
    """Health check endpoint"""
    return {"message": "Employee Management API is running", "status": "healthy"}


@app.get("/health", tags=["health"])
async def health_check():
    """Detailed health check"""
    return {
        "status": "healthy",
        "service": "Employee Management API",
        "version": "1.0.0",
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)