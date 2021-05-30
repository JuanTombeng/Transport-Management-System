from django.contrib.auth.views import PasswordChangeView
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.shortcuts import render

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse, reverse_lazy
from .models import Account
from booking.models import *
from booking.filters import *
from .forms import RegistrationForm, UserCreationForm, UserChangeForm, ProfileUpdateForm
from .filters import AdminUserFilter


class RegistrationView(SuccessMessageMixin, CreateView):
    template_name = 'users/user_registration.html'
    form_class = RegistrationForm
    success_message = "Account %(name)s has been created."

    def get_context_data(self, *args, **kwargs):
        context = super(RegistrationView, self).get_context_data(*args, **kwargs)
        context['next'] = self.request.GET.get('next')
        return context

    def get_success_url(self):
        return reverse('login')


class AdminRegistrationView(SuccessMessageMixin, CreateView):
    template_name = 'users/admin_user_registration.html'
    form_class = UserCreationForm
    success_message = "Account %(name)s has been created."

    def get_context_data(self, *args, **kwargs):
        context = super(AdminRegistrationView, self).get_context_data(*args, **kwargs)
        context['next'] = self.request.GET.get('next')
        return context

    def get_success_url(self):
        return reverse('admin_user_list')

    # def get_success_url(self):
    #     next_url = self.request.POST.get('next')
    #     success_url = reverse('login')
    #     if next_url:
    #         success_url += '?next={}'.format(next_url)
    #
    #     return success_url


class ProfileView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Account
    form_class = ProfileUpdateForm
    template_name = 'users/profile.html'
    success_message = "Your Profile has been updated."

    def get_success_url(self):
        return reverse('profile')

    def get_object(self):
        return self.request.user


# class AdminDestinationList(LoginRequiredMixin, ListView):
#     model = Account
#     context_object_name = 'accounts'
#     template_name = 'users/user_list.html'


class AdminUserDetail(LoginRequiredMixin, DetailView):
    model = Account
    context_object_name = 'account'
    accounts = Account.objects.all()
    template_name = 'users/user_detail.html'


class AdminUpdateUserView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Account
    form_class = UserChangeForm
    success_message = "User %(name)s has been updated."

    def get_success_url(self):
        return reverse_lazy('admin_user_detail', kwargs={'pk': self.object.pk})


class AdminUserDeleteView(LoginRequiredMixin, DeleteView):
    model = Account
    context_object_name = 'account'
    success_url = reverse_lazy('admin_user_delete')

    def get_success_url(self):
        return reverse_lazy('admin_user_list')


class PasswordsChangeView(LoginRequiredMixin, SuccessMessageMixin, PasswordChangeView):
    form_class = PasswordChangeForm
    success_url = reverse_lazy('profile')
    success_message = "Your password has been changed."


def admin_user_search_list(request):
    accounts = Account.objects.all()
    accountFilter = AdminUserFilter(request.GET, queryset=accounts)
    accounts = accountFilter.qs

    return render(request, "users/user_list.html",
                  {'accounts': accounts,
                   'accountFilter': accountFilter})
