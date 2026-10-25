"""Determine trip tag(s) from trip names"""
import re

available_tags = ["Warmup", "Commute", "Recovery", "Training", "Hilly", "Flat"]


def get_trip_tags(name):
    """Determines trip tag(s) from tip name"""
    trip_tags = []

    for tag in available_tags:
        if tag in name:
            trip_tags.append(tag)

    if any(phrase in name for phrase in ("Ride to", "Ride from", "Ride to/from")):
        if "Commute" not in trip_tags:
            trip_tags.append("Commute")

    return trip_tags

# def get_ride_type(name):
#     """Determines solo/group from trip name"""
#     if "HBC" in name:
#         return "Group"
#     if "Solo" in name:
#         return "Solo"
#     if "Hershey Cycles" in name:
#         return "Group"
#     if "Group" in name:
#         return "Group"
#     if "with" in name:
#         return "Group"
#     return None


# def get_organization(name):
#     """Determines org name from trip name"""
#     if "HBC" in name:
#         return "Harrisburg Bicycle Club"
#     if "Hershey Cycles" in name:
#         return "Hershey Cycles"
#     return None


# def get_ride_level(name):
#     """Determines ride level from trip name"""
#     if "HBC" not in name:
#         return None

#     level_match = re.search(r"\b(B\+|C\+|Flex|B|C)(?!\w)", name)
#     return level_match.group(1) if level_match else None
