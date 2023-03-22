import sqlite3

db = sqlite3.connect("basetest8.db")
sql = db.cursor()

sql.execute("""CREATE TABLE IF NOT EXISTS users (
    Name TEXT,
    Price TEXT,
    Id Text

) """)




db.commit()



def save_n_p(name,price,str3):
    name_arr=[]

    sql.execute(f"INSERT INTO users VALUES (?, ?, ?)",(name, price, str3))
    db.commit()

def arr_str3():
    arr=[]
    for value in sql.execute("SELECT * FROM users"):
            arr.append(value[2])
    return arr
def arr_name():
    name=[]
    for value in sql.execute("SELECT * FROM users"):
            name.append(value[0])
    return name
def arr_price():
    price = []
    arr=[]
    for value in sql.execute("SELECT * FROM users"):
            price.append(int(value[1]))
    return price

for value in sql.execute("SELECT * FROM users"):
            print(value)

        








    
