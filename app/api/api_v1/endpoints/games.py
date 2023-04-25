import logging

from fastapi import status, HTTPException
from app.schemas.games import Games

from app.core.routing import APIRouter

router = APIRouter()
logger = logging.getLogger('gaminect')


@router.post("", status_code=status.HTTP_202_ACCEPTED)
async def create_games(payload: Games):

    logger.info(f"Received {len(payload.games)} games to create")
    if len(payload.games) > 0:
        for game in payload.games:
            logger.info(f"Creating game {game.name}")
    return {"message": "Game created"}
