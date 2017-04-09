# get-a-room
Princeton University study room/space recommendation app

## What is it, and how does it work?
### Overview
The core idea behind our app is to present students with a visualization of the study spaces on campus. We provide
real-time information about how many people are using each study space, so students can find a nearby place to
study that isn't too busy.

The UI is a map of the campus with markers on every building, color-coded red/yellow/green to indicate how busy the
study spaces in each building are. Users can click on a marker to pull up a table of each study space/room and how
many people are currently using them.

We obtain these occupancy statistics by determining the number of devices connected to various wireless access points
(APs) on campus.

### Backend details
The data is (eventually going to be) obtained from OIT. This data is then parsed and stored in our own
database, which we read from to populate the map view.

We use several scripts to update and store our data, all within the `get_a_room` directory. Every five minutes, we go through
the following procedure:
1. Run `update_stats`, which (once we have arranged this with them) pulls data from OIT and stores it in `stats.txt`. (Currently, while we getting approval from OIT to access this data, `update_stats` just uses a script `create_stats.py` to
generate fake data for testing purposes.)
2. Run `read_stats_to_database.py`, which parses the raw data in `stats.txt` and stores it in our database.
Once this is done, the backend is updated, and the frontend can load the new data into the view.

### Frontend details
*TODO: Fill in this section.*

## Git conventions
### Branches
- `master`: Stable "production-level" branch. Commits are merged into here from the `dev` branch. This branch contains releases/milestones of the app, and should be *fully* tested and working.
- `dev`: Development branch. Contains commit history as we progress to each release/milestone. Commits are merged into `dev` from topic branches, so code should be *mostly* tested and working by the time it is merged here. (It still may have small bugs, though.)
- Topic branches: Branches out of `dev` for bug fixes, features, etc. Should be individually tested before merging back to `dev`. Name these branches with a few short words describing the branch, e.g. `database-setup`.

## Code conventions
### General
- Indentation: Indent with *spaces*, indent size of 4.
- Line endings: Unix-style `\n`.

### Python-specific
- Strings: Use single quotes.
- Header comments (at file-level and function-level): Standard Python style. Immediately inside the function/class, enclosed in triple quotes, with newlines between triple quotes.

## Dependencies
For contributers, installation of dependencies and other set-up is automated by running a script in the root of the project: `setup`. Once you've cloned the repo, you can get your environment set up by just running:
```
./setup [ubuntu|mac]
```
passing your OS as argument. When a new dependency installation or set-up is required, this script is updated accordingly to automate it and committed with the rest of the changes. When you pull these changes, you can rerun `setup` to update your environment.

## Contributers
- Michael J. Friedman
- Rachana Balasubramanian
