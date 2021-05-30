"""TransportManagement URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from users import views as user_views, views
from users.decorators import staff_member_required
from users.views import RegistrationView, PasswordsChangeView, ProfileView, AdminUpdateUserView, \
    AdminUserDetail, AdminUserDeleteView
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('booking.urls')),
    path('registration/', user_views.RegistrationView.as_view(), name='user_registration'),
    path('profile/', user_views.ProfileView.as_view(), name='profile'),
    path('user/login/', auth_views.LoginView.as_view(template_name='users/user_login.html'), name='login'),
    path('user/logout/', auth_views.LogoutView.as_view(template_name='users/user_logout.html'), name='logout'),

    path('password-reset/', auth_views.PasswordResetView.as_view(
        template_name='users/password/password_reset.html'),
         name='password_reset'),
    path('password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(template_name='users/password/password_reset_done.html'),
         name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='users/password/password_reset_confirm.html'),
         name='password_reset_confirm'),
    path('password-change/',
         PasswordsChangeView.as_view(template_name='users/password/password_change.html'),
         name='password_change'),
    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name='users/password/password_reset_complete.html'),
         name='password_reset_complete'),

    path('registration-admin/', user_views.AdminRegistrationView.as_view(), name='admin_user_registration'),
    # path('user-list-admin/', staff_member_required(user_views.AdminDestinationList.as_view()), name='admin_user_list'),
    path('user-list-admin/', views.admin_user_search_list, name='admin_user_list'),
    path('user-list-admin/<int:pk>/', AdminUserDetail.as_view(), name='admin_user_detail'),
    path('user-list-admin/update/<int:pk>/', AdminUpdateUserView.as_view(
        template_name='users/user_registration.html'), name='admin_user_update'),
    path('user-list-admin/delete/<int:pk>/', AdminUserDeleteView.as_view(
        template_name='users/user_confirm_delete.html'),
         name='admin_user_delete'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
