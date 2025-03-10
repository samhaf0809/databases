import pytest
import sqlalchemy as sa
import sqlalchemy.orm as so
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from models import User, Post, Comment, Base

#test_db_location = "sqlite:///test.db"
test_db_location = "sqlite:///:memory:"


def test_test():
    assert 3**2 ==9

class TestDatabase:
    @pytest.fixture(scope='class')
    def db_session(self):
        engine = sa.create_engine(test_db_location)
        Base.metadata.create_all(engine)
        session = Session(engine)
        yield session
        session.close()
        Base.metadata.drop_all(engine)

    def test_valid_user(self, db_session):
        user = User(name = "sami", age = 16, gender = "male")
        db_session.add(user)
        db_session.commit()
        qry = sa.select(User).where(User.name == "sami")
        sami = db_session.scalar(qry)
        assert sami.name == "sami"
        assert sami.age == 16
        assert sami.gender == "male"
        assert sami.nationality is None