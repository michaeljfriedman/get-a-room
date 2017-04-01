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
    import datetime
    from django.utils import timezone
    from get_a_room_app.models import Occupancy, Room

    frist_302 = Room(building='Frist Campus Center', number='302', capacity=100)
    frist_302.save()

    start_time = timezone.now() + datetime.timedelta(days=-1)
    occupancies = [
        Occupancy(timestamp=start_time + datetime.timedelta(minutes=t),
            room=frist_302, occupancy=100 - 2*t) for t in range(0, 30)
    ]
    for occupancy in occupancies:
        occupancy.save()
    print 'Done!'
