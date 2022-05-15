from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, AccessMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext, gettext_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from labels.forms import LabelForm
from labels.models import Label


class LabelsList(LoginRequiredMixin,
                 ListView,
                 AccessMixin):
    model = Label
    template_name = 'labels/list_labels.html'
    context_object_name = 'labels'
    error_message = gettext('У вас нет прав на просмотр данной страницы! '
                            'Авторизуйтесь!')
    no_permission_url = 'login'

    def handle_no_permission(self):
        messages.error(self.request, self.error_message)
        return redirect(self.no_permission_url)


class LabelCreate(SuccessMessageMixin, CreateView):
    model = Label
    template_name = 'labels/create_label.html'
    form_class = LabelForm
    success_message = gettext('Метка успешно создана')
    success_url = reverse_lazy('labels:list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = gettext('Создание метки')
        context['label'] = gettext('Имя')
        context['button_text'] = gettext('Создать метку')

        return context


class LabelUpdate(LoginRequiredMixin,
                  SuccessMessageMixin, AccessMixin, UpdateView):
    model = Label
    template_name = 'labels/update_label.html'
    form_class = LabelForm
    success_message = gettext('Метка успешно обновлена')
    success_url = reverse_lazy('labels:list')
    error_message = gettext_lazy('У вас нет разрешения на изменение метки')
    no_permission_url = 'statuses:list'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = gettext('Изменение метки')
        context['button_text'] = gettext('Изменить метку')
        return context

    def handle_no_permission(self):
        messages.error(self.request, self.error_message)
        return redirect(self.no_permission_url)


class LabelDelete(LoginRequiredMixin,
                  SuccessMessageMixin,
                  AccessMixin,
                  DeleteView
                  ):
    model = Label
    template_name = 'labels/delete_label.html'
    success_url = reverse_lazy('labels:list')

    def form_valid(self, form):
        if self.get_object().tasks.all():
            messages.error(self.request, gettext_lazy('Вы не можете удалить '
                                                      'статус, потому что он '
                                                      'используется'))
        else:
            super(LabelDelete, self).form_valid(form)
        return redirect(self.success_url)
