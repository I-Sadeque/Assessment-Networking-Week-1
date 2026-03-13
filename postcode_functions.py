"""Functions that interact with the Postcode API."""

import requests as req
import os
import json

CACHE_FILE = "./postcode_cache.json"


def load_cache() -> dict:
    """Loads the cache from a file and converts it from JSON to a dictionary."""

    if not os.path.exists(CACHE_FILE):
        return {}

    with open(CACHE_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def save_cache(cache: dict):
    """Saves the cache to a file as JSON"""

    with open(CACHE_FILE, "w", encoding="utf-8") as file:
        json.dump(cache, file)


def validate_postcode(postcode: str) -> bool:
    if not isinstance(postcode, str):
        raise TypeError("Function expects a string.")

    postcode = postcode.strip().upper()
    url = f"https://api.postcodes.io/postcodes/{postcode}/validate"
    response = req.get(url)

    if response.status_code >= 500:
        raise req.RequestException("Unable to access API.")

    data = response.json()

    return bool(data["result"])


def get_postcode_for_location(lat: float, long: float) -> str:
    """Gets the postcode from the URL"""

    if not isinstance(lat, float) or not isinstance(long, float):
        raise TypeError("Function expects two floats.")

    url = (f"https://api.postcodes.io/postcodes?lon={long}&lat={lat}")
    response = req.get(url)

    if response.status_code >= 500:
        raise req.RequestException("Unable to access API.")

    data = response.json()

    if data["result"] is None:
        raise ValueError("No relevant postcode found.")

    return data["result"][0]["postcode"]


def get_postcode_completions(postcode_start: str) -> list[str]:
    """Gets the postcode of the competed data"""

    if not isinstance(postcode_start, str):
        raise TypeError("Function expects a string.")

    url = (f"https://api.postcodes.io/postcodes/{postcode_start}/autocomplete")
    response = req.get(url)

    if response.status_code >= 500:
        raise req.RequestException("Unable to access API.")

    data = response.json()

    return data["result"]


def get_postcodes_details(postcodes: list[str]) -> dict:
    """collects postcode details"""

    if not isinstance(postcodes, list):
        raise TypeError("Function expects a list of strings.")

    for postcode in postcodes:
        if not isinstance(postcode, str):
            raise TypeError("Function expects a list of strings.")

    url = ("https://api.postcodes.io/postcodes")
    response = req.post(url, json={"postcodes": postcodes})

    if response.status_code >= 500:
        raise req.RequestException("Unable to access API.")

    data = response.json()

    return data["result"]
