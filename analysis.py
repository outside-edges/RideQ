from sqlalchemy import select, func
from fill_database import engine, trips_table


# ------------------------------------------------------------- #
# ANALYSIS PLAYGROUND
# ------------------------------------------------------------- #

# TOTAL MILES
total_distance_query = select(func.sum(trips_table.c.distance))

with engine.connect() as connection:
    result = connection.execute(total_distance_query)
    total_distance = result.scalar()

print(total_distance)

total_distance_miles = total_distance / 1609.344
print(total_distance_miles)


# MILES BY YEAR
distance_by_year_query = select(
    func.year(trips_table.c.departed_at),
    func.sum(trips_table.c.distance),
).group_by(func.year(trips_table.c.departed_at))

with engine.connect() as connection:
    result = connection.execute(distance_by_year_query)
    distance_by_year = result.all()

print(distance_by_year)
