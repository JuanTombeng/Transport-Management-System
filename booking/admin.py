from django.contrib import admin
from .models import Bookings, Destinations, StationLocation, Vehicles, DriverScheduleAvailabilities, Payments

admin.site.register(Bookings)
admin.site.register(Destinations)
admin.site.register(StationLocation)
admin.site.register(Vehicles)
admin.site.register(DriverScheduleAvailabilities)
admin.site.register(Payments)
