from typing import Type

from app.core.guid_type import GUID
from app.schemas.game import Game
from app.models.game import Game as GameModel
from app.services.main import AppCrud


class GameCrud(AppCrud):
    def get(self, game_id: GUID) -> Type[GameModel] | None:
        return self.db.query(Game).filter(GameModel.id == game_id).first()

    def get_by_name(self, name: str) -> GameModel:
        return self.db.query(Game).filter(GameModel.name == name).first()

    def get_all(self) -> list[Type[GameModel]]:
        return self.db.query(GameModel).all()

    def create(self, game: Game) -> GameModel:
        game_row = GameModel(id=game.id, name=game.name)
        self.db.add(game_row)
        self.db.commit()
        self.db.refresh(game_row)
        return game_row

    def update(self, game: Game) -> GameModel:
        self.db.add(game)
        self.db.flush()
        return game

    def delete(self, game_id: GUID) -> None:
        self.db.query(Game).filter(Game.id == game_id).delete()
        self.db.flush()
