from django.test import TestCase
from django.urls import reverse_lazy, reverse
from django_filters import FilterSet, BooleanFilter

from labels.models import Label
from statuses.models import Status
from tasks.forms import TasksFilter
from tasks.models import Task
from users.models import User


class TestTask(TestCase):
    fixtures = ['users.yaml', 'statuses.yaml', 'tasks.yaml', 'labels.yaml']

    def setUp(self) -> None:
        self.user1 = User.objects.get(pk=1)
        self.user2 = User.objects.get(pk=2)
        self.status1 = Status.objects.get(pk=1)
        self.status2 = Status.objects.get(pk=2)
        self.task1 = Task.objects.get(pk=1)
        self.task2 = Task.objects.get(pk=2)
        self.label1 = Label.objects.get(pk=1)
        self.label2 = Label.objects.get(pk=2)

    def test_list_tasks(self):
        self.client.force_login(self.user1)
        response = self.client.get(reverse_lazy('tasks:list'))
        self.assertEqual(response.status_code, 200)
        tasks_list = list(response.context['tasks'])
        self.assertQuerysetEqual(tasks_list, [self.task1, self.task2])

    def test_create_tasks(self):
        self.client.force_login(self.user1)
        new_task = {
            'name': 'Новая задача',
            'description': 'description',
            'author': 1,
            'executor': 2,
            'status': 1,
            'labels': [1, 2]
        }
        response = self.client.post(
            reverse_lazy('tasks:create'),
            new_task,
            follow=True
        )

        self.assertRedirects(response, '/tasks/')
        created_task = Task.objects.get(name=new_task['name'])
        self.assertEqual(created_task.name, 'Новая задача')

    def test_update_task(self):
        self.client.force_login(self.user1)
        url = reverse('tasks:update_task', args=(self.task1.pk,))
        changed_task = {
            'name': 'New task',
            'description': 'description',
            'author': 2,
            'executor': 1,
            'status': 2,
            'labels': [1, 2]
        }

        response = self.client.post(
            url,
            changed_task,
            follow=True
        )
        self.assertRedirects(response, '/tasks/')
        created_task = Task.objects.get(name=changed_task['name'])
        self.assertEqual(created_task.name, 'New task')

    def test_delete_task(self):
        self.client.force_login(self.user1)
        url = reverse_lazy('tasks:delete_task', args=(self.task1.id,))
        response = self.client.post(url, follow=True)
        with self.assertRaises(Task.DoesNotExist):
            Task.objects.get(pk=self.task1.id)
        self.assertRedirects(response, '/tasks/')

    def test_delete_task_not_author(self):
        self.client.force_login(self.user1)
        url = reverse_lazy('tasks:delete_task', args=(self.task2.pk,))
        response = self.client.post(url, follow=True)
        self.assertTrue(Task.objects.filter(pk=self.task2.pk).exists())
        self.assertRedirects(response, '/tasks/')

    def test_filter_status(self):
        status = Task._meta.get_field('status')
        result = FilterSet.filter_for_field(status, 'status')
        self.assertEqual(result.field_name, 'status')

    def test_filter_executor(self):
        status = Task._meta.get_field('executor')
        result = FilterSet.filter_for_field(status, 'executor')
        self.assertEqual(result.field_name, 'executor')

    def test_filter_label(self):
        status = Task._meta.get_field('labels')
        result = FilterSet.filter_for_field(status, 'labels')
        self.assertEqual(result.field_name, 'labels')
