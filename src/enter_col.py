import sqlite3

# Open a connection to the database file
conn = sqlite3.connect('db.sqlite3')

# Define the SQL query to add a new column to the table
alter_query = 'ALTER TABLE shop_app_product ADD COLUMN uhf_id VARCHAR NULL'

# Execute the SQL query
conn.execute(alter_query)

# Commit the changes to the database
conn.commit()

# Close the database connection
conn.close()