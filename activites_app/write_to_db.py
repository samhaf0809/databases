from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from models import Person


andrew = Person(first_name="Andrew", last_name="Dales")
people = [Person(first_name="Chris", last_name="Broline"),Person(first_name="Vera", last_name="Malcova")]

engine = create_engine("sqlite:///activities.sqlite")

with Session(engine) as sess:
    sess.add(andrew)
    sess.add_all(people)
    sess.commit()

