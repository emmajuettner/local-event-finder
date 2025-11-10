import os

from flask import Flask, render_template, request, redirect, url_for
from dotenv import dotenv_values
from app import db
from app import eventbrite
from app import maps
from app import input_validation

def create_app(test_config=None):
    # set up flask app & configs
    app = Flask(__name__, instance_relative_config=True)
    config = dotenv_values(".env")
    app.config.from_mapping(config)
    app.config.from_mapping(
        DATABASE=os.path.join(app.instance_path, config["DATABASE_FILENAME"]),
    )
    
    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
        
    @app.route("/", methods=["GET"])
    def index_get():
        return render_template("index.html", events=[])

    @app.route("/", methods=["POST"])
    def index_post():
        # Validate input data
        form_data = request.form
        start_location = form_data["startLocation"].strip()
        mins_away = form_data["minsAway"].strip()
        is_input_valid = input_validation.validate_input(start_location, mins_away)
        if not is_input_valid:
            return redirect(url_for('index_get'))
        
        # Refresh our cache if needed
        eventbrite.refresh_eventbrite_data()
        
        # Retrieve events corresponding to the user's request
        user_events = eventbrite.get_user_events()
        events_with_transit_info = maps.populate_events_with_transit_info(
            start_location,
            mins_away,
            user_events
        )
        
        # Sort the events, soonest date first
        events_sorted = sorted(events_with_transit_info, key=lambda event: event["start_time"])
        
        # Render the results
        return render_template(
            "index.html", 
            events=events_sorted, 
            mins_away=mins_away, 
            start_location=start_location
        )
    
    db.init_app(app)
    
    return app

