from django.shortcuts import render
from get_a_room_app.models import Room, Occupancy

def index(request):
    '''
    Sample view to demonstrate end-to-end flow of data. Displays the
    Room and Occupancy tables' raw contents.
    '''
    rooms = Room.objects.all()
    occupancies = Occupancy.objects.all()
    #return render(request, 'get_a_room_app/index.html', {'rooms': rooms, 'occupancies': occupancies})
    return render(request, 'get_a_room_app/map.html',{})