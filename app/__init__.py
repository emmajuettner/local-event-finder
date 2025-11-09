import os

from flask import Flask
from flask import render_template
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
        
    @app.route('/')
    def index():
        user_events = eventbrite.get_user_events()
        events_with_transit_info = maps.populate_events_with_transit_info("1060 W Addison St, Chicago, IL", user_events)
        return render_template('index.html', events=events_with_transit_info)

    return app

