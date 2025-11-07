# Local Event Finder (WIP)

## The Problem
Let's say it's a Friday night and you have no plans for the weekend. You want to do something fun, but you're tired and don't want to spend a bunch of time planning logistics.

## The Proposed Solution
A webpage where you can put in your location, the maximum time you're willing to spend in transit, and optionally your Eventbrite user ID for personalizing events to your interests. The webpage will spit out a list of events matching your criteria.

Each event should display a brief summary including:
- Name of the event
- How long it'll take to get there (plus info about which bus/train/etc you're taking)
- When you'll have to leave home

Events should be prioritized/sorted according to the following criteria:
- If Eventbrite ID was provided, prioritize events put on by organizations that the user is a member of
- Otherwise, list events that are closer by first

## Tasks
Essentials:
- [ ] Set up a basic client that can authenticate to the Eventbrite API
- [ ] Make a skeleton for the webpage
- [ ] Calculate the transit time between the user's location and an event (TravelTime API?)
- [ ] Retrieve a list of events and output the names
- [ ] Decide on a transit route and output information (time, bus/train line)
- [ ] Calculate when the user should leave home based on the travel time and event time

Make it fancier:
- [ ] Style it so it looks decent
- [ ] Add filters for event tags? (include/exclude)
- [ ] Add cost of event to display
- [ ] Add max cost filter

## Resources Used

- [Eventbrite API Docs](https://www.eventbrite.com/platform/api)
