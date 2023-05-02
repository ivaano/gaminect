from uuid import uuid4

from sqlalchemy.orm import relationship

from app.core.database import Base
from sqlalchemy import Column, func, Integer, String, Boolean, DateTime, ForeignKey, \
    Text
from app.core.guid_type import GUID


class Game(Base):
    __tablename__ = "games"
    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    playnite_id = Column(GUID)
    added = Column(DateTime)
    added_segment = Column(Integer)
    background_image = Column(String)
    description = Column(Text)
    notes = Column(Text)
    enable_system_hdr = Column(Boolean)
    name = Column(String)
    genres = relationship("Genre", secondary="game_genres", back_populates="games")


class GameGenre(Base):
    __tablename__ = "game_genres"
    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    game_id = Column(GUID, ForeignKey("games.playnite_id"))
    genre_id = Column(GUID, ForeignKey("genres.playnite_id"))
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())


class Genre(Base):
    __tablename__ = "genres"
    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    name = Column(String)
    playnite_id = Column(GUID)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    games = relationship("Game", secondary="game_genres", back_populates="genres")



