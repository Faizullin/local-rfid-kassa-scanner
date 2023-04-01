from src.sql_db import ProductDatabase

if __name__ == "__main__":
    path = "db.sqlite3"
    db = ProductDatabase(path)
    print(db.select_all_by_ids(['1','2']))
    