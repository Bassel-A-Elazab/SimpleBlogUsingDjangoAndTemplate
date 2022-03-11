from django.test import TestCase
from django.contrib.auth import get_user_model


class MyUserModelsTests(TestCase):

    @classmethod
    def setUpTestData(self):
        self.test_user1 = get_user_model().objects.create_user(
            email='test@user.com', name='test', password='test123')

    def test_email_label(self):
        email_label = self.test_user1._meta.get_field('email').verbose_name
        self.assertEqual(email_label, 'email address')

    def test_name_max_length(self):
        max_length = self.test_user1._meta.get_field('name').max_length
        self.assertEqual(max_length, 150)

    def test_str_is_equal_to_email(self):
        self.assertEqual(str(self.test_user1), 'test@user.com')