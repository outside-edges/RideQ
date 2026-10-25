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
