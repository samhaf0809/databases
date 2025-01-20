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


average_query = """
SELECT avg(age)
FROM students
WHERE gender = ?;
"""
average_age = cursor.execute(average_query, ('female',)).fetchone()[0]

group_by_query = """
SELECT gender, avg(age)
FROM students
GROUP BY gender
"""
average_age_by_gender = cursor.execute(group_by_query).fetchall()

# Question 7, 8, 9

j_firstname_query="""
SELECT firstname 
from students
where firstname like 'J%';
"""
j_firstname = cursor.execute(j_firstname_query).fetchmany(5)

num_per_gen_query = """
select count(gender), gender
from students 
group by gender;
"""
num_per_gender = cursor.execute(num_per_gen_query).fetchall()

sum_age_query = """
select substr(firstname,1,1), sum(age)
from students
group by substr(firstname,1,1);
"""
sum_age = cursor.execute(sum_age_query).fetchall()

conn.close()

print(first_students,"\n",more_students,"\n",other_students)

print(f"\nThe average age is {average_age}\n",average_age_by_gender)

print(j_firstname)

print(num_per_gender)

print(sum_age)