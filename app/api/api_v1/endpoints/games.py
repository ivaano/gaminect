import logging

from fastapi import Depends, status
from sqlalchemy.orm import Session

from app.core import config
from app.core.database import get_db
from app.schemas.playnite import Games as GamesPlaynite
from app.schemas.gaminect import Game
from app.core.routing import APIRouter
from app.services.game import GameService

router = APIRouter()
logger = logging.getLogger(config.PROJECT_NAME)


@router.get("", response_model=list[Game], status_code=status.HTTP_200_OK)
def get_games(db: Session = Depends(get_db)):
    logger.info("Received request to get all games")
    games = GameService(db).get_all()
    return games


@router.post("", status_code=status.HTTP_202_ACCEPTED)
def create_games(payload: GamesPlaynite, db: Session = Depends(get_db)):
    logger.info(f"Received {len(payload.games)} games to create")
    if len(payload.games) > 0:
        for game in payload.games:
            logger.info(f"Creating game {game.name}")
            result = GameService(db).upsert(game)

    return {"message": "Game created"}
