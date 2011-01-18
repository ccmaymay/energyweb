#!/usr/bin/env python


'''
Set up the development environment.  In particular, change sensor 
settings to those used by energyfaker.
'''


from django.core.management.base import BaseCommand, CommandError
from django.db.models import F
from graph.models import Sensor


class Command(BaseCommand):
    args = ''
    help = 'Set up the development environment.'

    def handle(self, *args, **options):
        Sensor.objects.all().update(ip='127.0.0.1', port=(4000 + F('pk')))
        print 'Updated sensor addresses to localhost, unique ports.'
