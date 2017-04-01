#-------------------------------------------------------------------------------
# setup_database.py
# Author: Michael Friedman
# Usage: python setup_database.py
#
# Runs the necessary Django commands to intialize/update the project's database.
# You can also rerun it each time the models for the database are updated as a
# shortcut for makemigrations + migrate.
#-------------------------------------------------------------------------------

# Some setup before we can interact with Django
import os
import django
os.environ['DJANGO_SETTINGS_MODULE'] = 'get_a_room.settings'
django.setup()

#-------------------------------------------------------------------------------

### Main script

from django.utils import timezone
from get_a_room_app.models import Occupancy, Room

# Initialize database
print 'Initializing/updating database...'
os.system('python manage.py makemigrations get_a_room_app')
os.system('python manage.py migrate')
print 'Done!'
