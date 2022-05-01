from django.contrib.auth.mixins import LoginRequiredMixin, \
    UserPassesTestMixin, AccessMixin
from django.contrib.auth.views import LoginView
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.utils.translation import gettext
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, \
    FormView
from users.models import User
from users.forms import RegisterUserForm, AuthUserForm


# Create your views here.
class UsersList(ListView):
    model = User
    template_name = 'users/users.html'
    context_object_name = 'users'


class CreateUser(CreateView, SuccessMessageMixin):
    model = User
    template_name = 'users/register.html'
    form_class = RegisterUserForm
    success_url = reverse_lazy('login')


class LoginUser(LoginView, SuccessMessageMixin):
    model = User
    template_name = 'users/login.html'
    form_class = AuthUserForm
    success_url = reverse_lazy('')


class UpdateUser(LoginRequiredMixin,
                 SuccessMessageMixin,
                 UserPassesTestMixin,
                 AccessMixin,
                 UpdateView,
                 FormView,):
    model = User
    template_name = 'users/update.html'
    form_class = RegisterUserForm
    success_url = reverse_lazy('users:list')
    error_message = 'You do not have permission to change another user'
    no_permission_url = 'users:list'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['button_text'] = gettext('Изменить пользователя')
        return context

    def test_func(self):
        return self.request.user == self.get_object()

    def handle_no_permission(self):
        messages.error(self.request, self.error_message)
        return redirect(self.no_permission_url)


class DeleteUser(LoginRequiredMixin,
                 SuccessMessageMixin,
                 UserPassesTestMixin,
                 AccessMixin,
                 DeleteView,
                 FormView,):
    model = User
    template_name = 'users/delete.html'
    success_url = reverse_lazy('users:list')
    error_message = 'You do not have permission to change another user'
    no_permission_url = 'users:list'

    def test_func(self):
        return self.request.user == self.get_object()

    def handle_no_permission(self):
        messages.error(self.request, self.error_message)
        return redirect(self.no_permission_url)
