from django.contrib.auth import get_user_model
from django.test import TestCase


class MyUsersManagersTests(TestCase):

    def setUp(self):
        self.user = get_user_model()
        self.user_email = "test@user.com"
        self.user_name = "test"
        self.user_password = "test123"

    def test_create_user(self):
        test_user = self.user.objects.create_user(
            email=self.user_email, name=self.user_name, password=self.user_password
        )
        self.assertEqual(test_user.email, self.user_email)
        self.assertEqual(test_user.name, self.user_name)
        self.assertFalse(test_user.is_active)
        self.assertFalse(test_user.is_staff)
        self.assertFalse(test_user.is_superuser)
        try:
            self.assertIsNone(test_user.username)
        except AttributeError:
            pass
        with self.assertRaises(TypeError):
            self.user.objects.create_user()
        with self.assertRaises(TypeError):
            self.user.objects.create_user()
        with self.assertRaises(ValueError):
            self.user.objects.create_user(
                email=self.user_email, name="", password=self.user_password
            )
        with self.assertRaises(ValueError):
            self.user.objects.create_user(
                email="", name=self.user_email, password=self.user_password
            )

    def test_create_superuser(self):
        admin_user = self.user.objects.create_superuser(
            email=self.user_email, name=self.user_name, password=self.user_password
        )
        self.assertEqual(admin_user.email, self.user_email)
        self.assertEqual(admin_user.name, self.user_name)
        self.assertTrue(admin_user.is_active)
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)
        try:
            self.assertIsNone(admin_user.username)
        except AttributeError:
            pass
        with self.assertRaises(ValueError):
            self.user.objects.create_superuser(
                email=self.user_email,
                name=self.user_name,
                password=self.user_password,
                is_superuser=False,
            )
        with self.assertRaises(ValueError):
            self.user.objects.create_superuser(
                email=self.user_email,
                name=self.user_name,
                password=self.user_password,
                is_staff=False,
            )
