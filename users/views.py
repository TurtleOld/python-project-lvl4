from django.shortcuts import render
from django.views.generic.list import ListView
from users.models import Users


# Create your views here.
class UsersView(ListView):
    model = Users
    template_name = 'users/users.html'
    context_object_name = 'users'
