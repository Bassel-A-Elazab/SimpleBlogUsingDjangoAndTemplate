from django.test import TestCase
from django.contrib.auth import get_user_model


class MyUsersManagersTests(TestCase):

    def test_create_user(self):
        User = get_user_model()
        user = User.objects.create_user(
            email='normal@user.com', name='normal', password='normal')
        self.assertEqual(user.email, 'normal@user.com')
        self.assertEqual(user.name, 'normal')
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        try:
            self.assertIsNone(user.username)
        except AttributeError:
            pass
        with self.assertRaises(TypeError):
            User.objects.create_user()
        with self.assertRaises(TypeError):
            User.objects.create_user()
        with self.assertRaises(ValueError):
            User.objects.create_user(
                email='normal@user.com', name='', password='normal')
        with self.assertRaises(ValueError):
            User.objects.create_user(
                email='', name='normal', password='normal')

    def test_create_superuser(self):
        User = get_user_model()
        admin_user = User.objects.create_superuser(
            email='super@user.com', name='super', password='super')
        self.assertEqual(admin_user.email, 'super@user.com')
        self.assertEqual(admin_user.name, 'super')
        self.assertTrue(admin_user.is_active)
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)
        try:
            self.assertIsNone(admin_user.username)
        except AttributeError:
            pass
        with self.assertRaises(ValueError):
            User.objects.create_superuser(
                email='super@user.com', name='super', password='super', is_superuser=False)
        with self.assertRaises(ValueError):
            User.objects.create_superuser(
                email='super@user.com', name='super', password='super', is_staff=False)
