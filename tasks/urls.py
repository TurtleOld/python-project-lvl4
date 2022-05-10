from django.urls import path

from tasks.views import TasksList, TaskCreate, TaskUpdate, TaskDelete, TaskView

app_name = 'tasks'
urlpatterns = [
    path('', TasksList.as_view(), name='list'),
    path('create/', TaskCreate.as_view(), name='create'),
    path('<int:pk>/update/', TaskUpdate.as_view(), name='update_task'),
    path('<int:pk>/delete/', TaskDelete.as_view(), name='delete_task'),
    path('<int:pk>/', TaskView.as_view(), name='view_task'),
]
