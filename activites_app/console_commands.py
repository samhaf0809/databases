from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session
from models import Person

engine = create_engine('sqlite:///activities.sqlite', echo=True)

sess = Session(engine)
