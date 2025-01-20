import sqlite3
from faker import Faker
import random

fake = Faker('en_GB')
parameterised_insert_query = """
INSERT INTO students (firstname,lastname,age,gender)
VALUES(?,?,?,?)
"""
conn = sqlite3.connect('students.sqlite')
cursor = conn.cursor()

fake.random.seed(4321)
random.seed(4321)
for _ in range(10):
    f_name = fake.first_name()
    l_name = fake.last_name()
    age = random.randint(11,18)
    gender = random.choice(('male','female'))
    cursor.execute(parameterised_insert_query, (f_name,l_name,age,gender))

conn.commit()
conn.close()