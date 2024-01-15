from io import BytesIO
from PIL import Image

from django.core.files.base import File
from django.contrib.auth import get_user_model
from django.test import TestCase

from webblog.users.models import user_signed_up_


class MyUserModelsTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model()
        cls.user_email = 'test@user.com'
        cls.user_name = 'test'
        cls.user_password = 'test123'
        cls.image_width = 300
        cls.image_height = 300

        cls.test_user = cls.user.objects.create_user(
            email=cls.user_email, name=cls.user_name, password=cls.user_password)

    @staticmethod
    def get_image_file(name, ext, size=(500, 500), color=(256, 0, 0)):
        file_obj = BytesIO()
        image = Image.new("RGB", size=size, color=color)
        image.save(file_obj, ext)
        file_obj.seek(0)
        return File(file_obj, name=name)

    def test_str_is_equal_to_email(self):
        self.assertEqual(str(self.test_user), self.user_email)

    def test_get_desired_absolute_url(self):
        expected_url = '/bloggers/' + str(self.test_user.pk)
        self.assertEqual(self.test_user.get_absolute_url(), expected_url)

    def test_email_correct_label(self):
        expected_email_label = 'email address'
        self.assertEqual(self.test_user._meta.get_field(
            'email').verbose_name, expected_email_label)

    def test_name_correct_label(self):
        expected_name_label = 'username'
        self.assertEqual(self.test_user._meta.get_field(
            'name').verbose_name, expected_name_label)

    def test_bio_correct_label(self):
        expected_bio_label = 'bio'
        self.assertEqual(self.test_user._meta.get_field(
            'bio').verbose_name, expected_bio_label)

    def test_date_of_birth_correct_label(self):
        expected_date_of_birth_label = 'birthdate'
        self.assertEqual(self.test_user._meta.get_field(
            'date_of_birth').verbose_name, expected_date_of_birth_label)

    def test_picture_correct_labe(self):
        expected_picture_label = 'profile picture'
        self.assertEqual(self.test_user._meta.get_field(
            'picture').verbose_name, expected_picture_label)

    def test_picture_save_with_correct_size(self):
        self.test_user.picture = self.get_image_file(
            'image.jpg', "png", (self.image_width, self.image_height))
        self.test_user.save()
        image = Image.open(self.test_user.picture.path)
        actual_image_width, actual_image_height = image.size
        self.assertLessEqual(actual_image_width, self.image_width)
        self.assertLessEqual(actual_image_height, self.image_height)

    def test_picture_save_with_wrong_size(self):
        self.test_user.picture = self.get_image_file(
            'image.jpg', "png", (500, 500))
        self.test_user.save()
        image = Image.open(self.test_user.picture.path)
        actual_image_width, actual_image_height = image.size
        self.assertLessEqual(actual_image_width, self.image_width)
        self.assertLessEqual(actual_image_height, self.image_height)

    def test_email_label(self):
        email_label = self.test_user._meta.get_field('email').verbose_name
        self.assertEqual(email_label, 'email address')

    def test_name_max_length(self):
        max_length = self.test_user._meta.get_field('name').max_length
        self.assertEqual(max_length, 150)

    def test_str_is_equal_to_email(self):
        self.assertEqual(str(self.test_user), self.user_email)

    def test_receiver_signed_up_signal(self):
        user_signed_up_(sender=None, request=None, user=self.test_user)
        self.assertTrue(self.test_user.is_active)
        
        