from django.test import TestCase
from django.urls import reverse

class IndexViewTests(TestCase):
    '''
    Tests for the index (landing) page
    '''

    def test_index_page_loads_hello_world(self):
        '''
        Tests that the index page loads with content "Hello world!"
        '''
        response = self.client.get(reverse('get_a_room_app:index'))
        self.assertEqual(response.content, 'Hello world!')
