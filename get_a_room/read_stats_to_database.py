#-------------------------------------------------------------------------------
# read_stats_to_database.py
# Author: Michael Friedman
#
# Reads the current stats from stats.txt into the database, using ap-to-room.txt
# to translate access points (APs) into room numbers.
#
# NOTE: We only have the translation for rooms in Frist as of now.

#-------------------------------------------------------------------------------

# Some setup before we can interact with Django
import os
import django
os.environ['DJANGO_SETTINGS_MODULE'] = 'get_a_room.settings'
django.setup()

#-------------------------------------------------------------------------------

### Main script
from collections import defaultdict
from django.utils import timezone
from get_a_room_app.models import Room, Occupancy

# Read in ap-to-room.txt to build a mapping from APs to rooms in Frist
ap_to_room = open('ap-to-room.txt', 'r')
lines = [line.strip() for line in ap_to_room.readlines()]
rooms_by_aps = defaultdict(lambda: None)
for line in lines:
    fields = line.split()
    ap = fields[0]
    room = fields[1]
    rooms_by_aps[ap] = room


# Read stats.txt into database
stats = open('stats.txt', 'r')
lines = [line.strip() for line in stats.readlines()]
for line in lines:
    fields = line.split()
    building = fields[0].lower()
    ap = fields[1]
    occupancy = int(fields[2])
    room_number = rooms_by_aps[ap]
    if room_number:
        rooms = Room.objects.filter(building=building, number=room_number)
        room = rooms[0]
        occupancy = Occupancy(
            timestamp=timezone.now(),
            room=room,
            occupancy=occupancy
        )
        occupancy.save()
