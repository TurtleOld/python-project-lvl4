from django.urls import path

from statuses.views import StatusList, StatusCreate, UpdateStatus, DeleteStatus

app_name = 'labels'
urlpatterns = [
    path('', LabelsList.as_view(), name='list'),
    path('create/', LabelCreate.as_view(), name='create'),
    path('<int:pk>/update/', UpdateLabel.as_view(), name='update_label'),
    path('<int:pk>/delete/', DeleteLabel.as_view(), name='delete_label'),
]
