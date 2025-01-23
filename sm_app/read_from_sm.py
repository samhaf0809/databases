import sqlite3
from multiprocessing import connection


def execute_read_query(connection, query):
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
    except sqlite3.Error as e:
        print(f"The error '{e}' occurred")
    return result

select_users = "SELECT * FROM users"
with sqlite3.connect("sm_app.sqlite") as conn:
    users = execute_read_query(conn, select_users)

for user in users:
    print(user)

print("")

select_posts = "SELECT * FROM posts"
posts = execute_read_query(conn, select_posts)
for post in posts:
    print(post)

print("")

select_users_posts = """
SELECT 
  users.id,users.name,
  posts.description
FROM 
  posts 
  INNER JOIN users ON users.id= posts.user_id
"""
users_posts = execute_read_query(conn, select_users_posts)
for users_post in users_posts:
    print(users_post)

print("")

select_posts_comments_user = """
SELECT 
  posts.description as post, 
  comments.text as comment, 
  users.name
FROM
  posts
  INNER JOIN comments ON posts.id = comments.post_id
  INNER JOIN users ON users.id = comments.user_id
"""

posts_comments_user = execute_read_query(conn, select_posts_comments_user)
for posts_comment in posts_comments_user:
    print(posts_comment)

print("")

with sqlite3.connect("sm_app.sqlite") as conn:
    cursor = conn.cursor()
    cursor.execute(select_posts_comments_user)
    cursor.fetchall()
    column_names = [description[0] for description in cursor.description]
print(column_names)