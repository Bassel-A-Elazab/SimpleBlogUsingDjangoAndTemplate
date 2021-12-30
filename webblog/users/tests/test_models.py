from django.test import TestCase
from django.core import mail

from webblog.users.models import MyUser


class MyUserModelsTests(TestCase):

    def test_str_is_equal_to_email(self):
        my_user = MyUser.objects.create(
            email='test@user.com', name='test', password='test123')
        self.assertEqual(str(my_user), 'test@user.com')

    def test_send_email(self):
        my_user = MyUser.objects.create(
            email='test@user.com', name='test', password='test123')
        subject = 'Test Subject'
        body = 'Test Body'

        my_user.email_user(subject, body, my_user.email)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, 'Test Subject')
        self.assertEqual(mail.outbox[0].body, 'Test Body')
        self.assertEqual(mail.outbox[0].to, [my_user.email])
