from django.conf.urls import url
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from users.decorators import admin_only, staff_member_required
from .views import (
    BookingList, BookingDetail, BookingUpdate, BookingDelete, PaymentUpdate,
    PaymentList, PaymentDetail, BookingPaymentList, ScheduleDetail, DriverScheduleList,
    DriverScheduleDetail, BookingCancelUpdate, CanceledBookingList, CanceledBookingDetail, FinancierPaymentList,
    FinancierPaymentDetail, FinancierPaymentUpdate, AdminBookingCreate, AdminBookingList, AdminBookingDetail,
    AdminStationLocationList, AdminVehicleDetail, AdminStationLocationDetail, AdminDestinationList,
    AdminDestinationDetail, AdminDriverScheduleDetail, AdminVehicleUpdate,
    AdminStationLocationUpdate, AdminDestinationUpdate, AdminDriverScheduleUpdate, AdminVehicleDelete,
    AdminStationLocationDelete, AdminDestinationDelete, AdminDriverScheduleDelete, AdminStatusDriverScheduleUpdate
)
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    # path('', BookingList.as_view(), name='tasks'),
    path('about/', views.about, name='about-us'),
    path('destinations/', views.list_destinations, name='destinations'),

    path('booking/admin/driver-schedule/my/', views.admin_driver_schedule_list, name='admin-my-driver-schedule'),
    path('booking/admin/vehicle/my/', views.admin_vehicle_search_list, name='admin-my-vehicle'),
    path('booking/admin/destination/my/', views.admin_destination_search_list, name='admin-my-destination'),
    path('booking/admin/station-location/my/', views.admin_station_location_search_list,
         name='admin-my-station-location'),

    path('booking/new/', views.createbooking, name='booking-create'),
    path('booking/my/', staff_member_required(BookingList.as_view()), name='my-booking'),
    path('booking/my/<int:pk>/', BookingDetail.as_view(), name='booking-detail'),
    # path('booking/my/update/<int:pk>/', BookingUpdate.as_view(), name='booking-update'),
    # path('task-delete/<int:pk>/', BookingDelete.as_view(), name='task-delete'),

    path('booking-payment/my/', PaymentList.as_view(), name='my-payment'),
    path('booking-to-payment/my/detail/<int:pk>/', PaymentDetail.as_view(), name='payment-detail'),
    path('booking-to-payment/my/update/<int:pk>/', PaymentUpdate.as_view(), name='payment-update'),

    path('booking-to-payment/', BookingPaymentList.as_view(), name='booking-to-payment'),
    path('booking/search-schedules/', views.search_schedules, name='search-schedules'),
    path('booking/schedule-detail/<int:pk>/', ScheduleDetail.as_view(), name='schedule-detail'),

    path('driver-schedule/my/', staff_member_required(DriverScheduleList.as_view()), name='my-driver-schedule'),
    path('driver-schedule/my/detail/<int:pk>/', staff_member_required(DriverScheduleDetail.as_view()),
         name='driver-schedule-detail'),

    path('booking/my/update/<int:pk>/', BookingCancelUpdate.as_view(template_name='booking/booking_cancel.html'),
         name='booking-status-update'),
    path('canceled-booking/my/', CanceledBookingList.as_view(), name='my-canceled-booking'),
    path('canceled-booking/my/detail/<int:pk>/', CanceledBookingDetail.as_view(), name='canceled-booking-detail'),

    path('financier-payment/my/', staff_member_required(FinancierPaymentList.as_view()), name='my-financier-payment'),
    path('financier-payment/my/detail/<int:pk>/', staff_member_required(FinancierPaymentDetail.as_view()),
         name='financier-payment-detail'),
    path('financier-payment/my/update/<int:pk>/', staff_member_required(FinancierPaymentUpdate.as_view(
        template_name='booking/financier_payment_form.html')), name='financier-payment-update'),

    # ADMIN URLS
    path('booking/admin/booking/new/', views.AdminBookingCreate.as_view(
        template_name='booking/admin/admin_booking_form.html'),
         name='admin-booking-create'),
    path('booking/admin/booking/my/', staff_member_required(AdminBookingList.as_view()), name='admin-my-booking'),
    path('booking/admin/booking/my/<int:pk>/', AdminBookingDetail.as_view(), name='admin-booking-detail'),
    # path('task-delete/<int:pk>/', BookingDelete.as_view(), name='task-delete'),

    path('booking/admin/vehicle/new/', views.AdminVehicleCreate.as_view(
        template_name='booking/admin/admin_vehicle_form.html'),
         name='admin-vehicle-create'),
    # path('booking/admin/vehicle/my/', staff_member_required(AdminVehicleList.as_view()),
    #      name='admin-my-vehicle'),
    path('booking/admin/vehicle/my/<int:pk>/', AdminVehicleDetail.as_view(), name='admin-vehicle-detail'),
    path('booking/admin/vehicle/my/update/<int:pk>/', AdminVehicleUpdate.as_view(
        template_name='booking/admin/admin_vehicle_form.html'), name='admin-vehicle-update'),
    path('booking/admin/vehicle/my/delete/<int:pk>/', AdminVehicleDelete.as_view(
        template_name='booking/admin/vehicles_confirm_delete.html'), name='admin-vehicle-delete'),
    # url(r'^(?P<plateNumber>\w+)/$', AdminVehicleDelete.as_view(
    #     template_name='booking/admin/vehicles_confirm_delete.html'), name='admin-vehicle-delete'),

    path('booking/admin/station-location/new/', views.AdminStationLocationCreate.as_view(
        template_name='booking/admin/admin_station_location_form.html'),
         name='admin-station-location-create'),
    # path('booking/admin/station-location/my/', staff_member_required(AdminStationLocationList.as_view()),
    #      name='admin-my-station-location'),
    path('booking/admin/station-location/my/<int:pk>/', AdminStationLocationDetail.as_view(),
         name='admin-station-location-detail'),
    path('booking/admin/station-location/my/update/<int:pk>/', AdminStationLocationUpdate.as_view(
        template_name='booking/admin/admin_station_location_form.html'),
         name='admin-station-location-update'),
    path('booking/admin/station-location/my/delete/<int:pk>/', AdminStationLocationDelete.as_view(
        template_name='booking/admin/station_location_confirm_delete.html'),
         name='admin-station-location-delete'),

    path('booking/admin/destination/new/', views.AdminDestinationCreate.as_view(
        template_name='booking/admin/admin_destination_form.html'),
         name='admin-destination-create'),
    # path('booking/admin/destination/my/', staff_member_required(AdminDestinationList.as_view()),
    #      name='admin-my-destination'),
    path('booking/admin/destination/my/<int:pk>/', AdminDestinationDetail.as_view(),
         name='admin-destination-detail'),
    path('booking/admin/destination/my/update/<int:pk>/', AdminDestinationUpdate.as_view(
        template_name='booking/admin/admin_destination_form.html'),
         name='admin-destination-update'),
    path('booking/admin/destination/my/delete/<int:pk>/', AdminDestinationDelete.as_view(
        template_name='booking/admin/destination_confirm_delete.html'), name='admin-destination-delete'),

    path('booking/admin/driver-schedule/new/',
         staff_member_required(views.AdminDriverScheduleCreate.as_view(
             template_name='booking/admin/admin_driver_schedule_form.html')),
         name='admin-driver-schedule-create'),
    # path('booking/admin/driver-schedule/my/', staff_member_required(AdminDriverScheduleAvailabilityList.as_view()),
    #      name='admin-my-driver-schedule'),
    path('booking/admin/driver-schedule/my/<int:pk>/', AdminDriverScheduleDetail.as_view(),
         name='admin-driver-schedule-detail'),
    path('booking/admin/driver-schedule/my/update/<int:pk>/', staff_member_required(AdminDriverScheduleUpdate.as_view(
        template_name='booking/admin/admin_driver_schedule_form.html')),
         name='admin-driver-schedule-update'),
    path('booking/admin/driver-schedule/my/status/update/<int:pk>/', AdminStatusDriverScheduleUpdate.as_view(
        template_name='booking/admin/admin_driver_schedule_status_form.html'),
         name='admin-driver-schedule-status-update'),
    path('booking/admin/driver-schedule/my/delete/<int:pk>/', AdminDriverScheduleDelete.as_view(
        template_name='booking/admin/driver_schedule_confirm_delete.html'), name='admin-driver-schedule-delete'),


]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
