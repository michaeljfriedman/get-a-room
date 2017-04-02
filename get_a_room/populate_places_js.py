#-------------------------------------------------------------------------------
# populate_places_js.py
# Author: Michael Friedman
#
# Generates our places.js file with the correct GPS coordinates of many
# buildings on campus.
#
# See Selenium documentation for details on usage:
# http://selenium-python.readthedocs.io/
#-------------------------------------------------------------------------------

# Some setup before we can interact with Django
import os
import django
os.environ['DJANGO_SETTINGS_MODULE'] = 'get_a_room.settings'
django.setup()

#-------------------------------------------------------------------------------

# Script
import sys
from selenium import webdriver

driver = webdriver.PhantomJS()
places_file = open('places.txt', 'r')
places = [line.strip() for line in places_file.readlines()]

# Start writing file
print '''
// WARNING [LONGITUTDE,LATITUDE] FORM! IT'S STUPID
var places = {
    "type": "FeatureCollection",
    "features": [
'''

# Get lat/lng coordinates for each location from m.princeton.edu's map
for i in range (0, 80):
    driver.get('http://m.princeton.edu/map/detail?feed=91eda3cbe8&group=princeton&featureindex=' + str(i) + '&category=91eda3cbe8%3AALL&_b=%5B%7B%22t%22%3A%22Map%22%2C%22lt%22%3A%22Map%22%2C%22p%22%3A%22index%22%2C%22a%22%3A%22%22%7D%5D#')

    # Skip this page if the location is not one that we want
    location = driver.find_element_by_css_selector('h2.nonfocal').text

    # Go to "Directions" tab
    directions_tab = driver.find_element_by_link_text('Directions')
    directions_tab.click()

    # Extract lat/lng coordinates from "View in Google Maps" button
    # Link is of the form:
    # http://maps.google.com? ... &q=loc:LAT,LNG+ ...
    button = driver.find_element_by_link_text('View in Google Maps')
    link = button.get_attribute('href')
    lat_str = link[link.index('q=loc:')+len('q=loc:'):link.index(',')]
    lng_str = link[link.index(',')+1:link.index('+')]
    lat = float(lat_str)
    lng = float(lng_str)

    # Insert entry into table
    print '''
    {
        "type": "Feature",
        "geometry": {
            "type": "Point",
            "coordinates": [
                %15.12f, %15.12f
            ]
        },
        "properties": {
            "popupContent":"%s"
        },
        "id": 1
    },
    ''' % (lng, lat, location)

    print >> sys.stderr, 'Entered ' + location

driver.quit()

# Wrap up
print '''
    ]
};
'''

os.system('mv places.js get_a_room_app/static/js')
