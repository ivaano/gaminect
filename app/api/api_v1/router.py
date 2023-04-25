from app.core.routing import APIRouter
from app.api.api_v1.endpoints import games

api1_router = APIRouter()
api1_router.include_router(games.router, prefix="/games", tags=["games"])
