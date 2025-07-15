from fastapi import FastAPI, Depends, WebSocket, WebSocketDisconnect
from fastapi.openapi.utils import get_openapi
from fastapi.staticfiles import StaticFiles
from src.auth import auth_routes
from src.tasks import task_routes
from src.notifications import notification_router
from src.database.db import Base, engine
from src.utils.security import get_current_user
from src.notifications.websocket_manager import manager

# Create DB tables
Base.metadata.create_all(bind=engine)

# App init
app = FastAPI(title="Task Manager")

app.mount("/static", StaticFiles(directory="static"), name="static")
# Routers
app.include_router(auth_routes.router)
app.include_router(task_routes.router)
app.include_router(notification_router.router)

# Custom Swagger JWT auth
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Task Manager",
        version="1.0.0",
        description="API for managing tasks with JWT authentication",
        routes=app.routes,
    )
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
        }
    }
    for path in openapi_schema["paths"].values():
        for method in path.values():
            method.setdefault("security", []).append({"BearerAuth": []})
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

# WebSocket Endpoint for Real-Time Notifications
@app.websocket("/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: int):
    await manager.connect(user_id, websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(user_id)
