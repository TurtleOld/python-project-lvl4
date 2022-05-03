from django.test import TestCase, Client
from django.urls import reverse
from faker import Faker

from users.models import User


# Create your tests here.
class TestUser(TestCase):

    fixtures = ['users.yaml']

    def setUp(self) -> None:
        self.user1 = User.objects.get(pk=1)
        self.user2 = User.objects.get(pk=2)
        self.client: Client = Client()
        self.faker = Faker()

    def test_create_user(self):
        url = reverse('users:create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        # create new user
        Faker.seed(0)
        username = self.faker.user_name()
        first_name = self.faker.first_name()
        last_name = self.faker.last_name()
        set_password = self.faker.password(length=12)
        new_user = {
            'first_name': first_name,
            'last_name': last_name,
            'username': username,
            'password1': set_password,
            'password2': set_password,
        }

        response = self.client.post(url, new_user, follow=True)
        self.assertRedirects(response, '/login/')

    def test_update_user(self):
        user = self.user1
        self.client.force_login(user)
        url = reverse('users:update_user', args=(user.id, ))

        new_password = self.faker.password(length=12)

        change_user = {
            'first_name': user.first_name,
            'last_name': user.last_name,
            'username': user.username,
            'password1': new_password,
            'password2': new_password,
        }

        response = self.client.post(url, change_user, follow=True)

        self.assertRedirects(response, '/users/')
        changed_user = User.objects.get(username=user.username)
        self.assertTrue(changed_user.check_password(new_password))

    def test_delete_user(self):
        user = self.user2
        self.client.force_login(user)
        url = reverse('users:delete_user', args=(user.id,))

        response = self.client.post(url, follow=True)

        with self.assertRaises(User.DoesNotExist):
            User.objects.get(pk=user.id)

        self.assertRedirects(response, '/users/')
