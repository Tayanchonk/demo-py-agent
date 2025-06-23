from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from uuid import UUID
from ...application import (
    EmployeeUseCase,
    EmployeeCreateDTO,
    EmployeeUpdateDTO,
    EmployeeResponseDTO,
)
from ..dependencies import get_employee_use_case, get_current_user


router = APIRouter(prefix="/employees", tags=["employees"])


@router.post(
    "/",
    response_model=EmployeeResponseDTO,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new employee",
)
async def create_employee(
    employee_data: EmployeeCreateDTO,
    employee_use_case: EmployeeUseCase = Depends(get_employee_use_case),
    current_user: str = Depends(get_current_user),
):
    """Create a new employee"""
    try:
        return await employee_use_case.create_employee(employee_data)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get(
    "/{emp_id}",
    response_model=EmployeeResponseDTO,
    summary="Get employee by ID",
)
async def get_employee(
    emp_id: UUID,
    employee_use_case: EmployeeUseCase = Depends(get_employee_use_case),
    current_user: str = Depends(get_current_user),
):
    """Get employee by ID"""
    employee = await employee_use_case.get_employee(emp_id)
    if not employee:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Employee not found"
        )
    return employee


@router.get(
    "/",
    response_model=List[EmployeeResponseDTO],
    summary="Get all employees",
)
async def get_all_employees(
    employee_use_case: EmployeeUseCase = Depends(get_employee_use_case),
    current_user: str = Depends(get_current_user),
):
    """Get all employees"""
    return await employee_use_case.get_all_employees()


@router.put(
    "/{emp_id}",
    response_model=EmployeeResponseDTO,
    summary="Update employee",
)
async def update_employee(
    emp_id: UUID,
    employee_data: EmployeeUpdateDTO,
    employee_use_case: EmployeeUseCase = Depends(get_employee_use_case),
    current_user: str = Depends(get_current_user),
):
    """Update employee"""
    try:
        employee = await employee_use_case.update_employee(emp_id, employee_data)
        if not employee:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Employee not found"
            )
        return employee
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.delete(
    "/{emp_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete employee",
)
async def delete_employee(
    emp_id: UUID,
    employee_use_case: EmployeeUseCase = Depends(get_employee_use_case),
    current_user: str = Depends(get_current_user),
):
    """Delete employee"""
    success = await employee_use_case.delete_employee(emp_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Employee not found"
        )