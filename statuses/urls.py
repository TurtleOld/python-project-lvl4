from django.urls import path

from statuses.views import StatusList, StatusCreate

app_name = 'statuses'
urlpatterns = [
    path('', StatusList.as_view(), name='list'),
    path('create/', StatusCreate.as_view(), name='create'),
    # path('<int:pk>/update/', UpdateUser.as_view(), name='update_user'),
    # path('<int:pk>/delete/', DeleteUser.as_view(), name='delete_user'),
]
