from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from model_sm import User, Post

users = [User(username="Sbeve"),
         User(username="Krill"),
         User(username="MushyMan"),
         ]

posts =[Post(user_id=users[0], post="Hi")]




engine = create_engine('sqlite:///activities.sqlite', echo=True)

# Create a session and add the people to the database
with Session(engine) as sess:
    sess.add_all(users)
    sess.add_all(posts)
    sess.commit()


