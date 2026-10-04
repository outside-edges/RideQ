import os
import pyodbc
from dotenv import load_dotenv

load_dotenv()

# ------------------------------------------------------------- #
# DATABASE CONNECTION
# ------------------------------------------------------------- #
rideq_db_server = os.getenv("RIDEQ_DB_SERVER")

db_connection_string = (
    "DRIVER={ODBC Driver 17 for SQL Server};"
    f"SERVER={rideq_db_server};"
    "DATABASE=master;"
    "Trusted_Connection=yes;"
)

connection = pyodbc.connect(db_connection_string, autocommit=True)

with open("sql/create_database.sql", "r") as file:
    sql_script = file.read()

sql_batches = sql_script.split("\nGO\n")

cursor = connection.cursor()
for batch in sql_batches:
    cursor.execute(batch)

cursor.close()
connection.close()
