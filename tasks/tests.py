from django.test import TestCase
from django.urls import reverse_lazy, reverse

from statuses.models import Status
from tasks.models import Task
from users.models import User


class TestTask(TestCase):
    fixtures = ['users.yaml', 'statuses.yaml', 'tasks.yaml']

    def setUp(self) -> None:
        self.user1 = User.objects.get(pk=1)
        self.user2 = User.objects.get(pk=2)
        self.status1 = Status.objects.get(pk=1)
        self.status2 = Status.objects.get(pk=2)
        self.task1 = Task.objects.get(pk=1)
        self.task2 = Task.objects.get(pk=2)

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
            'status': 1
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
            'status': 2
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
        self.task1.delete()
        url = reverse('tasks:delete_task', args=(self.task2.pk,))
        response = self.client.post(url, follow=True)
        self.assertRedirects(response, '/tasks/')
        with self.assertRaises(Task.DoesNotExist):
            Task.objects.get(pk=self.task1.pk)

    def test_delete_task_not_author(self):
        self.client.force_login(self.user1)
        url = reverse('tasks:delete_task', args=(self.task1.pk,))
        response = self.client.post(url, follow=True)
        self.assertTrue(Task.objects.filter(pk=self.task1.id).exists())
        self.assertRedirects(response, '/tasks/')
