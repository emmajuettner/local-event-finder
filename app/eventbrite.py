import requests
import json

from flask import current_app

BASE_URL="https://www.eventbriteapi.com/v3"

def get_auth():
    return "Bearer " + current_app.config["EVENTBRITE_API_KEY"]

def get_user():
    url = BASE_URL + "/users/me"
    headers = {"Authorization": get_auth(), "Content-Type" : "application/json"}
    response = requests.get(url, headers=headers)
    return response.json()["name"]

def get_user_events():
    user_venues = {"230819579" : "Eli Tea Bar", "99195019" : "Women & Children First"}
    user_events = []
    for venue_id in user_venues:
        venue_name = user_venues[venue_id]
        venue_events = get_venue_events(venue_id)
        for event_id in venue_events:
            event = venue_events[event_id]
            user_events.append({
                "venue_name" : venue_name,
                "name" : event["name"], 
                "start_time" : event["start_time"],
                "url" : event["url"],
                "venue_id" : event["venue_id"],
                "price" : event["price"],
            })
    return user_events

def get_user_organizations():
    """ Only returns organizations the user is a member of """
    url = BASE_URL + "/users/me/organizations/"
    headers = {"Authorization" : get_auth(), "Content-Type" : "application/json"}
    response = requests.get(url, headers=headers)
    print(response.json())
    organizations = response.json()["organizations"]
    user_orgs = {}
    for org in organizations:
        user_orgs[org["id"] : org["name"]]
    return user_orgs

def get_organization_events(org_id):
    url = BASE_URL + "/organizations/" + org_id + "/events/?order_by=start_asc&status=live&time_filter=current_future"
    headers = {"Authorization" : get_auth(), "Content-Type" : "application/json"}
    response = requests.get(url, headers=headers)
    events = response.json()["events"]
    return construct_event_list(events)
    
def get_venue_events(venue_id):
    url = BASE_URL + "/venues/" + venue_id + "/events/?order_by=start_asc&status=live"
    headers = {"Authorization" : get_auth(), "Content-Type" : "application/json"}
    response = requests.get(url, headers=headers)
    events = response.json()["events"]
    return construct_event_list(events)
    
def construct_event_list(event_json):
    """ Constructs a list of event objects based on the "events" json element from the API """
    events = {}
    for event in event_json:
        if event["online_event"] == True:
            continue # not including online events in the listing for now since the focus is on travel times
        if event_is_sold_out(event):
            continue # don't include sold out events
        events[event["id"]] = {
            "name" : event["name"]["text"], 
            "start_time" : event["start"]["local"],
            "url" : event["url"],
            "venue_id" : event["venue_id"],
            "price" : determine_ticket_price(event),
        }
    print(events)
    return events

def event_is_sold_out(event):
    return ("ticket_availability" in event
            and event["ticket_availability"] is not None
            and event["ticket_availability"]["is_sold_out"] == True)

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
            min_price = min_price_obj["major_price"]
        max_price_obj = event["ticket_availability"]["maximum_ticket_price"]
        if max_price_obj is not None:
            currency = max_price_obj["currency"]
            max_price = max_price_obj["major_price"]
    # try to get external ticketing details if applicable
    if "external_ticketing" in event and event["external_ticketing"] is not None:
        if event["external_ticketing"]["is_free"] is not None and event["external_ticketing"]["is_free"]:
            return "Free"
        min_price_obj = event["external_ticketing"]["minimum_ticket_price"]
        if min_price_obj is not None:
            currency = min_price_obj["currency"]
            min_price = min_price_obj["major_price"]
        max_price_obj = event["external_ticketing"]["maximum_ticket_price"]
        if max_price_obj is not None:
            currency = max_price_obj["currency"]
            max_price = max_price_obj["major_price"]
    # format the price range as a human readable string
    if currency is not None and min_price is not None and max_price is not None:
        price = "$" if currency == "USD" else ""
        if min_price == max_price:
            price += min_price
        else:
            price += min_price + "-" + max_price
        price += " " + currency if currency != "USD" else ""
        return price
    # if we still don't have all the price info at this stage, just don't display anything
    return ""
