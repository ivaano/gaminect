from typing import Type

from sqlalchemy.orm import joinedload

from app.core.guid_type import GUID
from app.schemas.playnite import Game
from app.models.gaminect import Game as GameModel, Genre
from app.services.main import AppService


class GameService(AppService):
    def get(self, game_id: GUID) -> Type[GameModel] | None:
        return self.db.query(GameModel).filter(GameModel.id == game_id).first()

    def get_by_name(self, name: str) -> GameModel:
        return self.db.query(GameModel).filter(GameModel.name == name).first()

    def get_all(self) -> list[Type[GameModel]]:
        return self.db.query(GameModel).options(joinedload(GameModel.genres)).all()

    def create(self, game: Game) -> GameModel:
        game_row = GameModel(id=game.id, name=game.name)
        self.db.add(game_row)
        self.db.commit()
        self.db.refresh(game_row)
        return game_row

    def upsert(self, game: Game) -> GameModel:

        game_row = GameModel(
            playnite_id=game.id,
            added=game.added,
            added_segment=game.added_segment,
            background_image=game.background_image,
            description=game.description,
            notes=game.notes,
            enable_system_hdr=game.enable_system_hdr,
            name=game.name)

        if game.genres:
            for genre in game.genres:
                genre_row = self.db.query(Genre).filter(Genre.playnite_id == genre.id).first()
                if genre_row is None:
                    genre_row = Genre(name=genre.name, playnite_id=genre.id)
                    self.db.add(genre_row)
                    self.db.commit()
                    self.db.refresh(genre_row)
                game_row.genres.append(genre_row)

        self.db.merge(game_row)
        self.db.commit()
        return game_row

    def update(self, game: Game) -> GameModel:
        self.db.add(game)
        self.db.flush()
        return game

    def delete(self, game_id: GUID) -> None:
        self.db.query(Game).filter(Game.id == game_id).delete()
        self.db.flush()
