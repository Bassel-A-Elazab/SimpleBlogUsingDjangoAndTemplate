from django.test import TestCase
from django.contrib.auth import get_user_model


class MyUserModelsTests(TestCase):

    @classmethod
    def setUpTestData(self):
        User = get_user_model()
        self.test_user1 = User.objects.create_user(
            email='test@user.com', name='test', password='test123')

    def test_str_is_equal_to_email(self):
        self.assertEqual(str(self.test_user1), 'test@user.com')

    def test_get_desired_absolute_url(self):
        expected_url = '/bloggers/' + str(self.test_user1.pk)
        self.assertEqual(self.test_user1.get_absolute_url(), expected_url)

    def test_email_correct_label(self):
        expected_email_label = 'email address'
        self.assertEqual(self.test_user1._meta.get_field(
            'email').verbose_name, expected_email_label)

    def test_name_correct_label(self):
        expected_name_label = 'username'
        self.assertEqual(self.test_user1._meta.get_field(
            'name').verbose_name, expected_name_label)

    def test_bio_correct_label(self):
        expected_bio_label = 'bio'
        self.assertEqual(self.test_user1._meta.get_field(
            'bio').verbose_name, expected_bio_label)

    def test_date_of_birth_correct_label(self):
        expected_date_of_birth_label = 'birthdate'
        self.assertEqual(self.test_user1._meta.get_field(
            'date_of_birth').verbose_name, expected_date_of_birth_label)

    def test_picture_correct_labe(self):
        expected_picture_label = 'profile picture'
        self.assertEqual(self.test_user1._meta.get_field(
            'picture').verbose_name, expected_picture_label)
