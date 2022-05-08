from django.urls import path

from statuses.views import StatusList, StatusCreate, UpdateStatus, DeleteStatus

app_name = 'statuses'
urlpatterns = [
    path('', StatusList.as_view(), name='list'),
    path('create/', StatusCreate.as_view(), name='create'),
    path('<int:pk>/update/', UpdateStatus.as_view(), name='update_status'),
    path('<int:pk>/delete/', DeleteStatus.as_view(), name='delete_status'),
]
