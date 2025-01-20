import sqlite3


conn = sqlite3.connect('students.sqlite')
cursor = conn.cursor()

insert_query = """
INSERT INTO students (firstname,lastname,age,gender)
VALUES ('Hermione','Grainger',14,'female');
"""
parameterised_insert_query="""
INSERT INTO students (firstname,lastname,age,gender)
VALUES(?,?,?,?);
"""


cursor.execute(insert_query)
cursor.execute(parameterised_insert_query,("Harry","Potter",13,"male"))


conn.commit()
conn.close()
