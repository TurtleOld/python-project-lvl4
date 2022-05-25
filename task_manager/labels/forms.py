from django.forms import ModelForm
from task_manager.labels.models import Label
from django.utils.translation import gettext


class LabelForm(ModelForm):
    class Meta:
        model = Label
        fields = ('name', )
        labels = {
            'name': gettext('Имя')
        }
