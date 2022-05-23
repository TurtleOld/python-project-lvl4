from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, AccessMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext, gettext_lazy
from django.views.generic import ListView, CreateView, UpdateView, FormView, \
    DeleteView

from statuses.forms import StatusForm
from statuses.models import Status


class StatusesList(LoginRequiredMixin, ListView, AccessMixin):
    model = Status
    template_name = 'statuses/list_statuses.html'
    context_object_name = 'statuses'
    error_message = gettext('У вас нет прав на просмотр данной страницы! '
                            'Авторизуйтесь!')
    no_permission_url = 'login'

    def handle_no_permission(self):
        messages.error(self.request, self.error_message)
        return redirect(self.no_permission_url)


class CreateStatus(SuccessMessageMixin, CreateView):
    model = Status
    template_name = 'statuses/create_status.html'
    form_class = StatusForm
    success_message = gettext_lazy('Статус успешно создан')
    success_url = reverse_lazy('statuses:list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = gettext('Создание статуса')
        context['button_text'] = gettext('Создать')
        context['label'] = gettext('Имя')
        return context


class UpdateStatus(LoginRequiredMixin,
                   SuccessMessageMixin,
                   AccessMixin,
                   UpdateView,
                   FormView, ):
    model = Status
    template_name = 'statuses/update_status.html'
    form_class = StatusForm
    success_url = reverse_lazy('statuses:list')
    success_message = gettext_lazy('Статус успешно изменён')
    error_message = gettext_lazy('У вас нет разрешения на изменение статуса')
    no_permission_url = 'statuses:list'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = gettext('Изменение статуса')
        context['button_text'] = gettext('Изменить')
        return context

    def handle_no_permission(self):
        messages.error(self.request, self.error_message)
        return redirect(self.no_permission_url)


class DeleteStatus(LoginRequiredMixin,
                   SuccessMessageMixin,
                   AccessMixin,
                   DeleteView,
                   FormView, ):
    model = Status
    template_name = 'statuses/delete_status.html'
    success_url = reverse_lazy('statuses:list')

    def form_valid(self, form):
        if self.get_object().tasks.all():
            messages.error(self.request, gettext_lazy('Вы не можете удалить '
                                                      'статус, потому что он '
                                                      'используется'))
        else:
            super(DeleteStatus, self).form_valid(form)
        return redirect(self.success_url)
