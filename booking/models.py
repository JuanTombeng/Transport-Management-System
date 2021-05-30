from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from users.models import Account
from django.conf import settings
from django.db.models.signals import post_save
from safedelete.models import SafeDeleteModel
from safedelete.models import SOFT_DELETE_CASCADE


class StationLocation(SafeDeleteModel):
    id = models.AutoField(primary_key=True)
    Station_Name = models.CharField(max_length=255)
    Station_Address = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    _safedelete_policy = SOFT_DELETE_CASCADE

    def __str__(self):
        return self.Station_Name



class Destinations(SafeDeleteModel):
    id = models.AutoField(primary_key=True)
    Destination_Name = models.CharField(max_length=255)
    Destination_City = models.CharField(max_length=255)
    Destination_District = models.CharField(max_length=255)
    Destination_Address = models.TextField()
    Departure_City = models.CharField(max_length=255)
    Departure_Address = models.TextField()
    Destination_Distance = models.DecimalField(max_digits=10, decimal_places=2)
    Destination_Price_Per_KiloMeter = models.DecimalField(max_digits=10, decimal_places=2)
    Destination_Final_Price = models.DecimalField(max_digits=10, decimal_places=2)
    Station_Location_Name = models.ForeignKey(StationLocation, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    _safedelete_policy = SOFT_DELETE_CASCADE

    def kilometer_price(self):
        kp = self.Destination_Price_Per_KiloMeter * self.Destination_Distance
        return kp

    def save(self, *args, **kwargs):
        self.Destination_Final_Price = self.kilometer_price()
        super(Destinations, self).save(*args, **kwargs)

    def __str__(self):
        return f'Destination ID: {self.id} | Name: {self.Destination_Name}'


class Vehicles(SafeDeleteModel):
    id = models.AutoField(primary_key=True)
    type = models.CharField(max_length=255)
    brand = models.CharField(max_length=255)
    plateNumber = models.CharField(max_length=255)
    gasolineType = models.CharField(max_length=255)
    color = models.CharField(max_length=255)
    capacity = models.DecimalField(max_digits=10, decimal_places=2)
    kilometerRecord = models.DecimalField(max_digits=10, decimal_places=2)
    currentMaintenanceIssue = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    _safedelete_policy = SOFT_DELETE_CASCADE

    def __str__(self):
        return self.plateNumber

    def get_absolute_url(self):
        return reverse('admin-vehicle-detail', kwargs={'pk': self.pk})


class DriverScheduleAvailabilities(SafeDeleteModel):
    id = models.AutoField(primary_key=True)
    Driver_Staff_ID = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                        limit_choices_to={'groups__name': "Driver Department"})
    destination_id = models.ForeignKey(Destinations, on_delete=models.CASCADE)
    Vehicle_Plate_Number = models.ForeignKey(Vehicles, on_delete=models.CASCADE)
    Departure_Date_Time = models.DateTimeField(auto_now_add=False, auto_now=False)
    tripHoursDuration = models.IntegerField()
    Return_Date_Time = models.DateTimeField(auto_now_add=False, auto_now=False, blank=True)
    Number_of_Seat = models.DecimalField(max_digits=10, decimal_places=0)
    Remaining_Seat = models.DecimalField(max_digits=10, decimal_places=0)
    Schedule_Status = models.BooleanField(default=False)
    Active_Status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    _safedelete_policy = SOFT_DELETE_CASCADE

    def __str__(self):
        return f'Destination = {self.destination_id.Destination_Name} | Date: {self.Departure_Date_Time}'

    def number_of_seat(self):
        nos = self.Vehicle_Plate_Number.capacity
        return nos

    @property
    def schedule_status(self):
        ss = self.Remaining_Seat < self.Number_of_Seat
        if ss is True:
            self.Schedule_Status = True
        return self.Schedule_Status

    def save(self, *args, **kwargs):
        self.Number_of_Seat = self.number_of_seat()
        self.Schedule_Status = self.schedule_status
        super(DriverScheduleAvailabilities, self).save(*args, **kwargs)


class Bookings(SafeDeleteModel):
    BOOKING_STATUS = (
        ('Pending', 'Pending'),
        ('Confirmed', 'Confirmed'),
        ('Canceled', 'Canceled'),
    )
    id = models.AutoField(primary_key=True)
    Customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    Available_Trips = models.ForeignKey(DriverScheduleAvailabilities, on_delete=models.CASCADE)
    Booking_Number_Of_Passengers = models.DecimalField(max_digits=10, decimal_places=2)
    Booking_Number_Of_Luggage = models.DecimalField(max_digits=10, decimal_places=2)
    Booking_Special_Condition = models.TextField(max_length=255)
    Booking_Total_Seats = models.DecimalField(max_digits=10, decimal_places=2)
    Booking_Total_Price = models.DecimalField(max_digits=10, decimal_places=2)
    Booking_Status = models.CharField(max_length=255, choices=BOOKING_STATUS, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    _safedelete_policy = SOFT_DELETE_CASCADE

    class Meta:
        order_with_respect_to = 'Customer'

    def get_absolute_url(self):
        return reverse('booking-details', kwargs={'pk': self.pk})

    def __str__(self):
        return "Booking ID: " + str(self.id)


class Payments(SafeDeleteModel):
    PAYMENT_STATUS = (
        ('Unpaid', 'Unpaid'),
        ('Pending', 'Pending'),
        ('Fully Paid', 'Fully Paid'),
    )
    PAYMENT_METHOD = (
        ('Personal Account', 'Personal Account'),
        ('Bank Transfer', 'Bank Transfer'),
    )
    CANCEL_STATUS = (
        ('Confirmed', 'Confirmed'),
        ('Not Cancel', 'Not Cancel'),
    )
    PaymentID = models.AutoField(primary_key=True)
    Financier = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True,
                                  limit_choices_to={'groups__name': "Finance Department"})
    booking_id = models.OneToOneField(Bookings, on_delete=models.CASCADE)
    paymentMethod = models.CharField(max_length=255, choices=PAYMENT_METHOD, default=None, null=True)
    paymentReceiptPicture = models.ImageField(upload_to='receipt_pics/', blank=True)
    paymentConfirmationStatus = models.CharField(max_length=255, choices=PAYMENT_STATUS, default=None)
    Cancellation_Confirmation_Status = models.CharField(max_length=255, choices=CANCEL_STATUS, default='Not Cancel')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    _safedelete_policy = SOFT_DELETE_CASCADE

    def __str__(self):
        return f'Payment ID: {self.PaymentID} | {self.booking_id}'

    class Meta:
        verbose_name_plural = "Payments"


def create_payment_on_booking(sender, instance, **kwargs):
    if instance.Booking_Status:
        Payments.objects.create(booking_id=instance, paymentConfirmationStatus='Unpaid')


post_save.connect(create_payment_on_booking, sender=Bookings)

