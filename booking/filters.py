import django_filters
from django.forms import DateTimeInput, TextInput
from django_filters import DateTimeFilter
from .models import *


class DestinationFilter(django_filters.FilterSet):
    class Meta:
        model = Destinations
        fields = ['Destination_City', 'Departure_City', 'Station_Location_Name']


class DriverScheduleAvailabilitiesFilter(django_filters.FilterSet):
    class Meta:
        model = DriverScheduleAvailabilities
        fields = ['destination_id']


class ScheduleAvailableFilter(django_filters.FilterSet):
    class Meta:
        model = DriverScheduleAvailabilities
        fields = ['Vehicle_Plate_Number']


class AdminDriverScheduleFilter(django_filters.FilterSet):
    # destination_id = django_filters.ModelChoiceFilter(
    #     queryset=DriverScheduleAvailabilities.objects.filter(),
    #     label='Destination')
    Departure_Date_Time = django_filters.DateTimeFilter(widget=DateTimeInput(attrs={'type': 'datetime-local'}))

    class Meta:
        model = DriverScheduleAvailabilities
        fields = ['Driver_Staff_ID',
                  'destination_id',
                  'Vehicle_Plate_Number',
                  'Departure_Date_Time', ]

    def __init__(self, *args, **kwargs):
        super(AdminDriverScheduleFilter, self).__init__(*args, **kwargs)
        self.filters['Driver_Staff_ID'].extra.update(
            {'empty_label': '---Driver Name---'})
        self.filters['destination_id'].extra.update(
            {'empty_label': '---Destination Name---'})
        self.filters['Vehicle_Plate_Number'].extra.update(
            {'empty_label': '---Vehicle Plate Number---'})


class AdminVehicleFilter(django_filters.FilterSet):
    class Meta:
        model = Vehicles
        fields = ['type',
                  'brand',
                  'plateNumber', ]

    # def __init__(self, *args, **kwargs):
    #     super(AdminVehicleFilter, self).__init__(*args, **kwargs)
    #     self.filters['type'].extra.update(
    #         {'empty_label': '---Type---'})
    #     self.filters['brand'].extra.update(
    #         {'empty_label': '---Brand---'})
    #     self.filters['plateNumber'].extra.update(
    #         {'empty_label': '---Plate Number---'})


class AdminDestinationFilter(django_filters.FilterSet):
    class Meta:
        model = Destinations
        fields = ['Destination_City', 'Departure_City', 'Station_Location_Name']

        widgets = {
            'Destination_City': TextInput(attrs={'type': 'text'}, ),
        }


class AdminStationLocationFilter(django_filters.FilterSet):
    class Meta:
        model = StationLocation
        fields = ['Station_Name']


# class SearchScheduleDateTimeFilter(django_filters.FilterSet):
#     # destination_id = django_filters.ModelChoiceFilter(
#     #     queryset=DriverScheduleAvailabilities.objects.filter(),
#     #     label='Destination')
#     Departure_Date_Time = django_filters.DateTimeFilter(widget=DateTimeInput(attrs={'type': 'datetime-local'}))
#
#     class Meta:
#         model = DriverScheduleAvailabilities
#         fields = ['Departure_Date_Time']