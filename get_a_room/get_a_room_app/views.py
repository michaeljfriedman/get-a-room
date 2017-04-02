from django.shortcuts import render
from get_a_room_app.models import Room, Occupancy

def index(request):
    '''
    Sample view to demonstrate end-to-end flow of data. Displays the
    Room and Occupancy tables' raw contents.
    '''
    rooms = Room.objects.all()
    occupancies = Occupancy.objects.all()
    return render(request, 'index.html',{})

def map(request):
    '''
    Sample view of the map.
    '''
    return render(request, 'map.html',{})