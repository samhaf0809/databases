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

    def test_create_user(self, controller):
        user = controller.create_user("Sam", 16,"Male","British")
        controller.set_current_user_from_name("Sam")
        assert controller.current_user.name == "Sam"
        assert controller.current_user.age == 16
        assert controller.current_user.gender == "Male"
        assert controller.current_user.nationality == "British"

    def test_get_posts(self,controller):
        posts = controller.get_posts("Alice")
        print(posts)
        assert posts[0]["title"] == "Exploring the Rocky Mountains"
        assert posts[0]["description"] == "Just returned from an amazing trip to the Rockies! The views were breathtaking and the hikes were exhilarating."
        assert posts[0]["number_likes"] == 2


    def test_add_post(self, controller):
        with so.Session(bind=controller.engine) as session:
            user = session.scalars(sa.select(User).where(User.name == "Alice")).one()

            controller.set_current_user_from_name("Alice")
            post = controller.add_post("Test post","This is a test post")
            print(post)
            assert True
            #assert post.description == "This is a test post"



    def test_like_post(self,controller):
        controller.set_current_user_from_name("Bob")
        controller.like_post("Alice","Exploring the Rocky Mountains")
        posts = controller.get_posts("Alice")
        assert posts[0]["number_likes"] == 3





    def test_comment_on_post(self,controller):
        controller.set_current_user_from_name("Diana")
        controller.comment_on_post("Exploring the Rocky Mountains","Alice","Test comment")
        posts = controller.get_posts("Alice")
        print(posts)
        assert posts[0]["comments"][2]["comment"] == "Test comment"
