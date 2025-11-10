from flask import flash

def validate_input(start_address, mins_away):
    return (
        validate_start_address(start_address)
        and validate_mins_away(mins_away)
    )

def validate_start_address(start_address):
    """
    Validate that the start address provided is valid.
    
    Limiting to 300 chars - this is somewhat arbitrary, but most street
    addresses are much shorter than this, and it seems safest not to accept
    arbitrarily long data. Couldn't determine an upper limit for Google's 
    Routes API address field.
    """
    is_valid = True
    if start_address is None or len(start_address) == 0:
        flash("Address is a required field.")
    if len(start_address) > 300:
        flash("Address cannot be longer than 300 characters.")
        is_valid = False
    return is_valid

def validate_mins_away(mins_away):
    is_valid = True
    try:
        int(mins_away)
    except ValueError:
        flash("The number of minutes must be an integer.")
        is_valid = False
    return is_valid
