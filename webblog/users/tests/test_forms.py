from datetime import date, timedelta

from django.test import TestCase
from django.utils.translation import gettext_lazy as _

from webblog.users.forms import BloggerUpdateForm, UserCreationFrom, UserSignUpForm


class UserCreationFromTest(TestCase):

    def setUp(self):
        self.user_email = "test@user.com"
        self.user_name = "test"
        self.user_password1 = "test"
        self.user_password2 = "test123"

    def test_clean_password2_creation_form_fail(self):
        form = UserCreationFrom(
            {
                "email": self.user_email,
                "name": self.user_name,
                "password1": self.user_password1,
                "password2": self.user_password2,
            }
        )

        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors["password2"][0], _("Password don't match!"))

    def test_clean_password2_creation_form_pass(self):
        form = UserCreationFrom(
            {
                "email": self.user_email,
                "name": self.user_name,
                "password1": self.user_password1,
                "password2": self.user_password1,
            }
        )
        self.assertTrue(form.is_valid())

    def test_save_custom_form_success(self):
        form = UserCreationFrom(
            {
                "email": self.user_email,
                "name": self.user_name,
                "password1": self.user_password1,
                "password2": self.user_password1,
            }
        )
        self.assertTrue(form.is_valid())
        user = form.save()
        self.assertEqual(user.email, self.user_email)
        self.assertEqual(user.name, self.user_name)


class UserSignUpFormTest(TestCase):

    def setUp(self):
        self.user_email = "test@user.com"
        self.user_name = "test"
        self.user_password1 = "test123"
        self.user_password2 = "test123"
        self.user_password2_wrong = "test"

        self.form_data_correct = {
            "email": self.user_email,
            "name": self.user_name,
            "password1": self.user_password1,
            "password2": self.user_password2,
        }
        self.form_data_wrong = {
            "email": self.user_email,
            "name": self.user_name,
            "password1": self.user_password1,
            "password2": self.user_password2_wrong,
        }

    def test_clean_password2_signup_fail(self):
        form = UserSignUpForm(self.form_data_wrong)

        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors["password2"][0], _("Password don't match!"))

    def test_clean_password2_signup_pass(self):
        form = UserSignUpForm(self.form_data_correct)
        self.assertTrue(form.is_valid())

    def test_signup_form_success(self):
        form = UserSignUpForm(self.form_data_correct)
        user = form.save()
        form.signup(request=None, user=user)
        self.assertTrue(form.is_valid())
        self.assertEqual(user.name, self.user_name)


class BloggerUpdateFormTest(TestCase):

    def setUp(self):
        self.user_name = "test"
        self.user_correct_date = ""
        self.user_birth_date_valid = date.today()
        self.user_birth_date_invalid = self.user_birth_date_valid + timedelta(days=1)
        self.form_data_correct = {
            "name": self.user_name,
            "date_of_birth": self.user_birth_date_valid,
        }
        self.form_data_wrong = {
            "name": self.user_name,
            "date_of_birth": self.user_birth_date_invalid,
        }

    def test_clean_birth_date_update_fail(self):
        form = BloggerUpdateForm(self.form_data_wrong)
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors["date_of_birth"][0], _("Invalid birth date range!")
        )

    def test_clean_birth_date_update_success(self):
        form = BloggerUpdateForm(self.form_data_correct)
        self.assertTrue(form.is_valid())
