"""Determine ride type, organization, and level from trip names"""
import re


def get_ride_type(name):
    """Determines solo/group from trip name"""
    if "HBC" in name:
        return "Group"
    if "Solo" in name:
        return "Solo"
    if "Hershey Cycles" in name:
        return "Group"
    if "Group" in name:
        return "Group"
    if "with" in name:
        return "Group"
    return None


def get_organization(name):
    """Determines org name from trip name"""
    if "HBC" in name:
        return "Harrisburg Bicycle Club"
    if "Hershey Cycles" in name:
        return "Hershey Cycles"
    return None


def get_ride_level(name):
    """Determines ride level from trip name"""
    if "HBC" not in name:
        return None

    level_match = re.search(r"\b(B\+|C\+|Flex|B|C)(?!\w)", name)
    return level_match.group(1) if level_match else None
