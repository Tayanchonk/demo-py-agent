from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from uuid import UUID
from ...application import (
    AddressUseCase,
    AddressCreateDTO,
    AddressUpdateDTO,
    AddressResponseDTO,
)
from ..dependencies import get_address_use_case, get_current_user


router = APIRouter(prefix="/addresses", tags=["addresses"])


@router.post(
    "/",
    response_model=AddressResponseDTO,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new address",
)
async def create_address(
    address_data: AddressCreateDTO,
    address_use_case: AddressUseCase = Depends(get_address_use_case),
    current_user: str = Depends(get_current_user),
):
    """Create a new address"""
    try:
        return await address_use_case.create_address(address_data)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get(
    "/{address_id}",
    response_model=AddressResponseDTO,
    summary="Get address by ID",
)
async def get_address(
    address_id: UUID,
    address_use_case: AddressUseCase = Depends(get_address_use_case),
    current_user: str = Depends(get_current_user),
):
    """Get address by ID"""
    address = await address_use_case.get_address(address_id)
    if not address:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Address not found"
        )
    return address


@router.get(
    "/employee/{employee_id}",
    response_model=List[AddressResponseDTO],
    summary="Get addresses by employee ID",
)
async def get_addresses_by_employee(
    employee_id: UUID,
    address_use_case: AddressUseCase = Depends(get_address_use_case),
    current_user: str = Depends(get_current_user),
):
    """Get addresses by employee ID"""
    try:
        return await address_use_case.get_addresses_by_employee(employee_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get(
    "/",
    response_model=List[AddressResponseDTO],
    summary="Get all addresses",
)
async def get_all_addresses(
    address_use_case: AddressUseCase = Depends(get_address_use_case),
    current_user: str = Depends(get_current_user),
):
    """Get all addresses"""
    return await address_use_case.get_all_addresses()


@router.put(
    "/{address_id}",
    response_model=AddressResponseDTO,
    summary="Update address",
)
async def update_address(
    address_id: UUID,
    address_data: AddressUpdateDTO,
    address_use_case: AddressUseCase = Depends(get_address_use_case),
    current_user: str = Depends(get_current_user),
):
    """Update address"""
    address = await address_use_case.update_address(address_id, address_data)
    if not address:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Address not found"
        )
    return address


@router.delete(
    "/{address_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete address",
)
async def delete_address(
    address_id: UUID,
    address_use_case: AddressUseCase = Depends(get_address_use_case),
    current_user: str = Depends(get_current_user),
):
    """Delete address"""
    success = await address_use_case.delete_address(address_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Address not found"
        )
