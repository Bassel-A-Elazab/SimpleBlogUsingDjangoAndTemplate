from django.test import TestCase

from webblog.users.models import MyUser


class MyUserModelsTests(TestCase):

    def test_str_is_equal_to_email(self):
        my_user = MyUser.objects.create(
            email='test@user.com', name='test', password='test')
        self.assertEqual(str(my_user), 'test@user.com')
