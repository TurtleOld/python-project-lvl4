from django.contrib.auth.mixins import LoginRequiredMixin, \
    UserPassesTestMixin, AccessMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.utils.translation import gettext, gettext_lazy
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, \
    FormView
from users.models import User
from users.forms import RegisterUserForm, AuthUserForm


# Create your views here.
class UsersList(ListView):
    model = User
    template_name = 'users/users.html'
    context_object_name = 'users'


class CreateUser(SuccessMessageMixin, CreateView):
    model = User
    template_name = 'users/register.html'
    form_class = RegisterUserForm
    success_url = reverse_lazy('login')
    success_message = gettext_lazy('Пользователь успешно зарегистрирован')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['button_text'] = gettext('Зарегистрировать')
        return context


class LoginUser(SuccessMessageMixin, LoginView):
    model = User
    template_name = 'users/login.html'
    form_class = AuthUserForm
    success_message = gettext_lazy('Вы залогинены')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['button_text'] = gettext('Войти')
        return context


class LogoutUser(LogoutView, SuccessMessageMixin):

    def dispatch(self, request, *args, **kwargs):
        messages.add_message(request, messages.SUCCESS,
                             gettext('Вы разлогинены'))
        return super().dispatch(request, *args, **kwargs)


class UpdateUser(LoginRequiredMixin,
                 SuccessMessageMixin,
                 UserPassesTestMixin,
                 AccessMixin,
                 UpdateView,
                 FormView, ):
    model = User
    template_name = 'users/update.html'
    form_class = RegisterUserForm
    success_url = reverse_lazy('users:list')
    success_message = gettext_lazy('Пользователь успешно изменён')
    error_message = gettext_lazy('У вас нет разрешения на изменение другого '
                                 'пользователя')
    no_permission_url = 'users:list'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['button_text'] = gettext('Изменить')
        return context

    def test_func(self):
        return self.request.user == self.get_object()

    def handle_no_permission(self):
        messages.error(self.request, self.error_message)
        return redirect(self.no_permission_url)


class DeleteUser(LoginRequiredMixin,
                 SuccessMessageMixin,
                 UserPassesTestMixin,
                 AccessMixin,
                 DeleteView,
                 FormView, ):
    model = User
    template_name = 'users/delete.html'
    success_url = reverse_lazy('users:list')
    success_message = gettext_lazy('Пользователь успешно удалён')
    error_message = gettext_lazy('У вас нет разрешения на изменение другого '
                                 'пользователя')
    no_permission_url = 'users:list'

    def test_func(self):
        return self.request.user == self.get_object()

    def handle_no_permission(self):
        messages.error(self.request, self.error_message)
        return redirect(self.no_permission_url)
