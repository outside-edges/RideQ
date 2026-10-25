import os
from datetime import datetime
from dotenv import load_dotenv
from rwgps import rwgps_get_trips
from database_fill import insert_trips

load_dotenv()

trips = rwgps_get_trips()
# print(len(trips))

# ------------------------------------------------------------- #

# convert ISO strings to datetime


def convert_datetime(timestamp):
    """convert from ISO formatted string to datetime"""
    return datetime.fromisoformat(timestamp)

# ------------------------------------------------------------- #

# create RideQ trip structure from RWGPS trips


def transform_trip(rwgps_trip):
    """Transforms RWGPS trip into trip with limited keys and added level data"""

    rideq_trip = {
        "source_trip_id": rwgps_trip["id"],
        "name": rwgps_trip["name"],
        "description": rwgps_trip["description"],
        # "ride_category": ride_values[0],
        # "ride_classification": ride_values[1],
        "departed_at": convert_datetime(rwgps_trip["departed_at"]),
        "fit_sport": rwgps_trip["fit_sport"],
        "fit_sub_sport": rwgps_trip["fit_sub_sport"],
        "is_stationary": rwgps_trip["stationary"],
        "distance": rwgps_trip["distance"],
        "duration": rwgps_trip["duration"],
        "moving_time": rwgps_trip["moving_time"],
        "elevation_gain": rwgps_trip["elevation_gain"],
        "elevation_loss": rwgps_trip["elevation_loss"],
        "avg_speed": rwgps_trip["avg_speed"],
        "max_speed": rwgps_trip["max_speed"],
        "created_at": convert_datetime(rwgps_trip["created_at"]),
        "updated_at": convert_datetime(rwgps_trip["updated_at"]),
    }
    return rideq_trip

# ------------------------------------------------------------- #


# create new list for RideQ trips
rideq_trips = []

for trip in trips:
    new_rideq_trip = transform_trip(trip)
    rideq_trips.append(new_rideq_trip)

# ------------------------------------------------------------- #

# create list of trips sorted by departure datetime, ascending


def get_departed_datetime(trip):
    """Returns a rideq trip's departure datetime"""
    return trip["departed_at"]


sorted_trips = sorted(rideq_trips, key=get_departed_datetime)
insert_trips(sorted_trips, "RWGPS")
