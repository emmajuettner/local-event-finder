import os

from flask import Flask, render_template, request, redirect, url_for
from dotenv import dotenv_values
from . import eventbrite
from . import maps
from . import input_validation

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
        form_data = request.form
        start_location = form_data["startLocation"].strip()
        mins_away = form_data["minsAway"].strip()
        is_input_valid = input_validation.validate_input(start_location, mins_away)
        if not is_input_valid:
            return redirect(url_for('index_get'))
        user_events = eventbrite.get_user_events()
        events_with_transit_info = maps.populate_events_with_transit_info(
            start_location,
            mins_away,
            user_events
        )
        return render_template(
            "index.html", 
            events=events_with_transit_info, 
            mins_away=mins_away, 
            start_location=start_location
        )
    
    return app

