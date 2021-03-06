from django.urls import path
from task_manager.users.views import CreateUser, UsersList, UpdateUser, \
    DeleteUser


app_name = 'users'
urlpatterns = [
    path('', UsersList.as_view(), name='list'),
    path('create/', CreateUser.as_view(), name='create'),
    path('<int:pk>/update/', UpdateUser.as_view(), name='update_user'),
    path('<int:pk>/delete/', DeleteUser.as_view(), name='delete_user'),
]
