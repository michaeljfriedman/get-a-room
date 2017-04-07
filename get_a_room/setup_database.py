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

# Populate database with sample contents
if populate:
    print 'Populating database with sample data...'
    from get_a_room_app.models import Occupancy, Room
    from random import randint

    f = open('ap-to-room.txt', 'r')
    lines = [line.strip() for line in f.readlines()]
    nums = [line.split()[1] for line in lines]
    print nums
    print
    print 'Populating rooms...'
    for num in nums:
        room = Room(
            building='Frist Campus Center',
            number=int(num),
            capacity=randint(50, 100)
        )
        room.save()
    print 'Done!'
