# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-01 17:52
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Occupancy',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField()),
                ('occupancy', models.PositiveSmallIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('building', models.CharField(max_length=50)),
                ('number', models.CharField(max_length=10)),
                ('capacity', models.PositiveSmallIntegerField()),
            ],
        ),
        migrations.AddField(
            model_name='occupancy',
            name='room',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='get_a_room_app.Room'),
        ),
    ]