from django import forms
from django.contrib.admin.widgets import AdminSplitDateTime
from django.forms import DateTimeInput

from booking.models import DriverScheduleAvailabilities, Payments, Bookings
import datetime


class CustomBookingForm(forms.Form):
    Schedule = forms.ModelChoiceField(queryset=DriverScheduleAvailabilities.objects.all())
    # Departure_Date = forms.DateField(required=True, input_formats=['%m/%d/%Y', ])
    Departure_Time = forms.TimeField(required=True, input_formats=['%H:%M:%S', ])
    # returnDate = forms.DateField(required=True, input_formats=['%m/%d/%Y', ])
    returnTime = forms.TimeField(required=True, input_formats=['%H:%M:%S', ])


class CreateDriverScheduleForm(forms.ModelForm):
    class Meta:
        model = DriverScheduleAvailabilities
        fields = 'Driver_Staff_ID', 'destination_id', 'Vehicle_Plate_Number', 'Departure_Date_Time', \
                 'tripHoursDuration', 'Return_Date_Time', 'Number_of_Seat', 'Remaining_Seat'

        widgets = {
            'Departure_Date_Time': DateTimeInput(attrs={'type': 'datetime-local'}),
            'Return_Date_Time': DateTimeInput(attrs={'type': 'datetime-local'}),
        }


class StatusUpdateDriverScheduleForm(forms.ModelForm):
    class Meta:
        model = DriverScheduleAvailabilities
        fields = ['Active_Status']
        exclude = ('Driver_Staff_ID',
                   'destination_id',
                   'Vehicle_Plate_Number',
                   'Departure_Date_Time',
                   'tripHoursDuration',
                   'Return_Date_Time',
                   'Number_of_Seat',
                   'Remaining_Seat',
                   'Schedule_Status')
