
from django.test import TestCase
from django.utils.translation import gettext_lazy as _


from webblog.users.models import MyUser
from webblog.users.forms import UserCreationFrom, UserSignUpForm


class MyUserFormTests(TestCase):

    def test_clean_password2(self):
        form = UserCreationFrom(
            {
                'email': 'test@user.com',
                'name': 'test',
                'password1': 'test',
                'password2': 'test123',
            }
        )

        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['password2']
                         [0], _("Password don't match!"))

    def test_custom_from(self):
        form = UserCreationFrom(
            {
                'email': 'test@user.com',
                'name': 'test',
                'password1': 'test',
                'password2': 'test',
            }
        )
        self.assertTrue(form.is_valid())
        if form.is_valid():
            form.save(commit=False)
            if form.save(commit=True):
                user = form.save(commit=False)
                user.save()

    def test_clean_password2_with_signup(self):
        form = UserSignUpForm(
            {
                'email': 'test@user.com',
                'name': 'test',
                'password1': 'test',
                'password2': 'test123',
            }
        )

        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['password2']
                         [0], _("Password don't match!"))

    def test_custom_from_with_signup(self):
        form = UserSignUpForm(
            {
                'email': 'test@user.com',
                'name': 'test',
                'password1': 'test',
                'password2': 'test',
            }
        )
        self.assertTrue(form.is_valid())
        if form.is_valid():
            form.save(commit=False)
            if form.save(commit=True):
                user = form.save(commit=False)
                user.save()
