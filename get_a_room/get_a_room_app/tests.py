import datetime
import json
from django.db import IntegrityError
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from get_a_room_app.models import Occupancy, Room

#-------------------------------------------------------------------------------

### View tests

'''
Helper methods for tests. Return a valid Room/Occupancy entries, but do not place them in their corresponding table. i.e. the caller must save() them
afterwards.
'''
def create_room(building='Frist Campus Center', number='302', capacity=50):
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
        frist_rooms = [
            create_room(number='100'),
            create_room(number='200'),
            create_room(number='300')
        ]
        for room in frist_rooms:
            room.save()

        cs_rooms = [
            create_room(building='Computer Science Building', number='100'),
            create_room(building='Computer Science Building', number='200'),
            create_room(building='Computer Science Building', number='300'),
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
            parsed_response = json.loads(response.content)
        except:
            self.fail('JSON response could not be parsed')

        # Verify response is correct
        self.assertEqual(sorted(parsed_response.keys()), ['name', 'rooms'])  # has correct attributes
        self.assertEqual(parsed_response['name'], frist_rooms[0].building)   # has correct building name

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
        pass

#-------------------------------------------------------------------------------

### Database tests

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
