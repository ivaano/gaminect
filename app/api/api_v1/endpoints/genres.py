import logging

from fastapi import Depends, status
from sqlalchemy.orm import Session
from app.core import config
from app.core.routing import APIRouter
from app.core.database import get_db
from app.schemas.gaminect import Genre
from app.services.genre import GenreService

router = APIRouter()
logger = logging.getLogger(config.PROJECT_NAME)


@router.get("", response_model=list[Genre], status_code=status.HTTP_200_OK)
def get_genres(db: Session = Depends(get_db)):
    logger.info("Received request to get all genres")
    genres = GenreService(db).get_all()
    return genres

