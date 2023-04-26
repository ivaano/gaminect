from app.core.database import Base
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from app.core.guid_type import GUID


class Game(Base):
    __tablename__ = "games"
    id = Column(GUID, primary_key=True, index=True)
    added = Column(DateTime)
    added_segment = Column(Integer)
    name = Column(String)
