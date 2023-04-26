import logging

from fastapi import Depends, status
from sqlalchemy.orm import Session

from app.core import config
from app.core.database import get_db
from app.schemas.game import Games
from app.core.routing import APIRouter
from app.services.game import GameCrud

router = APIRouter()
logger = logging.getLogger(config.PROJECT_NAME)


@router.post("", status_code=status.HTTP_202_ACCEPTED)
def create_games(payload: Games, db: Session = Depends(get_db)):
    logger.info(f"Received {len(payload.games)} games to create")
    if len(payload.games) > 0:
        for game in payload.games:
            logger.info(f"Creating game {game.name}")
            result = GameCrud(db).upsert(game)

    return {"message": "Game created"}
