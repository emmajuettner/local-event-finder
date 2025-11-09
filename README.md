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

## Running the App Locally

1. Run `python3 -m venv .venv` in the project's root directory to set up your local virtual environment.
2. Activate the virtual environment: `source .venv/bin/activate`
3. Install the required dependencies: `pip install -r requirements.txt`
4. Run the app: `flask --app app run --debug`
5. Visit [localhost:5000](http://localhost:5000/) in your browser to see the app running.

## Tasks
Essentials:
- [x] Set up a basic client that can call the Eventbrite API
- [x] Make a skeleton for the webpage
- [ ] Cache data in db so we don't have to call the API all the time
- [ ] Calculate the transit time between the user's location and an event (TravelTime API?)
- [x] Retrieve a list of events and output the names
- [ ] Decide on a transit route and output information (time, bus/train line)
- [ ] Calculate when the user should leave home based on the travel time and event time
- [ ] Handle pagination in Eventbrite requests
- [ ] Filter out completed events

Optional extras:
- [ ] Make it look nice
- [ ] Add filters for event tags? (include/exclude)
- [ ] Add cost of event to display
- [ ] Add max cost filter
- [ ] Add other event data sources (library RSS feeds? parks district events, if they have some feed/api?)

## Useful Resources

- [Eventbrite API Docs](https://www.eventbrite.com/platform/api)


