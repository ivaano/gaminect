from app.api.endpoints import health
from app.core.routing import APIRouter

api_router = APIRouter()
api_router.include_router(health.router, tags=["health"])
