import sqlite3

conn = sqlite3.connect('social_media1.sqlite')
cursor = conn.cursor()

create_sm_table = """
CREATE TABLE IF NOT EXISTS social_media(
id integer PRIMARY KEY autoincrement,
username TEXT NOT NULL, 
post TEXT NOT NULL,
comment TEXT,
likes INTEGAR
);
"""
cursor.execute(create_sm_table)

parameterised_insert_query = """
INSERT INTO social_media(username, post, comment, likes)
values (?, ?, ?, ?);
"""


cursor.execute(parameterised_insert_query, ("sami","hi there","hi",4))
cursor.execute(parameterised_insert_query, ("dave","hi there",None,4))

conn.commit()
conn.close()