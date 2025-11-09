import requests
import json

from flask import current_app

BASE_URL="https://routes.googleapis.com/directions/v2"

def get_auth():
    return current_app.config["GOOGLE_MAPS_API_KEY"]

def populate_events_with_transit_info(origin_address, events):
    for event in events:
        transit_info = get_transit_info(origin_address, event["full_address"])
        event["transit_duration"] = transit_info["duration"]
        transit_description = ""
        for step in transit_info["transit_steps"]:
            transit_description += " " + step["transit_emoji"] + " " + step["transit_name"]
        event["transit_description"] = transit_description
    return events
        

def get_transit_info(origin_address, destination_address):
    route_json = get_route(origin_address, destination_address)
    transit_duration = route_json["routes"][0]["localizedValues"]["duration"]["text"]
    steps = route_json["routes"][0]["legs"][0]["steps"]
    transit_steps = []
    for step in steps:
        if step["travelMode"] == "TRANSIT":
            transit_name = step["transitDetails"]["transitLine"]["nameShort"]
            transit_type = step["transitDetails"]["transitLine"]["vehicle"]["type"]
            transit_emoji = get_transit_emoji(transit_type)
            transit_steps.append({
                "transit_name" : transit_name, 
                "transit_emoji" : transit_emoji
            })
    return {"duration" : transit_duration, "transit_steps" : transit_steps}

def get_transit_emoji(transit_type):
    """
    Returns an emoji representation of the given transit type.
    
    Docs for possible transit types: https://googleapis.dev/python/routing/latest/routing_v2/types_.html#google.maps.routing_v2.types.TransitVehicle.TransitVehicleType
    """
    if transit_type in ["BUS", "INTERCITY_BUS"]:
        return "🚍"
    elif transit_type in ["METRO_RAIL", "SUBWAY", "TRAM"]:
        return "🚇"
    elif transit_type in ["COMMUTER_TRAIN", "HEAVY_RAIL", "HIGH_SPEED_TRAIN", "LONG_DISTANCE_TRAIN", "RAIL"]:
        return "🚆"
    elif transit_type in ["CABLE_CAR", "MONORAIL", "TROLLEYBUS"]:
        return "🚊"
    elif transit_type in ["FERRY"]:
        return "🚢"
    elif transit_type in ["FUNICULAR", "GONDOLA_LIFT"]:
        return "🚡"
    else:
        return "🚏"

def get_route(origin_address, destination_address):
    print("Retrieving route from Google Maps API")
    url = BASE_URL + ":computeRoutes"
    headers = {
        "X-Goog-Api-Key": get_auth(),
        "Content-Type" : "application/json",
        "X-Goog-FieldMask" : "routes.duration,routes.localizedValues,routes.legs.steps.transitDetails,routes.legs.steps.travelMode"}
    body = {
        "origin":{
            "address": origin_address
        },
        "destination":{
            "address": destination_address
        },
        "travelMode": "TRANSIT",
        "computeAlternativeRoutes" : False
    }
    response = requests.post(url, json=body, headers=headers)
    return response.json()
