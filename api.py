from fastapi import FastAPI
from sqlalchemy import select
from database import engine, trip_table

# create application instance
app = FastAPI()


# @ = decorator: registers function below as the handler for GET requests to the specified endpoint
@app.get("/")
def root():
    return {"message": "Welcome to RideQ"}


@app.get("/trips")
def database_get_trips():
    """Get trips data from database"""
    with engine.connect() as connection:
        trips_data = connection.execute(select(trip_table)).mappings().all()

    # create empty list, loop through rows, convert each row to dictionary, and add to list
    # NTS: entire right-hand side is evaled first, and only assigned to left-hand variable once fully evaled
    # similar to count = count ++
    trips_data = [dict(row) for row in trips_data]

    return trips_data
