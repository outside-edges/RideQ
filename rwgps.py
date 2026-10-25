import os
from dotenv import load_dotenv
import requests

load_dotenv()

# ENDPOINTS
RWGPS_BASE_URL = "https://ridewithgps.com/api/v1"
ENDPOINT_TRIPS = "/trips.json"

# ------------------------------------------------------------- #
# RWGPS CREDENTIALS
# ------------------------------------------------------------- #
rwgps_api_key = os.getenv("RWGPS_API_KEY")
rwgps_auth_token = os.getenv("RWGPS_AUTH_TOKEN")


# ------------------------------------------------------------- #
# GET TRIPS
# ------------------------------------------------------------- #
# RWGPS QUIRK: trips[0] is the most recently updated trip, not trip with most recent departed_at

def rwgps_get_trips():
    """Get list of trip dictionaries from RWGPS"""
    rwgps_headers = {
        "x-rwgps-api-key": rwgps_api_key,
        "x-rwgps-auth-token": rwgps_auth_token,
    }

    trips_response = requests.get(
        url=f"{RWGPS_BASE_URL}{ENDPOINT_TRIPS}",
        headers=rwgps_headers,
        timeout=10
    )

    trips_data = trips_response.json()
    trips = trips_data["trips"]
    trips_pagination = trips_data["meta"]["pagination"]

    next_page_url = trips_pagination["next_page_url"]

    while next_page_url:
        next_page_response = requests.get(
            url=next_page_url,
            headers=rwgps_headers,
            timeout=10
        )
        next_page_data = next_page_response.json()
        trips.extend(next_page_data["trips"])
        next_page_url = next_page_data["meta"]["pagination"]["next_page_url"]

    return trips
