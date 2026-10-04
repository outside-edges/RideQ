import os
from urllib.parse import quote_plus
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy import MetaData, Table
from sqlalchemy import select

load_dotenv()

rideq_db_server = os.getenv("RIDEQ_DB_SERVER")


# ------------------------------------------------------------- #
# CONNECT TO DATABASE
# ------------------------------------------------------------- #
db_connection_string = (
    "DRIVER={ODBC Driver 17 for SQL Server};"
    f"SERVER={rideq_db_server};"
    "DATABASE=RideQ;"
    "Trusted_Connection=yes;"
)

connection_url = (
    "mssql+pyodbc:///?odbc_connect="
    + quote_plus(db_connection_string)
)

engine = create_engine(connection_url)
metadata = MetaData()

trips_table = Table(
    "Trips",
    metadata,
    autoload_with=engine
)

# for column in trips_table.columns:
#     print(column.name, column.type)


# ------------------------------------------------------------- #
# INSERT SORTED_TRIPS INTO DATABASE
# ------------------------------------------------------------- #
def insert_trips(trips):
    """Insert trips that do not already exist in RideQ database"""
    for trip in trips:
        # create program-level check for if trip already exists in db
        existing_trip_query = select(trips_table).where(
            trips_table.c.rwgps_trip_id == trip["rwgps_trip_id"]
        )

        with engine.connect() as connection:
            result = connection.execute(existing_trip_query)
            existing_trip = result.first()

            if existing_trip is None:
                insert_trip = trips_table.insert().values(trip)

                connection.execute(insert_trip)
                connection.commit()
            else:
                print(existing_trip)
