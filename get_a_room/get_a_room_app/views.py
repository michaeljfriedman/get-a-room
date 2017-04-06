import json
from collections import defaultdict
from django.http import HttpResponse
from django.shortcuts import render
from get_a_room_app.models import Room, Occupancy

def index(request):
    '''
    Sample view to demonstrate end-to-end flow of data. Displays the
    Room and Occupancy tables' raw contents.
    '''
    return render(request, 'index.html',{})


def format_building_stats(occupancies):
    '''
    Returns the jsonify-able string for the list 'occupancies' of all Occupancy
    entries from the same building. Returns a dict of the form:
    {
        'name': 'Frist Campus Center',
        'rooms': [
            {'number': '123A', 'occupancy': 25, 'capacity': 50},
            ...
        ]
    }
    which can then by jsonified
    '''
    building = occupancies[0].room.building
    stats = {'name': building, 'rooms': []}
    for occupancy in occupancies:
        stats['rooms'].append({
            'number': occupancy.room.number,
            'occupancy': occupancy.occupancy,
            'capacity': occupancy.room.capacity
        })
    return stats


def stats_building(request, building):
    '''
    Responds with the stats for the 'building' from the database, formatted
    in JSON.
    '''
    # Format building name
    building_pieces = [piece[0].upper() + piece[1:] for piece in building.split('-')]
    building = ' '.join(building_pieces)

    # Get building's occupancy stats
    occupancies_ordered_by_timestamp = Occupancy.objects.order_by('-timestamp')
    if len(occupancies_ordered_by_timestamp) == 0:
        return HttpResponse(json.dumps({}))
    most_recent_timestamp = occupancies_ordered_by_timestamp[0].timestamp
    occupancies = Occupancy.objects.filter(timestamp=most_recent_timestamp, room__building=building)

    if len(occupancies) == 0:
        return HttpResponse(json.dumps({}))
    return HttpResponse(json.dumps(format_building_stats(occupancies)))


def stats_most_recent(request):
    '''
    Responds with the most recent stats for all buildings in the database,
    formatted in JSON.
    '''
    # Get stats for all buildings
    occupancies_ordered_by_timestamp = Occupancy.objects.order_by('-timestamp')
    if len(occupancies_ordered_by_timestamp) == 0:
        return HttpResponse(json.dumps({}))
    most_recent_timestamp = occupancies_ordered_by_timestamp[0].timestamp
    all_occupancies = Occupancy.objects.filter(timestamp=most_recent_timestamp)

    # Separate them by building
    occupancies_by_buildings = defaultdict(lambda: [])
    for occupancy in all_occupancies:
        building = occupancy.room.building
        occupancies_by_buildings[building].append(occupancy)

    # Format into a jsonify-able list of dicts
    stats = []
    for _, occupancies in occupancies_by_buildings.iteritems():
        stats.append(format_building_stats(occupancies))

    return HttpResponse(json.dumps(stats))


def slide_panel_test(request):
    '''
    Sample view to demonstrate the slide panel. Displays a button
    you can click to open a slide panel with building stats.
    '''
    return render(request, 'slide-panel-test.html', {})


def test(request):
    '''
    Test view to display the raw database contents
    '''
    rooms = Room.objects.all()
    occupancies = Occupancy.objects.all()
    return render(request, 'test.html', {'occupancies': occupancies, 'rooms': rooms})
