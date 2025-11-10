# Local Event Finder

## The Problem
Let's say it's a Friday night and you have no plans for the weekend. You want to do something fun, but you're tired and don't want to spend a bunch of time figuring out which local events are within a reasonable distance from home.

## The Proposed Solution
An app where you can put in your location and the maximum time you're willing to spend in transit. The app will spit out a list of events from Eventbrite matching your criteria.

Each event should display a brief summary including:
- Name of the event
- How long it'll take to get there
- Info about which bus/train/etc you're taking

## A Caveat

It turns out Eventbrite's API doesn't actually let you search events, nor venues, nor organizations. It also doesn't let you look up a user and get a list of organizations that user follows. For this reason, to get an initial list of venues whose events you're interested in, you have to look up their Eventbrite venue IDs and insert those into the database so that we can use that to pull a list of upcoming events at those venues.

## Screenshots

Search form:

<img width="854" height="392" alt="image" src="https://github.com/user-attachments/assets/5879a94d-feee-44a6-b8ad-9bc2833da385" />

Example results:

<img width="849" height="761" alt="image" src="https://github.com/user-attachments/assets/c905c7aa-5c24-4ecc-a2df-f9b41d7c2d14" />


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
- [x] Cache venues in db so we don't have to call the API every time
- [ ] Cache events in db to improve performance
- [ ] Refactor eventbrite.py/maps.py to pull out functions that aren't actually interacting with the apis and put them somewhere that makes more sense
- [x] Calculate the transit time between the user's location and an event (Google Maps Routes API)
- [x] Retrieve a list of events and output the names
- [x] Decide on a transit route and output information (time, bus/train line)
- [x] Handle pagination in Eventbrite requests
- [x] Filter out completed events
- [x] Set up test framework
- [x] Add some validations for input
- [ ] Add more robust error handling
- [ ] Add more tests

Extras:
- [ ] Make it look nice
- [ ] Add filters for event tags? (include/exclude)
- [x] Add cost of event to display
- [ ] Add max cost filter
- [ ] Add other event data sources (library RSS feeds? parks district events, if they have some feed/api?)
- [ ] Make travel time calculation slightly more sophisticated by setting desired arrival time (to account for different transit schedules on different days of week/times of day)
- [ ] Cache routes in db to improve performance?

## Useful Resources

- [Eventbrite API Docs](https://www.eventbrite.com/platform/api)
- [Google Maps Routes API Docs](https://developers.google.com/maps/documentation/routes)

