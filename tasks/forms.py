from django import forms
from django.db.models import Value
from django.db.models.functions import Concat
from django.forms import ModelForm
import django_filters

from labels.models import Label
from statuses.models import Status
from tasks.models import Task
from django.utils.translation import gettext_lazy

from users.models import User


class TaskForm(ModelForm):
    class Meta:
        model = Task
        fields = ('name', 'description', 'status', 'executor', 'labels')
        labels = {
            'name': gettext_lazy('Имя'),
            'description': gettext_lazy('Описание'),
            'status': gettext_lazy('Статус'),
            'executor': gettext_lazy('Исполнитель'),
            'labels': gettext_lazy('Метки')
        }


class TasksFilter(django_filters.FilterSet):
    statuses = Status.objects.values_list('id', 'name', named=True).all()
    status = django_filters.ChoiceFilter(label=gettext_lazy('Статус'),
                                         choices=statuses)

    executors = User.objects.values_list('id', Concat('first_name',
                                                      Value(' '),
                                                      'last_name'),
                                         named=True).all()
    executor = django_filters.ChoiceFilter(label=gettext_lazy('Исполнитель'),
                                           choices=executors)

    all_labels = Label.objects.values_list('id', 'name', named=True)
    labels = django_filters.ChoiceFilter(label=gettext_lazy('Метка'),
                                         choices=all_labels)

    self_task = django_filters.BooleanFilter(
        label=gettext_lazy('Только свои задачи'),
        widget=forms.CheckboxInput(),
        method='filter_current_user',
        field_name='self_task'
    )

    def filter_current_user(self, queryset, name, value):
        if value:
            author = getattr(self.request, 'user', None)
            queryset = queryset.filter(author=author)
        return queryset

    class Meta:
        model = Task
        fields = ['status', 'executor', 'labels']
