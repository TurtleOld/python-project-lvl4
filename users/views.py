from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
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
                 UpdateView,):
    model = User
    template_name = 'users/update.html'
    form_class = RegisterUserForm
    success_url = reverse_lazy('users:list')


class DeleteUser(LoginRequiredMixin,
                 SuccessMessageMixin,
                 DeleteView,):
    model = User
    template_name = 'users/delete.html'
    success_url = reverse_lazy('users:list')
