from django.forms import ModelForm
from task_manager.statuses.models import Status
from django.utils.translation import gettext


class StatusForm(ModelForm):
    class Meta:
        model = Status
        fields = ('name', )
        labels = {
            'name': gettext('Имя')
        }
