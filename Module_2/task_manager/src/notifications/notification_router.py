from fastapi import APIRouter, Depends
from src.utils.security import get_current_user
from src.notifications.websocket_manager import manager

router = APIRouter(prefix="/notifications", tags=["Notifications"])

@router.post("/broadcast")
async def broadcast_notification(message: str, user=Depends(get_current_user)):
    """
    Broadcast a message to all connected users (for testing/demo).
    """
    await manager.broadcast(f"Broadcast from {user.username}: {message}")
    return {"msg": "Message broadcasted"}

@router.post("/personal")
async def personal_notification(message: str, user=Depends(get_current_user)):
    """
    Send a personal notification to the current user.
    """
    await manager.send_personal_message(str(user.id), f"{message}")
    return {"msg": "Personal message sent"}
