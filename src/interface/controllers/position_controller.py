from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from uuid import UUID
from ...application import (
    PositionUseCase,
    PositionCreateDTO,
    PositionUpdateDTO,
    PositionResponseDTO,
)
from ..dependencies import get_position_use_case, get_current_user


router = APIRouter(prefix="/positions", tags=["positions"])


@router.post(
    "/",
    response_model=PositionResponseDTO,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new position",
)
async def create_position(
    position_data: PositionCreateDTO,
    position_use_case: PositionUseCase = Depends(get_position_use_case),
    current_user: str = Depends(get_current_user),
):
    """Create a new position"""
    return await position_use_case.create_position(position_data)


@router.get(
    "/{position_id}",
    response_model=PositionResponseDTO,
    summary="Get position by ID",
)
async def get_position(
    position_id: UUID,
    position_use_case: PositionUseCase = Depends(get_position_use_case),
    current_user: str = Depends(get_current_user),
):
    """Get position by ID"""
    position = await position_use_case.get_position(position_id)
    if not position:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Position not found"
        )
    return position


@router.get(
    "/",
    response_model=List[PositionResponseDTO],
    summary="Get all positions",
)
async def get_all_positions(
    position_use_case: PositionUseCase = Depends(get_position_use_case),
    current_user: str = Depends(get_current_user),
):
    """Get all positions"""
    return await position_use_case.get_all_positions()


@router.put(
    "/{position_id}",
    response_model=PositionResponseDTO,
    summary="Update position",
)
async def update_position(
    position_id: UUID,
    position_data: PositionUpdateDTO,
    position_use_case: PositionUseCase = Depends(get_position_use_case),
    current_user: str = Depends(get_current_user),
):
    """Update position"""
    position = await position_use_case.update_position(position_id, position_data)
    if not position:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Position not found"
        )
    return position


@router.delete(
    "/{position_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete position",
)
async def delete_position(
    position_id: UUID,
    position_use_case: PositionUseCase = Depends(get_position_use_case),
    current_user: str = Depends(get_current_user),
):
    """Delete position"""
    success = await position_use_case.delete_position(position_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Position not found"
        )