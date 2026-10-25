import os
from urllib.parse import quote_plus
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy import MetaData, Table

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


# Tables needed for ingestion:
#   Trip:           captures incoming data
#   TripMetadata:   stores ride type, ride level, etc resulting from python algo
#   Source:         Trip references source_id from Source

trip_table = Table(
    "Trip",
    metadata,
    autoload_with=engine
)

trip_metadata_table = Table(
    "TripMetadata",
    metadata,
    autoload_with=engine
)

source_table = Table(
    "Source",
    metadata,
    autoload_with=engine
)

ride_level_table = Table(
    "RideLevel",
    metadata,
    autoload_with=engine
)

organization_table = Table(
    "Organization",
    metadata,
    autoload_with=engine
)

tag_table = Table(
    "Tag",
    metadata,
    autoload_with=engine
)

trip_tag_table = Table(
    "TripTag",
    metadata,
    autoload_with=engine
)

# for column in trip_table.columns:
#     print(column.name, column.type)
