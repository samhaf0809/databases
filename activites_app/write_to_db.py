from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from models import Person, Activity, Location

# Create some instances of the Person class
people = [Person(first_name="Andrew", last_name="Dales"),
          Person(first_name="Chris", last_name="Brolin"),
          Person(first_name='Vera', last_name="Malcova"),
]

locations =[Location(room = "7"),
            Location(room = "Fives courts"),
            Location(room = "Senior Fields"),
            ]

chess = Activity(name="Chess",location=locations[0])
fives = Activity(name="Fives",location=locations[1])
outdoor_ed = Activity(name="Outdoor Ed",location=locations[2])
squash = Activity(name="Squash",location=locations[1])

people[0].activities.append(chess)
people[0].activities.append(fives)
people[1].activities.append(outdoor_ed)
people[1].activities.append(fives)
people[2].activities.append(squash)
people[2].activities.append(fives)


# Connect to the activities database
engine = create_engine('sqlite:///activities.sqlite', echo=True)

# Create a session and add the people to the database
with Session(engine) as sess:
    sess.add_all(people)
    sess.add_all(locations)
    sess.commit()