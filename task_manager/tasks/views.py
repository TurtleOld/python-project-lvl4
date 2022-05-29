from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, AccessMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext, gettext_lazy
from django.views.generic import CreateView, UpdateView, DeleteView, \
    DetailView
from django_filters.views import FilterView

from task_manager.tasks.forms import TaskForm, TasksFilter
from task_manager.tasks.models import Task
from task_manager.users.models import User
from task_manager.mixins import HandleNoPermissionMixin


class TasksList(LoginRequiredMixin,
                HandleNoPermissionMixin,
                SuccessMessageMixin,
                FilterView):
    model = Task
    template_name = 'tasks/list_tasks.html'
    context_object_name = 'tasks'
    filterset_class = TasksFilter
    error_message = gettext_lazy('У вас нет прав на просмотр данной страницы! '
                                 'Авторизуйтесь!')
    no_permission_url = reverse_lazy('login')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(TasksList, self).get_context_data(**kwargs)
        context['button_filter_text'] = 'Показать'
        return context


class CreateTask(SuccessMessageMixin, HandleNoPermissionMixin, CreateView):
    model = Task
    template_name = 'tasks/create_task.html'
    form_class = TaskForm
    success_message = gettext_lazy('Задача успешно создана')
    success_url = reverse_lazy('tasks:list')
    error_message = gettext_lazy('У вас нет прав на просмотр данной страницы! '
                                 'Авторизуйтесь!')
    no_permission_url = reverse_lazy('login')

    def form_valid(self, form):
        form.instance.author = User.objects.get(pk=self.request.user.pk)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(CreateTask, self).get_context_data(**kwargs)
        context['title'] = gettext('Создание задачи')
        context['button_text'] = gettext('Создать')
        return context


class UpdateTask(SuccessMessageMixin, HandleNoPermissionMixin, UpdateView):
    model = Task
    template_name = 'tasks/update_task.html'
    form_class = TaskForm
    success_message = gettext_lazy('Задача успешно изменена')
    success_url = reverse_lazy('tasks:list')
    error_message = gettext_lazy('У вас нет прав на просмотр данной страницы! '
                                 'Авторизуйтесь!')
    no_permission_url = reverse_lazy('login')

    def get_context_data(self, **kwargs):
        context = super(UpdateTask, self).get_context_data(**kwargs)
        context['title'] = gettext_lazy('Обновление задачи')
        context['button_text'] = gettext_lazy('Изменить')
        return context


class DeleteTask(LoginRequiredMixin,
                 SuccessMessageMixin, HandleNoPermissionMixin,
                 DeleteView):
    model = Task
    template_name = 'tasks/delete_task.html'
    success_url = reverse_lazy('tasks:list')
    success_message = gettext_lazy('Задача успешно удалена')
    error_message = gettext_lazy('У вас нет прав на просмотр данной страницы! '
                                 'Авторизуйтесь!')
    no_permission_url = reverse_lazy('login')

    def get_context_data(self, **kwargs):
        context = super(DeleteTask, self).get_context_data(**kwargs)
        context['title'] = gettext_lazy('Удаление задачи')
        return context

    def form_valid(self, form):
        if self.request.user != self.get_object().author:
            messages.error(self.request, gettext_lazy('Вы не можете удалить '
                                                      'чужую задачу!'))
        else:
            super(DeleteTask, self).form_valid(form)
        return redirect(self.success_url)


class TaskView(LoginRequiredMixin,
               SuccessMessageMixin, HandleNoPermissionMixin,
               DetailView):
    model = Task
    template_name = 'tasks/view_task.html'
    context_object_name = 'task'
    error_message = gettext('У вас нет прав на просмотр данной страницы! '
                            'Авторизуйтесь!')
    no_permission_url = reverse_lazy('login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['labels'] = self.get_object().labels.all()
        return context
