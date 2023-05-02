import pytest
from app.services.genre import GenreService
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from app.models.gaminect import Genre
from app.core.database import Base

engine = create_engine("sqlite:///./app-test.db",
                       pool_pre_ping=True,
                       echo=True, connect_args={"check_same_thread": False})

Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope='session')
def db_session():
    Base.metadata.create_all(engine)
    session = Session()
    yield session
    session.rollback()
    session.close()


@pytest.fixture(scope='module')
def valid_genre():
    valid_genre = Genre(name='Test Genre',
                        playnite_id='75412748d3584c42866d5d6c2f5c4ec2')
    db_session.add(valid_genre)
    db_session.commit()
    return valid_genre


class TestGenre:
    def test_valid_genre(self, db_session):
        assert db_session.query(Genre).filter(
            Genre.name == 'Test Genre').first() is not None

    def test_get_all(self, db_session):
        genres = GenreService(db_session).get_all()
        assert genres is not None
        assert db_session.query(Genre).all() is not None
