from django.test import TestCase
from django.utils.translation import gettext_lazy as _

from webblog.users.forms import UserCreationFrom, UserSignUpForm


class UserCreationFromTest(TestCase):
    def test_clean_password2_creation_form_fail(self):
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

    def test_clean_password2_creation_form_pass(self):
        form = UserCreationFrom(
            {
                'email': 'test@user.com',
                'name': 'test',
                'password1': 'test123',
                'password2': 'test123',
            }
        )
        self.assertTrue(form.is_valid())

    def test_save_custom_form_success(self):
        form = UserCreationFrom(
            {
                'email': 'test@user.com',
                'name': 'test',
                'password1': 'test123',
                'password2': 'test123',
            }
        )
        self.assertTrue(form.is_valid())
        user = form.save()
        self.assertEqual(user.email, 'test@user.com')
        self.assertEqual(user.name, 'test')


class UserSignUpFormTest(TestCase):
    @classmethod
    def setUpTestData(self):
        email = 'test@user.com'
        name = 'test'
        password1 = 'test123'
        password2 = 'test123'
        password2_wrong = 'test'
        self.form_data_correct = {
            'email': email,
            'name': name,
            'password1': password1,
            'password2': password2,
        }

        self.form_data_wrong = {
            'email': email,
            'name': name,
            'password1': password1,
            'password2': password2_wrong,
        }

    def test_clean_password2_signup_fail(self):
        form = UserSignUpForm(self.form_data_wrong)

        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['password2']
                         [0], _("Password don't match!"))

    def test_clean_password2_signup_pass(self):
        form = UserSignUpForm(self.form_data_correct)
        self.assertTrue(form.is_valid())
