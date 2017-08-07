# Backend (Database and API)

Below is the directory structure that backend developers will work with.

```
- get_a_room_app/
  - models.py
  - tests.py
  - urls.py
  - views.py
- get_a_room/
  - settings.py
- ap-to-room.txt
- create_stats.py
- locations.json
- read_stats_to_database.py
- setup_database.py
- stats.txt
- update_stats
```

## Database

### Schema
The database schema is defined by `models.py`. We use a simple relational model, implemented in SQLite. It consists of three models: `Building`, `Room`, and `Occupancy`.

- `Building`: A single building on campus.
  - Name (string): *full name* of the building
  - Latitude (float)
  - Longitude (float)
- `Room`: A room within a building.
  - Number (string): the room number, e.g. 102A
  - Capacity (integer): the *maximum* capacity of the room
  - Building (`Building`): building containing the room
- `Occupancy`: A group of statistics about a room.
  - Occupany (integer): number of people in the room
  - Timestamp (date/time): when the occupancy was last updated
  - Room (`Room`): room with this occupancy

### Initializing the database

For convenience, we created a script `setup_database.py`, which does initial configuration of the database and optionally populates it with data. You can run it with:

```
python setup_database.py
```

> Note that the `configure.{ps1, sh}` script runs `setup_database.py` to do its database configuration, so you never really need to run this directly. It is only documented here for completeness.

### Populating the database

`Building` and `Room` contain static data, so they only need to be populated once. `Building` is populated with the data in `locations.json`, which was scraped from the [Princeton map website](http://m.princeton.edu/map/campus). `Room` is populated with data in `ap-to-room.txt`, a file that maps campus WiFi access points to the rooms they're in (we manually created this).

On the other hand, `Occupancy` is dynamic; it must constantly be updated with the latest room occupancy stats. We will eventually obtain this data from OIT (we are currently working this out with them). However, even without the data, we have developed a system for populating the database with it.

```
       update_stats                  read_stats_to_database.py
OIT  ---------------->  stats.txt  ---------------------------->  Our database
                            +
                      ap-to-room.txt
```

1. `update_stats` makes a request to OIT for latest room occupancy stats, outputs to `stats.txt`.
2. `read_stats_to_database.py` reads in `stats.txt` and `ap-to-room.txt`, and populates our database with those stats.

We repeat this procedure automatically every five minutes.

Until we work out our access to this data with OIT, the role of "OIT" in procedure is served by a script `create_stats.py`, which generates fake data. So for now, `update_stats` simply runs `create_stats.py` and outputs the results to `stats.txt`.

## API

We implemented a web API that allows the frontend UI to pull data from our backend database. The UI shows all the most recent room availability stats, and it retrieves this information through two API calls:

### GET /stats/building/<building_name>
Returns the occupancy stats for `building_name`, formatted as a JSON object in the following format:

```
{
  'name': 'Frist Campus Center',
  'lat': '12.3456789',
  'lng': '12.3456789',
  'rooms': [
    {'number': '123A', 'occupancy': 25, 'capacity': 50},
      ...
  ]
}
```

Note that each room's stats are in their own JSON object, collected in the `rooms` array. *This array is not in any particular order.* In particular, it is not necessarily ordered by room number.

### GET /stats/most-recent
Returns the occupancy stats for all buildings, formatted as a JSON array. This is an array of building objects (as returned by `GET /stats/building/<building_name>`), sorted by building name. An abbreviated sample response is below:

```
[
  {'name': 'Frist Campus Center', 'lat': '...', 'lng': '...', 'rooms': [...]},
  {'name': 'Lewis Library', 'lat': '...', 'lng': '...', 'rooms': [...]},
  ...
]
```

These API calls are implemented as Django views, methods located in `views.py`. When the page is loaded, it sends a request to `/stats/most-recent` and uses the data to color each of the buildings based on their occupancy levels. Then, when a user clicks on a particular building, it requests `/stats/building/<building_name>` and populates a side bar with the resulting stats for that building.

## Testing

Write all tests in `tests.py`. Use the [Django’s testing documentation](https://docs.djangoproject.com/en/1.11/topics/testing/) as a reference for this.

## Dependencies

Below we list the dependencies (libraries, frameworks, etc.) used in the backend, and what we use them for. Update this list as more dependencies are added.

- Django 1.10.6: Framework for web app's backend.
