import sqlite3
conn=sqlite3.connect("sm_app.sqlite")
cursor = conn.cursor()

select_posts = """
select title, description
from posts
"""

select_post_likes="""
select description as Post, COUNT(likes.id) as Likes
from likes,posts
where posts.id = likes.post_id
group by likes.post_id
"""

select_name_inner = """
select users.name, posts.description
from users inner join posts on users.id = posts.user_id
order by users.name
"""

select_name_left = """
select users.name, posts.description
from users left join posts on users.id = posts.user_id
order by users.name
"""

posts=cursor.execute(select_posts).fetchall()
name_likes=cursor.execute(select_post_likes).fetchall()
name_inner=cursor.execute(select_name_inner).fetchall()
name_left=cursor.execute(select_name_left).fetchall()

print(posts)
print(name_likes)
print(name_inner)
print(name_left)

conn.close()

'''
select description
from posts
where description like '%?';

update users
set name = 'Lizzy'
where name = 'Elizabeth';

select users.name, count(posts.id)
from users inner join posts on users.id = posts.user_id
group by posts.id;


'''