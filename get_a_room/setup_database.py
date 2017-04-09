#-------------------------------------------------------------------------------
# setup_database.py
# Author: Michael Friedman
# Usage: python setup_database.py -p
#
# Runs the necessary Django commands to intialize/update the project's database.
# You can also rerun it each time the models for the database are updated as a
# shortcut for makemigrations + migrate. Optionally pass the -p arg to
# populate with some sample data.
#-------------------------------------------------------------------------------

# Check usage
import sys
usage = 'usage: python setup_database.py [-p]'
if len(sys.argv) != 1 and len(sys.argv) != 2:
    print usage
    exit(1)
elif len(sys.argv) == 2 and sys.argv[1] != '-p':
    print usage
    exit(1)

populate = (len(sys.argv) == 2)

#-------------------------------------------------------------------------------

# Some setup before we can interact with Django
import os
import django
os.environ['DJANGO_SETTINGS_MODULE'] = 'get_a_room.settings'
django.setup()

#-------------------------------------------------------------------------------

### Main script

# Initialize database
print 'Initializing/updating database...'
os.system('python manage.py makemigrations get_a_room_app')
os.system('python manage.py migrate')
print 'Done!'

# Populate database with most recent stats from all buildings
if populate:
    print 'Populating database with most recent stats from all buildings...'
    import json
    from django.db import IntegrityError
    from get_a_room_app.models import Building, Occupancy, Room
    from random import randint

    # Populate buildings
    print 'Populating buildings...'
    f = open('locations.json', 'r')
    buildings = json.loads(f.read())
    for building in buildings:
        try:
            Building(
                name=building['name'],
                lat=float(building['lat']),
                lng=float(building['lng'])
            ).save()
        except IntegrityError as e:
            print >> sys.stderr, 'Duplicate building %s: not entered' % building['name']
    f.close()
    print 'Done!'
    print

    # Populate rooms
    # TODO: For now, ap-to-room.txt only maps rooms in Frist. Need to add a mapping for rooms in all other buildings.
    print 'Populating rooms...'
    f = open('ap-to-room.txt', 'r')
    lines = [line.strip() for line in f.readlines()]
    nums = [line.split()[1] for line in lines]
    for num in nums:
        building = Building.objects.get(name='Frist Campus Center')
        Room(
            building=building,
            number=int(num),
            capacity=randint(50, 100)
        ).save()
    f.close()
    print 'Done!'
    print

    # Get most recent stats and put them into database
    print 'Populating most recent stats'
    # os.system('./update_stats')  # TODO: Fix this
    os.system('python read_stats_to_database.py')
    print 'Done!'
