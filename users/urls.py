from django.urls import path
from users.views import CreateUser, UsersList


app_name = 'users'
urlpatterns = [
    path('', UsersList.as_view(), name='list'),
    path('create/', CreateUser.as_view(), name='create'),
]
