from django.forms import ModelForm
from tasks.models import Task
from django.utils.translation import gettext


class TaskForm(ModelForm):
    class Meta:
        model = Task
        fields = ('name', 'description', 'status', 'executor')
        labels = {
            'name': gettext('Имя'),
            'description': gettext('Описание'),
            'status': gettext('Статус'),
            'executor': gettext('Исполнитель'),
        }
