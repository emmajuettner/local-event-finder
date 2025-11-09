import os
import datetime

from flask import Flask
from flask import render_template
from dotenv import dotenv_values
from . import eventbrite


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
        return render_template('index.html', user_name=eventbrite.get_user(), events=user_events)

    return app

