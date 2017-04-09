import datetime
import json
from django.db import IntegrityError
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from get_a_room_app.models import Building, Occupancy, Room

#-------------------------------------------------------------------------------

### View tests

'''
Helper methods for tests. Return a valid Building/Room/Occupancy entries, but do
not place them in their corresponding table. i.e. the caller must save() them
afterwards.
'''
def create_building(name, lat=0.0, lng=0.0):
    return Building(name=name, lat=lat, lng=lng)

def create_room(building=0, number='302', capacity=50):
    if building == 0:
        building = create_building('Frist Campus Center')
        building.save()
    return Room(building=building, number=number, capacity=capacity)

def create_occupancy(timestamp=timezone.now(), room=0, occupancy=25):
    if room == 0:
        room = create_room()
        room.save()
    return Occupancy(timestamp=timestamp, room=room, occupancy=occupancy)


class IndexViewTests(TestCase):
    '''
    Tests for the index (landing) page
    '''

    def test_index_page_loads_database_contents(self):
        '''
        Tests that the index page loads correctly.
        '''
        pass # TODO: Implement this

class StatsBuildingViewTests(TestCase):
    '''
    Tests for retrieving stats by building name in JSON format.
    '''

    def test_stats_building_for_valid_building(self):
        '''
        Requests the stats for a building that is in the database, and checks
        that we get back the correctly formatted JSON object. Should only
        return stats for the most recent timestamp.
        '''
        # Make several rooms for two buildings
        frist_building = create_building('Frist Campus Center')
        frist_building.save()
        cs_building = create_building('Computer Science Building')
        cs_building.save()

        frist_rooms = [
            create_room(building=frist_building, number='100'),
            create_room(building=frist_building, number='200'),
            create_room(building=frist_building, number='300')
        ]
        for room in frist_rooms:
            room.save()

        cs_rooms = [
            create_room(building=cs_building, number='100'),
            create_room(building=cs_building, number='200'),
            create_room(building=cs_building, number='300'),
        ]
        for room in cs_rooms:
            room.save()

        # Enter occupancy stats for each room. Create some stats with older
        # timestamp. The request should only retrieve the more recent stats.
        now = timezone.now()
        frist_occupancies = [
            create_occupancy(timestamp=now, room=frist_rooms[0]),
            create_occupancy(timestamp=now, room=frist_rooms[1]),
            create_occupancy(timestamp=now, room=frist_rooms[2])
        ]
        for occupancy in frist_occupancies:
            occupancy.save()

        before = now - datetime.timedelta(days=1)
        cs_occupancies = [
            create_occupancy(timestamp=before, room=cs_rooms[0]),
            create_occupancy(timestamp=before, room=cs_rooms[1]),
            create_occupancy(timestamp=before, room=cs_rooms[2])
        ]
        for occupancy in cs_occupancies:
            occupancy.save()

        # Make the request
        response = self.client.get(reverse('get_a_room_app:stats_building', kwargs={'building': 'frist-campus-center'}))
        try:
            parsed_response = json.loads(response.content)  # JSON object for one building, formatted as specified in views.py
        except:
            self.fail('JSON response could not be parsed')

        # Verify response is correct
        self.assertEqual(sorted(parsed_response.keys()), ['lat', 'lng', 'name', 'rooms'])  # has correct attributes
        self.assertEqual(parsed_response['name'], frist_rooms[0].building.name)            # has correct building name

        frist_occupancies = sorted(frist_occupancies, cmp=lambda x, y: cmp(x.room.number, y.room.number))
        test_occupancies = sorted(parsed_response['rooms'], cmp=lambda x, y: cmp(x['number'], y['number']))
        self.assertEqual(len(test_occupancies), len(frist_occupancies))  # has correct number of entries
        for i in range(0, len(frist_occupancies)):
            # Has correct fields in each entry
            self.assertEqual(test_occupancies[i]['number'], frist_occupancies[i].room.number)
            self.assertEqual(test_occupancies[i]['occupancy'], frist_occupancies[i].occupancy)
            self.assertEqual(test_occupancies[i]['capacity'], frist_occupancies[i].room.capacity)

    def test_stats_building_for_nonexistent_building(self):
        '''
        Requests the stats for a building that does not exist in the database,
        and checks that we get back an empty JSON object.
        '''
        response = self.client.get(reverse('get_a_room_app:stats_building', kwargs={'building': 'white-house'}))
        try:
            parsed_response = json.loads(response.content)
        except:
            self.fail('JSON response could not be parsed')

        # Verify response is correct
        self.assertEqual(parsed_response, {})


class StatsMostRecentViewTests(TestCase):
    '''
    Tests for retrieving stats by most recent timestamp.
    '''

    def test_stats_most_recent_valid(self):
        '''
        Requests the most recent stats for all buildings when there is at
        least one timestamp in the database, and checks that we get back the
        correctly formatted JSON.
        '''
        # Make several rooms for two buildings
        frist_building = create_building('Frist Campus Center')
        frist_building.save()
        cs_building = create_building('Computer Science Building')
        cs_building.save()

        frist_rooms = [
            create_room(building=frist_building, number='100'),
            create_room(building=frist_building, number='200'),
            create_room(building=frist_building, number='300')
        ]
        for room in frist_rooms:
            room.save()

        cs_rooms = [
            create_room(building=cs_building, number='100'),
            create_room(building=cs_building, number='200'),
            create_room(building=cs_building, number='300'),
        ]
        for room in cs_rooms:
            room.save()

        # Enter occupancy stats for each room. (All rooms in both buildings have
        # the same timestamp)
        now = timezone.now()
        frist_occupancies = [
            create_occupancy(timestamp=now, room=frist_rooms[0]),
            create_occupancy(timestamp=now, room=frist_rooms[1]),
            create_occupancy(timestamp=now, room=frist_rooms[2])
        ]
        for occupancy in frist_occupancies:
            occupancy.save()

        cs_occupancies = [
            create_occupancy(timestamp=now, room=cs_rooms[0]),
            create_occupancy(timestamp=now, room=cs_rooms[1]),
            create_occupancy(timestamp=now, room=cs_rooms[2])
        ]
        for occupancy in cs_occupancies:
            occupancy.save()

        # Make request
        response = self.client.get(reverse('get_a_room_app:stats_most_recent'))
        try:
            parsed_response = json.loads(response.content) # List of JSON objects, formatted as specified in views.py
        except:
            self.fail('JSON response could not be parsed')

        # Verify response is correct
        for entry in parsed_response:
            self.assertEqual(sorted(entry.keys()), ['lat', 'lng', 'name', 'rooms']) # each entry has correct attributes

        test_buildings = sorted(parsed_response, cmp=lambda x, y: cmp(x['name'], y['name']))
        self.assertEqual(len(test_buildings), 2)   # has correct number of buildings
        self.assertEqual([test_buildings[0]['name'], test_buildings[1]['name']],
            [cs_rooms[0].building.name, frist_rooms[0].building.name])  # has correct buildings

        frist_test_vs_actual = (test_buildings[0]['rooms'], frist_occupancies)
        cs_test_vs_actual = (test_buildings[1]['rooms'], cs_occupancies)
        for test_occupancies, actual_occupancies in [frist_test_vs_actual, cs_test_vs_actual]:
            actual_occupancies = sorted(actual_occupancies, cmp=lambda x, y: cmp(x.room.number, y.room.number))
            test_occupancies = sorted(test_occupancies, cmp=lambda x, y: cmp(x['number'], y['number']))
            self.assertEqual(len(test_occupancies), len(actual_occupancies))  # has correct number of room entries
            for i in range(0, len(actual_occupancies)):
                # Has correct fields in each room entry
                self.assertEqual(test_occupancies[i]['number'], actual_occupancies[i].room.number)
                self.assertEqual(test_occupancies[i]['occupancy'], actual_occupancies[i].occupancy)
                self.assertEqual(test_occupancies[i]['capacity'], actual_occupancies[i].room.capacity)

    def test_stats_most_recent_with_empty_database(self):
        '''
        Requests the most recent stats for all buildings when there are no
        entries in the Occupancy table. Checks that this returns an empty
        JSON object.
        '''
        response = self.client.get(reverse('get_a_room_app:stats_most_recent'))
        try:
            parsed_response = json.loads(response.content)
        except:
            self.fail('JSON response could not be parsed')

        # Verify response is correct
        self.assertEqual(parsed_response, {})


#-------------------------------------------------------------------------------

### Database tests

class BuildingModelTests(TestCase):
    '''
    Tests that we can put/get things into/from the Building table, and that
    it only accepts valid entries.
    '''

    def test_insert_with_valid_entry(self):
        '''
        Inserts an entry into the table, gets it out, and checks that its
        attributes are correct.
        '''
        building = create_building('White House')
        building.save()

        test_building = Building.objects.order_by('-id')[0]
        self.assertEqual(test_building, building)

    def test_insert_with_no_name(self):
        '''
        Inserts an entry with an empty name into the table, and checks that
        it fails to insert.
        '''
        building = create_building(None)
        self.assertRaises(IntegrityError, building.save)

    def test_insert_with_no_latitude(self):
        '''
        Inserts an entry with an empty latitude into the table, and checks that
        it fails to insert.
        '''
        building = create_building('White House', lat=None)
        self.assertRaises(IntegrityError, building.save)

    def test_insert_with_no_longitude(self):
        '''
        Inserts an entry with an empty longitude into the table, and checks that
        it fails to insert.
        '''
        building = create_building('White House', lng=None)
        self.assertRaises(IntegrityError, building.save)

    def test_unique_names(self):
        '''
        Inserts two entries with the same name into the table, and checks that
        the second one fails to insert.
        '''
        building1 = Building(name='White House', lat=0.0, lng=0.0)
        building1.save()

        building2 = Building(name='White House', lat=90.0, lng=180.0)
        self.assertRaises(IntegrityError, building2.save)

class RoomModelTests(TestCase):
    '''
    Tests for Room table in the database.
    '''

    def test_insert_valid_entry(self):
        '''
        Insets a valid entry, and tests that its contents are correct.
        '''
        room = create_room()
        room.save()

        test_room = Room.objects.order_by('-id')[0]
        self.assertEqual(test_room, room)

    def test_insert_with_negative_capacity(self):
        '''
        Inserts an entry with negative capacity, and tests that it fails to
        insert.
        '''
        room = create_room(capacity=-1)
        self.assertRaises(ValueError, room.save)

    '''
    The following tests attempt to insert entries with missing attributes, and
    test that the insertion fails.
    '''
    def test_insert_with_no_building(self):
        room = create_room(building=None)
        self.assertRaises(IntegrityError, room.save)

    def test_insert_with_no_number(self):
        room = create_room(number=None)
        self.assertRaises(IntegrityError, room.save)

    def test_insert_with_no_capacity(self):
        room = create_room(capacity=None)
        self.assertRaises(IntegrityError, room.save)


class OccupancyModelTests(TestCase):
    '''
    Tests for Occupancy table in the database.
    '''

    def test_insert_valid_entry(self):
        '''
        Inserts a valid entry and tests that it has the right contents.
        '''
        occupancy = create_occupancy()
        occupancy.save()

        test_occupancy = Occupancy.objects.order_by('-id')[0]
        self.assertEqual(test_occupancy, occupancy)

    def test_insert_with_timestamp_in_the_future(self):
        '''
        Inserts an entry with a timestamp in the future, and tests that it
        fails to insert.
        '''
        occupancy = create_occupancy(timestamp=timezone.now() + datetime.timedelta(days=30))
        self.assertRaises(ValueError, occupancy.save)

    def test_insert_with_nonexistent_room(self):
        '''
        Inserts an entry with a room that is not in the Room table, and tests
        that it fails to insert.
        '''
        occupancy = create_occupancy(room=create_room())
        self.assertRaises(ValueError, occupancy.save)

    def test_insert_with_negative_occupancy(self):
        '''
        Inserts an entry with a negative value for occupancy, and tests that
        it fails to insert.
        '''
        occupancy = create_occupancy(occupancy=-1)
        self.assertRaises(ValueError, occupancy.save)

    def test_insert_with_occupancy_greater_than_capacity(self):
        '''
        Inserts an entry with a value for occupancy greater than the total
        capacity of the room, and tests that it fails to insert.
        '''
        occupancy = create_occupancy(occupancy=51)
        self.assertRaises(ValueError, occupancy.save)

    '''
    The following tests attempt to insert entries with missing attributes, and
    test that the insertion fails.
    '''
    def test_insert_with_no_timestamp(self):
        occupancy = create_occupancy(timestamp=None)
        self.assertRaises(IntegrityError, occupancy.save)

    def test_insert_with_no_room(self):
        occupancy = create_occupancy(room=None)
        self.assertRaises(IntegrityError, occupancy.save)

    def test_insert_with_no_occupancy(self):
        occupancy = create_occupancy(occupancy=None)
        self.assertRaises(IntegrityError, occupancy.save)
