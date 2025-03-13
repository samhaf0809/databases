import pytest
import sqlalchemy as sa
import sqlalchemy.orm as so
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from social_media_3_3_3.models import User, Post, Comment, Base
from social_media_3_3_3.write_to_db import write_inital_data
from social_media_3_3_3.controller import Controller

test_db_location = "sqlite:///test_database.db"
#test_db_location = "sqlite:///:memory:"


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

    def test_invalid_user(self, db_session):
        user = User(age = 16, nationality = "british")
        db_session.add(user)
        with pytest.raises(IntegrityError):
            db_session.commit()
        db_session.rollback()

    def test_add_post(self,db_session):
        user = User(name = "sami", age = 16, gender = "male")
        post = Post(title="hello",description="hello world")
        user.posts.append(post)



class TestController:
    @pytest.fixture(scope='class', autouse=True)
    def test_db(self):
        engine = sa.create_engine(test_db_location)
        Base.metadata.create_all(engine)
        write_inital_data(engine)
        yield
        #After the fixture is used drop the data from the database
        Base.metadata.drop_all(engine)

    @pytest.fixture(scope='class')
    def controller(self):
        control = Controller(db_location=test_db_location)
        return control

    def test_set_current_user_from_name(self, controller):
        controller.set_current_user_from_name("Alice")
        assert controller.current_user.name == "Alice"
        assert controller.current_user.age == 30
        assert controller.current_user.id == 1
        assert controller.current_user.gender == "Female"

    def test_get_user_names(self, controller):
        assert controller.get_user_names() == ['Alice', 'Bob', 'Charlie', 'Diana']
        assert controller.get_user_names()[0] == "Alice"
        assert controller.get_user_names()[1] == "Bob"
        assert controller.get_user_names()[2] == "Charlie"
        assert controller.get_user_names()[3] == "Diana"

    def test_create_user(self):
        assert False

    def test_get_posts(self):
        assert False

    def test_add_post(self):
        assert False

    def test_like_post(self):
        assert False

    def test_comment_on_post(self):
        assert False
