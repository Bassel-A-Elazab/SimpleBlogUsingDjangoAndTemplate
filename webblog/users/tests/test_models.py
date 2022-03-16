from django.test import TestCase
from django.urls import reverse

from webblog.users.models import MyUser


class MyUserModelsTests(TestCase):

    @classmethod
    def testSetUpDataTest(self):
        self.test_user1 = MyUser.objects.create_user(
            email='test@user.com', name='test', password='test123')

    def test_str_is_equal_to_email(self):
        self.assertEqual(str(self.test_user1), 'test@user.com')

    def test_get_desired_absolute_url(self):
        expected_url = '/bloggers/' + str(self.test_user1.pk)
        self.assertEqual(self.test_user1.get_absolute_url(), expected_url)
