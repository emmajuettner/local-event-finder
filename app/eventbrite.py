import requests
import datetime

from flask import current_app
from app import db

BASE_URL="https://www.eventbriteapi.com/v3"

def get_auth():
    return "Bearer " + current_app.config["EVENTBRITE_API_KEY"]

def refresh_eventbrite_data():
    """
    Calls the Eventbrite API to refresh our database cache if needed.
    
    Updates venue details and (TODO) will retrieve any new events belonging to them,
    if the venue was last updated more than a day ago.
    """
    refresh_venues()

def get_user():
    print("Retrieving user from Eventbrite API")
    url = BASE_URL + "/users/me"
    headers = {"Authorization": get_auth(), "Content-Type" : "application/json"}
    response = requests.get(url, headers=headers)
    return response.json()["name"]

def get_user_events():
    user_venues = get_all_venues()
    user_events = []
    for venue in user_venues:
        venue_id = venue["venue_id"]
        venue_name = venue["name"]
        venue_events = get_venue_events_paginated(venue_id)
        for event_id in venue_events:
            event = venue_events[event_id]
            user_events.append({
                "venue_name" : venue_name,
                "name" : event["name"], 
                "start_time" : event["start_time"],
                "url" : event["url"],
                "venue_id" : event["venue_id"],
                "price" : event["price"],
                "full_address" : venue["address_1"] + ", " + venue["city"] + ", " + venue["state"]
            })
    return user_events

def get_all_venues():
    return db.query_db("SELECT * FROM venue")

def get_user_organizations():
    """ Only returns organizations the user is a member of """
    print("Retrieving organizations for user from Eventbrite API")
    url = BASE_URL + "/users/me/organizations/"
    headers = {"Authorization" : get_auth(), "Content-Type" : "application/json"}
    response = requests.get(url, headers=headers)
    organizations = response.json()["organizations"]
    user_orgs = {}
    for org in organizations:
        user_orgs[org["id"] : org["name"]]
    return user_orgs

def get_organization_events(org_id):
    print("Retrieving events for organization from Eventbrite API")
    url = BASE_URL + "/organizations/" + org_id + "/events/?order_by=start_asc&status=live&time_filter=current_future"
    headers = {"Authorization" : get_auth(), "Content-Type" : "application/json"}
    response = requests.get(url, headers=headers)
    events = response.json()["events"]
    return construct_event_list(events)

def refresh_venues():
    """
    Check our cached list of venues and retrieve any that have not been updated in the past day.
    """
    for venue in db.query_db("""
        SELECT * FROM venue 
        WHERE (last_retrieved IS NULL OR last_retrieved < CURRENT_TIMESTAMP - 1)
    """):
        venue_latest = get_venue(venue["venue_id"])
        db.execute_sql("""
            UPDATE venue SET
            last_retrieved = CURRENT_TIMESTAMP,
            name = ?,
            address_1 = ?,
            city = ?,
            state = ?
            WHERE venue_id = ?
        """, args=[
            venue_latest["name"],
            venue_latest["address"]["address_1"],
            venue_latest["address"]["city"],
            venue_latest["address"]["region"],
            venue["venue_id"]
        ])

def get_venue(venue_id):
    print("Retrieving venue from Eventbrite API")
    url = BASE_URL + "/venues/" + venue_id
    headers = {"Authorization" : get_auth(), "Content-Type" : "application/json"}
    response = requests.get(url, headers=headers)
    return response.json()

def get_venue_events_paginated(venue_id):
    events = []
    has_more_items = True
    continuation = ""
    # Retrieve as many pages of events as exist for the venue
    while has_more_items:
        response = get_venue_events_single_page(venue_id, continuation)
        events += response.json()["events"]
        has_more_items = response.json()["pagination"]["has_more_items"]
        if "continuation" in response.json()["pagination"]:
            continuation = response.json()["pagination"]["continuation"]
    return construct_event_list(events)

def get_venue_events_single_page(venue_id, continuation=""):
    print("Retrieving events for venue from Eventbrite API")
    url = BASE_URL + "/venues/" + venue_id + "/events/?order_by=start_asc&status=live"
    if continuation != "":
        url += "&continuation=" + continuation
    headers = {"Authorization" : get_auth(), "Content-Type" : "application/json"}
    return requests.get(url, headers=headers)
    
def construct_event_list(event_json):
    """ Constructs a list of event objects based on the "events" json element from the API """
    events = {}
    current_datetime = datetime.datetime.now()
    for event in event_json:
        if event["status"] != "live":
            continue # don't include events that are completed, canceled, etc
        if event["online_event"]:
            continue # don't include online events in the listing for now since the focus is on travel times
        if event_is_sold_out(event):
            continue # don't include sold out events
        event_start_datetime = datetime.datetime.fromisoformat(event["start"]["local"])
        if event_start_datetime < current_datetime:
            continue # don't include past events
        if event_start_datetime > current_datetime + datetime.timedelta(days=14):
            continue # don't include events that are more than 2 weeks away
        events[event["id"]] = {
            "name" : event["name"]["text"], 
            "start_time" : event_start_datetime,
            "url" : event["url"],
            "venue_id" : event["venue_id"],
            "price" : determine_ticket_price(event),
        }
    return events

def event_is_sold_out(event):
    return ("ticket_availability" in event
            and event["ticket_availability"] is not None
            and event["ticket_availability"]["is_sold_out"])

def determine_ticket_price(event):
    """ 
    Returns a string describing the ticket price of an event.
    
    e.g. 'Free' or  '$5.99' or '$20-30' or '20-30 GBP'
    """
    if event["is_free"]:
        return "Free"
    min_price = None
    max_price = None
    currency = None
    # try to get the general Eventbrite ticketing details
    if "ticket_availability" in event and event["ticket_availability"] is not None:
        min_price_obj = event["ticket_availability"]["minimum_ticket_price"]
        if min_price_obj is not None:
            currency = min_price_obj["currency"]
            min_price = min_price_obj["major_value"]
        max_price_obj = event["ticket_availability"]["maximum_ticket_price"]
        if max_price_obj is not None:
            currency = max_price_obj["currency"]
            max_price = max_price_obj["major_value"]
    # try to get external ticketing details if applicable
    if "external_ticketing" in event and event["external_ticketing"] is not None:
        if event["external_ticketing"]["is_free"] is not None and event["external_ticketing"]["is_free"]:
            return "Free"
        min_price_obj = event["external_ticketing"]["minimum_ticket_price"]
        if min_price_obj is not None:
            currency = min_price_obj["currency"]
            min_price = min_price_obj["major_value"]
        max_price_obj = event["external_ticketing"]["maximum_ticket_price"]
        if max_price_obj is not None:
            currency = max_price_obj["currency"]
            max_price = max_price_obj["major_value"]
    # format the price range as a human readable string
    if currency is not None and min_price is not None and max_price is not None:
        price = "$" if currency == "USD" else ""
        min_price_str = format_number_with_optional_two_decimals(min_price)
        max_price_str = format_number_with_optional_two_decimals(max_price)
        if min_price == max_price:
            price += min_price_str
        else:
            price += min_price_str + "-" + max_price_str
        price += " " + currency if currency != "USD" else ""
        return price
    # if we still don't have all the price info at this stage, just don't display anything
    return ""

def format_number_with_optional_two_decimals(num):
    """ Formats a number so it either has two decimal places or none.
    
    E.g. 2.45 becomes "2.45", 5.5 becomes "5.50", 34 becomes "34" """
    if num.is_integer():
        return str(num)
    else:
        return '{0:.2f}'.format(num)
