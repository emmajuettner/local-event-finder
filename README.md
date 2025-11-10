# Local Event Finder (WIP)

## The Problem
Let's say it's a Friday night and you have no plans for the weekend. You want to do something fun, but you're tired and don't want to spend a bunch of time planning logistics.

## The Proposed Solution
An app where you can put in your location and the maximum time you're willing to spend in transit. The app will spit out a list of events from organizations you follow on Eventbrite matching your criteria.

Each event should display a brief summary including:
- Name of the event
- How long it'll take to get there (plus info about which bus/train/etc you're taking)
- When you'll have to leave home

## Configurations
Configurable values are stored in the `.env` file. You can copy the example set of configurations to start with: `cp .starter-env .env`

You'll need to update the following values in `.env`:
- `EVENTBRITE_API_KEY` - Used to pull data from Eventbrite. Log into your Eventbrite account and [retrieve your API key](https://www.eventbrite.com/platform/api-keys).
- `SECRET_KEY` - Used by Flask for sessions. Run `python3 -c 'import secrets; print(secrets.token_hex())'`
- `GOOGLE_MAPS_API_KEY` - Used to pull transit route data from Google Maps. Log into your Google Cloud account and [retrieve your API key](https://console.cloud.google.com/google/maps-apis/credentials).

## Running the App Locally

1. Run `python3 -m venv .venv` in the project's root directory to set up your local virtual environment.
2. Activate the virtual environment: `source .venv/bin/activate`
3. Install the required dependencies: `pip install -r requirements.txt`
4. Initialize the database: `flask --app app init-db`
5. Run the app: `flask --app app run --debug`
6. Visit [localhost:5000](http://localhost:5000/) in your browser to see the app running.

## Running Linter/Test Suite

Run `ruff check` from the project root directory to run the linter.

Run `pytest tests/` from the project root directory to execute the tests.

## Tasks
Essentials:
- [x] Set up a basic client that can call the Eventbrite API
- [x] Make a skeleton for the webpage
- [x] Make the form fields functional
- [ ] Cache data in db so we don't have to call the API all the time
- [x] Calculate the transit time between the user's location and an event (Google Maps Routes API)
- [x] Retrieve a list of events and output the names
- [x] Decide on a transit route and output information (time, bus/train line)
- [ ] Handle pagination in Eventbrite requests
- [x] Filter out completed events
- [x] Add some tests
- [x] Add validations for input

Optional extras:
- [ ] Make it look nice
- [ ] Add filters for event tags? (include/exclude)
- [x] Add cost of event to display
- [ ] Add max cost filter
- [ ] Add other event data sources (library RSS feeds? parks district events, if they have some feed/api?)
- [ ] Make travel time calculation slightly more sophisticated by setting desired arrival time (to account for different transit schedules on different days of week/times of day)

## Useful Resources

- [Eventbrite API Docs](https://www.eventbrite.com/platform/api)
- [Google Maps Routes API Docs](https://developers.google.com/maps/documentation/routes)

