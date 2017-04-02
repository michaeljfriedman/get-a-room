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

def slide_panel(request, building):
    '''
    Responds with the HTML for the slide panel, populated with data for
    'building'
    '''
    most_recent_timestamp = Occupancy.objects.order_by('-timestamp')[0].timestamp
    occupancies = Occupancy.objects.filter(timestamp=most_recent_timestamp, room__building=building)

    # Format building name
    building_pieces = [piece[0].upper() + piece[1:] for piece in building.split('-')]
    building = ' '.join(building_pieces)

    return render(request, 'slide-panel.html', {'building': building, 'occupancies': occupancies})

def slide_panel_test(request):
    '''
    Sample view to demonstrate the slide panel. Displays a button
    you can click to open a slide panel with building stats.
    '''
    return render(request, 'slide-panel-test.html', {})
