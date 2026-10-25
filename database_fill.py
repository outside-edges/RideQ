from sqlalchemy import select
from database import engine, trip_table, trip_metadata_table, source_table, ride_level_table, organization_table, tag_table, trip_tag_table
from trip_assign_metadata import get_ride_type, get_organization, get_ride_level
from trip_assign_tags import get_trip_tags


# ------------------------------------------------------------- #
# INSERT SORTED_TRIPS INTO DATABASE
# ------------------------------------------------------------- #

def insert_trips(retrieved_trips, source_shortname):
    """Insert trips that do not already exist in RideQ database"""
    with engine.begin() as connection:
        source_id_query = select(source_table.c.source_id).where(
            source_table.c.shortname == source_shortname
        )  # Currently only source is Ride with GPS (shortname RWGPS, id 1)

        source_id = connection.execute(source_id_query).scalar_one()
        # scalar_one returns single value of source id, not entire row
        # results in error if multiple or DNE

        for trip in retrieved_trips:
            # create program-level check for if trip already exists in db
            # uses combo unique constraint of source_id & source_trip_id
            existing_trip_query = select(trip_table).where(
                trip_table.c.source_id == source_id,
                trip_table.c.source_trip_id == trip["source_trip_id"]
            )
            result = connection.execute(existing_trip_query)
            existing_trip = result.first()

            if existing_trip is None:
                # ------------------------------------------------------------- #
                # TRIP
                # ------------------------------------------------------------- #
                print("INSERTED: ", trip["source_trip_id"])
                insert_trip = trip_table.insert().values(
                    **trip,
                    source_id=source_id
                )
                result = connection.execute(insert_trip)
                new_trip_id = result.inserted_primary_key[0]

                # ------------------------------------------------------------- #
                # TRIP METADATA
                # ------------------------------------------------------------- #
                ride_type = get_ride_type(trip["name"])
                organization = get_organization(trip["name"])
                ride_level = get_ride_level(trip["name"])

                organization_id = None
                ride_level_id = None

                if organization is not None:
                    organization_id_query = select(organization_table.c.organization_id).where(
                        organization_table.c.name == organization
                    )

                    organization_id = connection.execute(
                        organization_id_query).scalar_one()

                if ride_level is not None:
                    ride_level_id_query = select(ride_level_table.c.ride_level_id).where(
                        ride_level_table.c.name == ride_level
                    )

                    ride_level_id = connection.execute(
                        ride_level_id_query).scalar_one()

                insert_metadata = trip_metadata_table.insert().values(
                    trip_id=new_trip_id,
                    ride_type=ride_type,
                    organization_id=organization_id,
                    ride_level_id=ride_level_id
                )
                connection.execute(insert_metadata)

                # ------------------------------------------------------------- #
                # TRIP TAGS
                # ------------------------------------------------------------- #
                trip_tags = get_trip_tags(trip["name"])

                for tag in trip_tags:
                    tag_id_query = select(tag_table.c.tag_id).where(
                        tag_table.c.name == tag
                    )

                    tag_id = connection.execute(tag_id_query).scalar_one()

                    insert_trip_tags = trip_tag_table.insert().values(
                        trip_id=new_trip_id,
                        tag_id=tag_id
                    )

                    connection.execute(insert_trip_tags)

# ------------------------------------------------------------- #
# ------------------------------------------------------------- #
# ------------------------------------------------------------- #
# ------------------------------------------------------------- #
# ------------------------------------------------------------- #
# ------------------------------------------------------------- #
# ------------------------------------------------------------- #
# ------------------------------------------------------------- #
# ------------------------------------------------------------- #
# ------------------------------------------------------------- #

            elif trip["updated_at"] > existing_trip.updated_at:
                print("UPDATED: ", trip["source_trip_id"])
                update_trip = trip_table.update().values(trip).where(
                    trip_table.c.source_id == source_id,
                    trip_table.c.source_trip_id == trip["source_trip_id"]
                )
                connection.execute(update_trip)

            else:
                print("SKIPPED: ", trip["source_trip_id"])
