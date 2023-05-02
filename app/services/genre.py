from typing import Type

from sqlalchemy import func, Row

from app.models.gaminect import Game, Genre
from app.services.main import AppService


class GenreService(AppService):
    def get_all(self) -> list[Type[Genre]]:
        return self.db.query(Genre.id, Genre.name, Genre.playnite_id, func.count(Game.id).label('game_count')) \
            .join(Genre.games).group_by(Genre.id).all()
