from cs50 import SQL

db = SQL('sqlite:///data.db')

# db.execute('DROP table users')
# db.execute("""
#            CREATE TABLE users (id INTEGER NOT NULL PRIMARY KEY,username VARCHAR(64), password STRING, email VARCHAR(64), tel INTEGER NOT NULL,confirmed BOOLEAN, adm BOOLEAN)
#            """)

db.execute('update users set adm = True where id = 1')