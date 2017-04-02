# Some setup before we can interact with Django
import os
import django
os.environ['DJANGO_SETTINGS_MODULE'] = 'get_a_room.settings'
django.setup()

# Clear the database
from get_a_room_app.models import Room, Occupancy

print 'Clearing database...'
for room in Room.objects.all():
    room.delete()

for occupancy in Occupancy.objects.all():
    occupancy.delete()
print 'Done!'
