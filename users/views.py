from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from users.models import User
from users.forms import RegisterUserForm, AuthUserForm, UpdateUserForm


# Create your views here.
class UsersList(ListView):
    model = User
    template_name = 'users/users.html'
    context_object_name = 'users'


class CreateUser(CreateView, SuccessMessageMixin):
    model = User
    template_name = 'users/register.html'
    form_class = RegisterUserForm
    success_url = '/login/'


class LoginUser(LoginView, SuccessMessageMixin):
    model = User
    template_name = 'users/login.html'
    success_url = '/'
    form_class = AuthUserForm


class UpdateUser(UpdateView, SuccessMessageMixin):
    model = User
    template_name = 'users/update.html'
    form_class = UpdateUserForm
    success_url = '/'
