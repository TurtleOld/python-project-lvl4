from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, AccessMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext, gettext_lazy
from django.views.generic import ListView, CreateView, UpdateView

from statuses.forms import StatusForm
from statuses.models import Status


class StatusList(LoginRequiredMixin, ListView, AccessMixin):
    model = Status
    template_name = 'statuses/list_statuses.html'
    context_object_name = 'statuses'
    error_message = gettext('У вас нет прав на просмотр данной страницы! '
                            'Авторизуйтесь!')
    no_permission_url = 'login'

    def handle_no_permission(self):
        messages.error(self.request, self.error_message)
        return redirect(self.no_permission_url)


class StatusCreate(SuccessMessageMixin, CreateView):
    model = Status
    template_name = 'statuses/create_status.html'
    form_class = StatusForm
    success_message = gettext_lazy('Статус успешно создан!')
    success_url = reverse_lazy('statuses:list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['button_text'] = gettext('Создать статус')
        context['label'] = gettext('Имя')
        return context


class UpdateStatus(SuccessMessageMixin, UpdateView):
    pass


class DeleteStatus(SuccessMessageMixin, UpdateView):
    pass
