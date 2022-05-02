from django.test import TestCase
from django.urls import reverse

from users.models import User


# Create your tests here.
class TestUser(TestCase):

    fixtures = ['users.yaml']

    def setUp(self) -> None:
        self.user1 = User.objects.get(pk=1)
        self.user2 = User.objects.get(pk=2)

    def test_create_user(self):
        url = reverse('users:create')
        print(url)
        new_user = {
            'username': 'alexander',
            'first_name': 'Alexander',
            'last_name': 'Pavlov',
            'password1': '123',
            'password2': '123',
        }
        response = self.client.post(url, new_user, follow=True)
        print(response.status_code)
        self.assertRedirects(response, '/login/')
