from __future__ import unicode_literals

import datetime
from django.db import models, IntegrityError
from django.utils import timezone

building_name_max_length = 50
room_number_max_length = 10
building_lat_lng_decimal_places = 12

class Building(models.Model):
    '''
    Represents the Building table.
    '''
    name = models.CharField(max_length=building_name_max_length, unique=True)
    lat = models.DecimalField(decimal_places=building_lat_lng_decimal_places,
        max_digits=building_lat_lng_decimal_places+3) # 2 for 0-90, 1 for "-" sign
    lng = models.DecimalField(decimal_places=building_lat_lng_decimal_places,
        max_digits=building_lat_lng_decimal_places+4) # 3 for 0-180, 1 for "-" sign

    def __unicode__(self):
        return self.name

class Room(models.Model):
    '''
    Represents the Room table.
    '''
    building = models.ForeignKey(Building, on_delete=models.CASCADE)
    number = models.CharField(max_length=room_number_max_length)
    capacity = models.PositiveSmallIntegerField()

    def save(self, *args, **kwargs):
        '''
        Overrides default save method to validate attributes in greater depth
        than Django does by default.
        '''
        if self.capacity and self.capacity < 0:
            raise ValueError('\'capacity\' attribute of Room is negative')
        super(Room, self).save(*args, **kwargs)

    def __unicode__(self):
        return '%s %s: capacity %d' % (self.building, self.number, self.capacity)

class Occupancy(models.Model):
    '''
    Represents the Occupancy table.
    '''
    timestamp = models.DateTimeField()
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    occupancy = models.PositiveSmallIntegerField()

    def save(self, *args, **kwargs):
        '''
        Overrides default save method to validate attributes in greater depth
        than Django does by default.
        '''
        if isinstance(self.timestamp, datetime.datetime) and self.timestamp > timezone.now():
            raise ValueError('\'timestamp\' attribute of the Occupancy is in the future')
        try:
            if self.occupancy and self.occupancy > self.room.capacity:
                raise ValueError('\'occupancy\' attribute of Occupancy is greater than max capacity of the room')
        except Room.DoesNotExist:
            raise IntegrityError('\'room\' attribute of Occupancy violates NOT NULL constraint')
        if self.occupancy and self.occupancy < 0:
            raise ValueError('\'occupancy\' attribute of Occupancy is negative')
        super(Occupancy, self).save(*args, **kwargs)

    def __unicode__(self):
        return '%s %s %s: occupancy %d / %d' % (str(self.timestamp), self.room.building,
            self.room.number, self.occupancy, self.room.capacity)
