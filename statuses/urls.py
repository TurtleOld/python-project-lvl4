from django.urls import path

from statuses.views import StatusList, StatusCreate, StatusUpdate, StatusDelete

app_name = 'statuses'
urlpatterns = [
    path('', StatusList.as_view(), name='list'),
    path('create/', StatusCreate.as_view(), name='create'),
    path('<int:pk>/update/', StatusUpdate.as_view(), name='update_status'),
    path('<int:pk>/delete/', StatusDelete.as_view(), name='delete_status'),
]
