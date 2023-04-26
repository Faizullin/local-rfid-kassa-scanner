import sqlite3, os, sys, requests

args = sys.argv
path = os.path.join('data', 'db.sqlite3')
if '-l' in args or '--load' in args:
    url = 'https://rfid-kassa.com/api/download-db'
    response = requests.get(url)
    if response.status_code == 200:
        with open(path, 'wb') as f:
            f.write(response.content)
            print(f'Downloaded db as {path} successfully.')
    else:
        print(f'Error downloading: {response.status_code}')
        sys.exit(1)

conn = sqlite3.connect(path)
alter_query = ''
alter_query += 'ALTER TABLE shop_app_product ADD COLUMN uhf_id VARCHAR NULL;'
alter_query += 'ALTER TABLE shop_app_customuser ADD COLUMN uhf_id VARCHAR NULL;'
conn.execute(alter_query)
conn.commit()
conn.close()