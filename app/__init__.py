import os

from flask import Flask, render_template, request
from dotenv import dotenv_values
from . import eventbrite
from . import maps

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
        user_events = eventbrite.get_user_events()
        events_with_transit_info = maps.populate_events_with_transit_info(form_data["startLocation"], form_data["minsAway"], user_events)
        return render_template("index.html", events=events_with_transit_info, mins_away=form_data["minsAway"], start_location=form_data["startLocation"])
    
    return app

