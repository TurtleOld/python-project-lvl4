from django.urls import path

from labels.views import LabelsList, LabelCreate, LabelUpdate, LabelDelete

app_name = 'labels'
urlpatterns = [
    path('', LabelsList.as_view(), name='list'),
    path('create/', LabelCreate.as_view(), name='create'),
    path('<int:pk>/update/', LabelUpdate.as_view(), name='update_label'),
    path('<int:pk>/delete/', LabelDelete.as_view(), name='delete_label'),
]
