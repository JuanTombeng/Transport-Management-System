import django_filters
from django.forms import DateTimeInput, TextInput
from django_filters import DateTimeFilter

from booking.models import DriverScheduleAvailabilities
from .models import *


class AdminUserFilter(django_filters.FilterSet):
    class Meta:
        model = Account
        fields = ['email', 'name', 'groups']

    def __init__(self, *args, **kwargs):
        super(AdminUserFilter, self).__init__(*args, **kwargs)
        self.filters['groups'].extra.update(
            {'empty_label': '---User Group---'})


