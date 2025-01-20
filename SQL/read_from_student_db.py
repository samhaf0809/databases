import sqlite3
conn = sqlite3.connect('students.sqlite')
cursor = conn.cursor()

select_students = """
SELECT id,firstname,lastname
FROM students
WHERE age >= 15;
"""

cursor.execute(select_students)
first_students = cursor.fetchone()
more_students = cursor.fetchmany(10)
other_students = cursor.fetchall()
conn.close()

print(first_students,"\n",more_students,"\n",other_students)