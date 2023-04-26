from app.core.database import Base
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Text
from app.core.guid_type import GUID


class Game(Base):
    __tablename__ = "games"
    id = Column(GUID, primary_key=True, index=True)
    added = Column(DateTime)
    added_segment = Column(Integer)
    background_image = Column(String)
    description = Column(Text)
    notes = Column(Text)
    enable_system_hdr = Column(Boolean)
    name = Column(String)
