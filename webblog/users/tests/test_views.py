from django.contrib.auth import tokens
from django.http import response
from django.test import TestCase
from django.utils.encoding import force_str
from django.urls import reverse_lazy
from webblog.users.models import MyUser
from webblog.users.tokens import account_activation_token
from django.urls import reverse
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str


class MyUserViewsTests(TestCase):

    def test_sign_up(self):
        data = {
            'email': 'test@user.com',
            'name': 'test',
            'password1': 'test123',
            'password2': 'test123'
        }
        response = self.client.post(
            reverse('users:signup'), data=data, follow=True)
        self.assertEqual(response.status_code, 200)

    def test_activate_email_success(self):
        my_user = MyUser.objects.create(
            email='test@user.com', name='test', password='test')
        token = account_activation_token.make_token(my_user)
        user_id = urlsafe_base64_encode(force_bytes(my_user.pk))
        activation_url = reverse('users:activate', kwargs={
            'uid': user_id, 'token': token})
        activation_url = 'http://127.0.0.1:8000' + activation_url
        response = self.client.get(activation_url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, '/')
