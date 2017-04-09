# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-09 17:49
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('get_a_room_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Building',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('lat', models.DecimalField(decimal_places=12, max_digits=15)),
                ('lng', models.DecimalField(decimal_places=12, max_digits=16)),
            ],
        ),
        migrations.AlterField(
            model_name='room',
            name='building',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='get_a_room_app.Building'),
        ),
    ]