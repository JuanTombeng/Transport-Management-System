from django.core.mail import send_mail
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy, reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from users.decorators import admin_only, allowed_users
from django.utils.decorators import method_decorator
from django.views import View
from .models import *
from .filters import DestinationFilter, DriverScheduleAvailabilitiesFilter, ScheduleAvailableFilter, \
    AdminDriverScheduleFilter, AdminVehicleFilter, AdminDestinationFilter, AdminStationLocationFilter
from .forms import CreateDriverScheduleForm, StatusUpdateDriverScheduleForm
from django import template
from django.contrib.auth.models import Group


def home(request):
    driverscheduleavailabilities = DriverScheduleAvailabilities.objects.all().select_related('Driver_Staff_ID',
                                                                                             'destination_id',
                                                                                             'Vehicle_Plate_Number')
    scheduleFilter = DriverScheduleAvailabilitiesFilter(request.GET, queryset=driverscheduleavailabilities)
    driverscheduleavailabilities = scheduleFilter.qs
    context = {
        'posts': Bookings.objects.all(),
        'driverscheduleavailabilities': driverscheduleavailabilities,
        'scheduleFilter': scheduleFilter,
    }
    return render(request, 'booking/home.html')


def about(request):
    return render(request, 'booking/about_us.html')


# @allowed_users(allowed_roles=['admin'])
def list_destinations(request):
    destinations = Destinations.objects.all()
    myFilter = DestinationFilter(request.GET, queryset=destinations)
    destinations = myFilter.qs

    return render(request, "booking/list_destinations.html", {'destinations': destinations, 'myFilter': myFilter})


# def search_schedules(request):
#     if request.method == "POST":
#         searched = request.POST['searched']
#         schedules = DriverScheduleAvailabilities.objects.filter(destination_id__Destination_City__icontains=searched)
#         return render(request, 'booking/search_schedule.html', {'searched': searched, 'schedules': schedules})
#     else:
#         return render(request, 'booking/search_schedule.html', {})


class BookingList(LoginRequiredMixin, ListView):
    model = Bookings
    context_object_name = 'bookings'
    template_name = 'booking/my_booking.html'

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['bookings'] = context['bookings'].filter(Customer=self.request.user)
    #     return context


class BookingDetail(DetailView):
    model = Bookings
    context_object_name = 'booking'
    bookings = Bookings.objects.all()
    template_name = 'booking/bookings_detail.html'


class BookingUpdate(LoginRequiredMixin, UpdateView):
    model = Bookings
    fields = ['Available_Trips',
              'Booking_Number_Of_Passengers',
              'Booking_Number_Of_Luggage',
              'Booking_Special_Condition',
              ]

    def get_object(self):
        Booking_id = self.kwargs.get("pk")
        object1 = Bookings.objects.get(pk=Booking_id)
        # object1 = get_object_or_404(Bookings, id=Booking_id)
        return object1

    def get_success_url(self):
        return reverse_lazy('booking-detail', kwargs={'pk': self.object.pk})


class BookingDelete(LoginRequiredMixin, DetailView):
    model = Bookings
    context_object_name = 'bookings'
    success_url = reverse_lazy('my-booking')


# @method_decorator(admin_only, name='dispatch')
class PaymentList(LoginRequiredMixin, ListView):
    model = Payments
    context_object_name = 'payments'
    template_name = 'booking/my_payment.html'

    # def get_context_data(self, **kwargs):
    #     context = super(PaymentList, self).get_context_data(**kwargs)
    #     context['PaymentID'] = self.request.user
    #     return context

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['PaymentID'] = self.request.user
        return context

    # @method_decorator(admin_only, name='dispatch')
    # def dispatch(self, request, *args, **kwargs):
    #     return super().dispatch(*args, **kwargs)

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['payments'] = context['payments'].filter(booking_id=Payments.booking_id.Customer)
    #     return context


class BookingPaymentList(LoginRequiredMixin, ListView):
    model = Payments
    context_object_name = 'payments'
    template_name = 'booking/booking-to-payment.html'

    def get_context_data(self, **kwargs):
        context = super(BookingPaymentList, self).get_context_data(**kwargs)
        context['PaymentID'] = self.request.user
        return context
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['payments'] = context['payments'].filter(PaymentID=Payments.PaymentID)
    #     return context


# class BookingPaymentDetail(DetailView):
#     model = Payments
#     context_object_name = 'payments'
#     payments = Payments.objects.all()
#     template_name = 'booking/booking-to-payment.html'
#
#     def get_context_data(self, **kwargs):
#         context = super(BookingPaymentDetail, self).get_context_data(**kwargs)
#         context[''] = self.request.user
#         return context


class PaymentDetail(DetailView):
    model = Payments
    context_object_name = 'payment'
    payments = Payments.objects.all()
    template_name = 'booking/payment_detail.html'


class PaymentUpdate(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Payments
    fields = ['paymentMethod',
              'paymentReceiptPicture',
              ]

    # def get_object(self):
    #     PaymentID = self.kwargs.get("id")
    #     object1 = get_object_or_404(Payments, PaymentID=PaymentID)
    #     return object1
    success_message = "Your Payment has been Updated."

    def get_success_url(self):
        return reverse_lazy('payment-detail', kwargs={'pk': self.object.pk})


def search_schedules(request):
    if request.method == "POST":
        searched = request.POST['searched']
        schedules = DriverScheduleAvailabilities.objects.filter(destination_id__Destination_City__icontains=searched)
        #     return render(request, 'booking/search_schedule.html', {'searched': searched, 'schedules1': schedules1})
        # else:
        #     return render(request, 'booking/search_schedule.html', {})
        return render(request, "booking/search_schedule.html",
                      {'searched': searched,
                       'schedules': schedules})


# def search_schedule_date(request):
#     schedules = DriverScheduleAvailabilities.objects.all()
#     searchScheduleFilter = SearchScheduleDateTimeFilter(request.GET, queryset=schedules)
#     schedules = searchScheduleFilter.qs
#
#     return render(request, "booking/search_schedule.html",
#                   {'schedules': schedules,
#                    'searchScheduleFilter': searchScheduleFilter})


class ScheduleDetail(DetailView):
    model = DriverScheduleAvailabilities
    context_object_name = 'driverscheduleavailability'
    payments = DriverScheduleAvailabilities.objects.all()
    template_name = 'booking/schedule_detail.html'


class DriverScheduleList(LoginRequiredMixin, ListView):
    model = DriverScheduleAvailabilities
    context_object_name = 'driverschedules'
    template_name = 'booking/my_driver_schedule.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['driverschedules'] = \
            context['driverschedules'].filter(Driver_Staff_ID=self.request.user)
        return context

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['Driver_Staff_ID'] = self.request.user
    #     return context


class DriverScheduleDetail(DetailView):
    model = DriverScheduleAvailabilities
    context_object_name = 'driverschedule'
    driverschedules = DriverScheduleAvailabilities.objects.all()
    template_name = 'booking/driver_schedule_detail.html'


class BookingCancelUpdate(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Payments
    fields = ['Cancellation_Confirmation_Status',
              ]
    success_message = "Your Booking has been canceled."

    def get_success_url(self):
        return reverse_lazy('payment-detail', kwargs={'pk': self.object.pk})


class CanceledBookingList(LoginRequiredMixin, ListView):
    model = Payments
    context_object_name = 'payments'
    template_name = 'booking/my_canceled_booking.html'

    # def get_context_data(self, **kwargs):
    #     context = super(PaymentList, self).get_context_data(**kwargs)
    #     context['PaymentID'] = self.request.user
    #     return context

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['PaymentID'] = self.request.user
        return context


class CanceledBookingDetail(DetailView):
    model = Payments
    context_object_name = 'payment'
    payments = Payments.objects.all()
    template_name = 'booking/canceled_booking_detail.html'


class FinancierPaymentList(LoginRequiredMixin, ListView):
    model = Payments
    context_object_name = 'payments'
    template_name = 'booking/my_financier_payment.html'


class FinancierPaymentDetail(DetailView):
    model = Payments
    context_object_name = 'payment'
    payments = Payments.objects.all()
    template_name = 'booking/financier_payment_detail.html'


class FinancierPaymentUpdate(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Payments
    fields = ['paymentConfirmationStatus']
    success_message = "Payment has been updated."

    # send_mail('Payment Update from TMS',
    #           'Dear Customer, you payment has been received and updated.',
    #           '201700165j@gmail.com',
    #           [Payments.booking_id.Customer.email]
    #           )
    def form_valid(self, form):
        form.instance.Financier = self.request.user
        return super(FinancierPaymentUpdate, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('financier-payment-detail', kwargs={'pk': self.object.pk})


def createbooking(request):
    context = []
    if request.method == 'POST':
        id_r = request.POST.get('schedule_id')
        lug_r = int(request.POST.get('no_lug'))
        pass_r = int(request.POST.get('no_pass'))
        spec_con = str(request.POST.get('special_con'))
        seats_r = lug_r + pass_r
        schedule = DriverScheduleAvailabilities.objects.get(id=id_r)
        if schedule:
            if schedule.Remaining_Seat > seats_r:
                trip_name = schedule
                total_seats = seats_r
                price = total_seats * schedule.destination_id.Destination_Final_Price
                special_cond = spec_con
                customer = request.user
                sche_rem = schedule.Remaining_Seat - total_seats
                DriverScheduleAvailabilities.objects.filter(id=id_r).update(Remaining_Seat=sche_rem)
                DriverScheduleAvailabilities.objects.filter(id=id_r).update(Schedule_Status=True)
                Book = Bookings.objects.create(Customer=customer, Available_Trips=trip_name,
                                               Booking_Number_Of_Passengers=pass_r, Booking_Number_Of_Luggage=lug_r,
                                               Booking_Special_Condition=special_cond, Booking_Total_Seats=total_seats,
                                               Booking_Total_Price=price, Booking_Status='Pending')
                messages.success(request, 'Your Booking is under process!')
                return render(request, 'booking/booking_success.html', locals())
            else:
                messages.error(request, 'Select fewer number of seats')
                return render(request, 'booking/bookings_form.html')
    else:
        return render(request, 'booking/bookings_form.html')


class AdminBookingCreate(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Bookings
    fields = ['Customer',
              'Available_Trips',
              'Booking_Number_Of_Passengers',
              'Booking_Number_Of_Luggage',
              'Booking_Special_Condition',
              'Booking_Total_Seats',
              'Booking_Total_Price',
              ]
    success_url = reverse_lazy('admin-my-booking')
    success_message = "Booking: %(Customer)s with trip: %(Available_Trips)s has been booked."

    def form_valid(self, form):
        form.instance.Profile = self.request.user
        return super(AdminBookingCreate, self).form_valid(form)


class AdminVehicleCreate(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Vehicles
    fields = '__all__'
    success_url = reverse_lazy('admin-my-vehicle')
    success_message = "Vehicle: %(plateNumber)s has been created."

    def form_valid(self, form):
        form.instance.Profile = self.request.user
        return super(AdminVehicleCreate, self).form_valid(form)


class AdminStationLocationCreate(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = StationLocation
    fields = '__all__'
    success_url = reverse_lazy('admin-my-station-location')
    success_message = "Station Location: %(Station_Name)s has been created."

    def form_valid(self, form):
        form.instance.Profile = self.request.user
        return super(AdminStationLocationCreate, self).form_valid(form)


class AdminDestinationCreate(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Destinations
    fields = ['Destination_Name',
              'Destination_City',
              'Destination_District',
              'Destination_Address',
              'Departure_City',
              'Departure_Address',
              'Destination_Distance',
              'Destination_Price_Per_KiloMeter',
              'Station_Location_Name']
    success_url = reverse_lazy('admin-my-destination')
    success_message = "Destination: from %(Departure_City)s to %(Destination_Name)s has been created."

    def form_valid(self, form):
        form.instance.Profile = self.request.user
        return super(AdminDestinationCreate, self).form_valid(form)


class AdminDriverScheduleCreate(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    template_name = 'booking/admin/admin_driver_schedule_form.html'
    form_class = CreateDriverScheduleForm
    success_url = reverse_lazy('admin-my-driver-schedule')
    success_message = "Driver: %(Driver_Staff_ID)s has been created."

    def form_valid(self, form):
        form.instance.Profile = self.request.user
        return super(AdminDriverScheduleCreate, self).form_valid(form)


class AdminBookingList(LoginRequiredMixin, ListView):
    model = Bookings
    context_object_name = 'bookings'
    template_name = 'booking/admin/my_booking.html'


class AdminPaymentList(LoginRequiredMixin, ListView):
    model = Payments
    context_object_name = 'payments'
    template_name = 'booking/admin/my_payment.html'


# class AdminVehicleList(LoginRequiredMixin, ListView):
#     model = Vehicles
#     context_object_name = 'vehicles'
#     template_name = 'booking/admin/my_vehicles.html'


class AdminStationLocationList(LoginRequiredMixin, ListView):
    model = StationLocation
    context_object_name = 'stationlocations'
    template_name = 'booking/admin/my_station_location.html'


class AdminDestinationList(LoginRequiredMixin, ListView):
    model = Destinations
    context_object_name = 'destinations'
    template_name = 'booking/admin/my_destination.html'


class AdminDriverScheduleAvailabilityList(LoginRequiredMixin, ListView):
    model = DriverScheduleAvailabilities
    context_object_name = 'driverscheduleavailabilities'
    template_name = 'booking/admin/my_driver_schedule.html'


class AdminBookingDetail(LoginRequiredMixin, DetailView):
    model = Bookings
    context_object_name = 'booking'
    payments = Bookings.objects.all()
    template_name = 'booking/admin/my_booking_detail.html'


class AdminVehicleDetail(LoginRequiredMixin, DetailView):
    model = Vehicles
    context_object_name = 'vehicle'
    payments = Vehicles.objects.all()
    template_name = 'booking/admin/my_vehicle_detail.html'


class AdminStationLocationDetail(LoginRequiredMixin, DetailView):
    model = StationLocation
    context_object_name = 'stationlocation'
    payments = StationLocation.objects.all()
    template_name = 'booking/admin/my_station_location_detail.html'


class AdminDestinationDetail(LoginRequiredMixin, DetailView):
    model = Destinations
    context_object_name = 'destination'
    payments = Destinations.objects.all()
    template_name = 'booking/admin/my_destination_detail.html'


class AdminDriverScheduleDetail(LoginRequiredMixin, DetailView):
    model = DriverScheduleAvailabilities
    context_object_name = 'driverscheduleavalability'
    driverscheduleavalabilities = DriverScheduleAvailabilities.objects.all()
    template_name = 'booking/admin/my_driver_schedule_detail.html'





class AdminVehicleUpdate(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Vehicles
    fields = '__all__'
    success_message = "Vehicle %(plateNumber)s has been updated."

    def get_success_url(self):
        return reverse_lazy('admin-vehicle-detail', kwargs={'pk': self.object.pk})


class AdminStationLocationUpdate(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = StationLocation
    fields = '__all__'
    success_message = "Station Location: %(Station_Name)s has been updated."

    def get_success_url(self):
        return reverse_lazy('admin-station-location-detail', kwargs={'pk': self.object.pk})


class AdminDestinationUpdate(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Destinations
    fields = ['Destination_Name',
              'Destination_City',
              'Destination_District',
              'Destination_Address',
              'Departure_City',
              'Departure_Address',
              'Destination_Distance',
              'Destination_Price_Per_KiloMeter',
              'Station_Location_Name']
    success_message = "Destination: from %(Departure_City)s to %(Destination_Name)s has been updated."

    def get_success_url(self):
        return reverse_lazy('admin-destination-detail', kwargs={'pk': self.object.pk})


class AdminDriverScheduleUpdate(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = DriverScheduleAvailabilities
    form_class = CreateDriverScheduleForm
    success_message = "Driver Schedule for Driver: %(Driver_Staff_ID)s has been updated."

    def get_success_url(self):
        return reverse_lazy('admin-driver-schedule-detail', kwargs={'pk': self.object.pk})


class AdminStatusDriverScheduleUpdate(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = DriverScheduleAvailabilities
    form_class = StatusUpdateDriverScheduleForm
    success_message = "Driver Schedule for Driver: %(Driver_Staff_ID)s has been updated."

    def get_success_url(self):
        return reverse_lazy('admin-driver-schedule-detail', kwargs={'pk': self.object.pk})


class AdminVehicleDelete(LoginRequiredMixin, DeleteView):
    model = Vehicles
    context_object_name = 'vehicle'
    success_url = reverse_lazy('admin-vehicle-delete')

    def get_success_url(self):
        return reverse_lazy('admin-my-vehicle')





# class AdminVehicleDelete(LoginRequiredMixin, DeleteView):
#     model = Vehicles
#     context_object_name = 'vehicle'
#     success_url = reverse_lazy('admin-vehicle-delete')
#
#     def get_object(self):
#         obj = get_object_or_404(Vehicles, plateNumber=self.kwargs['plateNumber'])
#         return obj

# def get_success_url(self):
#     return reverse_lazy('admin-my-vehicle')

# def AdminVehicleDelete(request, id):
#     vehicle = get_object_or_404(Vehicles, pk=id).delete()
#
#     return reverse_lazy('admin-my-vehicle')



class AdminStationLocationDelete(LoginRequiredMixin, DeleteView):
    model = StationLocation
    context_object_name = 'stationlocation'
    success_url = reverse_lazy('admin-station-location-delete')

    def get_success_url(self):
        return reverse_lazy('admin-my-station-location')


class AdminDestinationDelete(LoginRequiredMixin, DeleteView):
    model = Destinations
    context_object_name = 'destination'
    success_url = reverse_lazy('admin-destination-delete')

    def get_success_url(self):
        return reverse_lazy('admin-my-destination')


class AdminDriverScheduleDelete(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = DriverScheduleAvailabilities
    context_object_name = 'driverscheduleavailabilitiy'
    success_url = reverse_lazy('admin-driver-schedule-delete')
    success_message = "Driver Schedule for Driver: %(Driver_Staff_ID)s has been deleted."

    def get_success_url(self):
        return reverse_lazy('admin-my-driver-schedule')


def admin_driver_schedule_list(request):
    driverscheduleavailabilities = DriverScheduleAvailabilities.objects.all()
    driverScheduleFilter = AdminDriverScheduleFilter(request.GET, queryset=driverscheduleavailabilities)
    driverscheduleavailabilities = driverScheduleFilter.qs

    return render(request, "booking/admin/my_driver_schedule.html",
                  {'driverscheduleavailabilities': driverscheduleavailabilities,
                   'driverScheduleFilter': driverScheduleFilter})


def admin_vehicle_search_list(request):
    vehicles = Vehicles.objects.all()
    vehicleFilter = AdminVehicleFilter(request.GET, queryset=vehicles)
    vehicles = vehicleFilter.qs

    return render(request, "booking/admin/my_vehicles.html",
                  {'vehicles': vehicles,
                   'vehicleFilter': vehicleFilter})


def admin_destination_search_list(request):
    destinations = Destinations.objects.all()
    destinationFilter = AdminDestinationFilter(request.GET, queryset=destinations)
    destinations = destinationFilter.qs

    return render(request, "booking/admin/my_destination.html",
                  {'destinations': destinations,
                   'destinationFilter': destinationFilter})


def admin_station_location_search_list(request):
    stationlocations = StationLocation.objects.all()
    stationlocationFilter = AdminStationLocationFilter(request.GET, queryset=stationlocations)
    stationlocations = stationlocationFilter.qs

    return render(request, "booking/admin/my_station_location.html",
                  {'stationlocations': stationlocations,
                   'stationlocationFilter': stationlocationFilter})
