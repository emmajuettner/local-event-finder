import eventbrite

def test_determine_ticket_price_returns_free_for_free_events():
    event = {
        "is_free" : True
        }
    price = eventbrite.determine_ticket_price(event)
    assert price == "Free"

def test_determine_ticket_price_returns_price_range_USD():
    event = {
        "is_free" : False,
        "ticket_availability" : {
            "minimum_ticket_price" : {
                "currency" : "USD",
                "value" : 550,
                "major_value" : 5.50,
                "display" : "5.50 USD"
            },
            "maximum_ticket_price" : {
                "currency" : "USD",
                "value" : 1000,
                "major_value" : 10,
                "display" : "10.00 USD"
            }
        }
    }
    price = eventbrite.determine_ticket_price(event)
    assert price == "$5.50-10"

def test_determine_ticket_price_returns_price_range_GBP():
    event = {
        "is_free" : False,
        "ticket_availability" : {
            "minimum_ticket_price" : {
                "currency" : "GBP",
                "value" : 599,
                "major_value" : 5.99,
                "display" : "5.99 GBP"
            },
            "maximum_ticket_price" : {
                "currency" : "GBP",
                "value" : 1000,
                "major_value" : 10,
                "display" : "10.00 GBP"
            }
        }
    }
    price = eventbrite.determine_ticket_price(event)
    assert price == "5.99-10 GBP"

def test_determine_ticket_price_returns_price_range_USD_externally_ticketed():
    event = {
        "is_free" : False,
        "external_ticketing" : {
            "is_free" : False,
            "minimum_ticket_price" : {
                "currency" : "USD",
                "value" : 550,
                "major_value" : 5.50,
                "display" : "5.50 USD"
            },
            "maximum_ticket_price" : {
                "currency" : "USD",
                "value" : 1000,
                "major_value" : 10,
                "display" : "10.00 USD"
            }
        }
    }
    price = eventbrite.determine_ticket_price(event)
    assert price == "$5.50-10"
