from fastapi import FastAPI
from sqlalchemy import select
from database import engine, trip_table, trip_metadata_table, ride_level_table, trip_tag_table, tag_table

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
        trips_data = connection.execute(
            select(
                trip_table,
                trip_metadata_table.c.ride_type.label("ride_type"),
                ride_level_table.c.name.label("ride_level")
            ).outerjoin(
                trip_metadata_table, trip_table.c.trip_id == trip_metadata_table.c.trip_id
            ).outerjoin(
                ride_level_table, trip_metadata_table.c.ride_level_id == ride_level_table.c.ride_level_id
            )
        ).mappings().all()

        tags_data = connection.execute(
            select(
                trip_tag_table.c.trip_id,
                tag_table.c.name
            ).join(
                tag_table, trip_tag_table.c.tag_id == tag_table.c.tag_id
            )
        ).mappings().all()

    # create empty list, loop through rows, convert each row to dictionary, and add to list
    # NTS: entire right-hand side is evaled first, and only assigned to left-hand variable once fully evaled
    # similar to count = count ++
    trips_data = [dict(row) for row in trips_data]
    tags_data = [dict(row) for row in tags_data]

    tags_by_trip = {}

    for trip_tag_pair in tags_data:
        if trip_tag_pair["trip_id"] not in tags_by_trip:
            tags_by_trip[trip_tag_pair["trip_id"]] = [trip_tag_pair["name"]]
        else:
            tags_by_trip[trip_tag_pair["trip_id"]].append(
                trip_tag_pair["name"])

    for trip in trips_data:
        trip["tags"] = tags_by_trip.get(trip["trip_id"], [])

    return trips_data
