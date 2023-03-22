import sqlite3

db = sqlite3.connect("basetest2.db")
sql = db.cursor()

sql.execute("""CREATE TABLE IF NOT EXISTS users (
    Name TEXT,
    Price TEXT

) """)

db.commit()

for value in sql.execute("SELECT * FROM users"):
    print(value)

def save_n_p(name,price):
    name_arr=[]

    sql.execute(f"INSERT INTO users VALUES (?, ?)",(name, price))
    db.commit()

    for value in sql.execute("SELECT Name FROM users"):
        print(value)
save_n_p("Egg",'450') 



    