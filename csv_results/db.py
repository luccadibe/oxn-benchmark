import sqlite3
import pandas as pd

# Load CSV into Pandas DataFrame
csv_file = "clean.csv"
df = pd.read_csv(csv_file)

# Connect to SQLite Database
conn = sqlite3.connect("db.db")

# Load DataFrame into SQLite
df.to_sql("table_name", conn, if_exists="replace", index=False)

# Close the connection
conn.close()

