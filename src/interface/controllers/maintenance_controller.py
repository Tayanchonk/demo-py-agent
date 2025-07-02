from fastapi import APIRouter, Depends, status
from ..dependencies import get_database, get_current_user
import aiosqlite


router = APIRouter(prefix="/maintenance", tags=["maintenance"])


@router.post(
    "/vacuum",
    status_code=status.HTTP_200_OK,
    summary="Optimize database with VACUUM command",
)
async def vacuum_database(
    current_user: str = Depends(get_current_user),
    db = Depends(get_database),
):
    """
    Run SQLite VACUUM command to rebuild the database, reclaiming unused space and
    reducing fragmentation. This improves performance and reduces the database file size.
    
    This operation requires authentication and may take time on large databases.
    """
    try:
        async with db.get_connection() as conn:
            await conn.execute("VACUUM")
            await conn.commit()
        
        return {"status": "success", "message": "Database optimized successfully"}
    except aiosqlite.Error as e:
        return {
            "status": "error", 
            "message": f"Failed to optimize database: {str(e)}"
        }
