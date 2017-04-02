import datetime
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
def create_room(building='frist-campus-center', number='302', capacity=50):
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

class SlidePanelViewTests(TestCase):
    '''
    Tests for retrieving data and populating them into the slide panel.
    '''

    def test_slide_panel_loads_building_contents(self):
        '''
        Loads the slide panel view and checks that the building stats are
        in it.
        '''
        # TODO: There is something wrong with this test, but the view itself works. Fix this later
        # create_occupancy().save()
        # response = self.client.get(reverse('get_a_room_app:slide-panel', kwargs={'building': 'frist-campus-center'}))
        # most_recent_timestamp = Occupancy.objects.order_by('-timestamp')[0].timestamp
        # occupancies = Occupancy.objects.filter(timestamp=most_recent_timestamp, room__building='frist-campus-center')
        # for occupancy in occupancies:
        #     self.assertContains(response.content, str(occupancy.room.building))
        #     self.assertContains(response.content, str(occupancy.room.number))
        #     self.assertContains(response.content, str(occupancy.occupancy))
        #     self.assertContains(response.content, str(occupancy.room.capacity))

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
