DROP TABLE IF EXISTS venue;

CREATE TABLE venue (
  venue_id TEXT PRIMARY KEY,
  last_retrieved TIMESTAMP,
  name TEXT,
  address_1 TEXT,
  city TEXT,
  state TEXT
);


-- Seed the venue table with some venues, since Eventbrite doesn't have a way to search organizations/venues.
-- The other columns for these records will be filled in the first time we fetch data from the API.
INSERT INTO venue ('venue_id', 'name') VALUES
    ('230819579', 'Eli Tea Bar'),
    ('99195019', 'Women & Children First'),
    ('294845373', 'Lot''sa'),
    ('294117663', 'Steppenwolf Theatre Company'),
    ('99300689', 'Dorothy'),
    ('247504153', 'Pumping Station One'),
    ('275093843', 'Chicago Fair Trade Museum & Store'),
    ('289397983', 'Annoyance Theatre & Bar'),
    ('195277559', 'Avondale Bowl');
