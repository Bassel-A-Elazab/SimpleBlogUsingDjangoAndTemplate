from io import BytesIO
from PIL import Image

from django.core.files.base import File
from django.test import TestCase
from django.contrib.auth import get_user_model


class MyUserModelsTests(TestCase):

    @classmethod
    def setUpTestData(self):
        User = get_user_model()
        self.test_user1 = User.objects.create_user(
            email='test@user.com', name='test', password='test123')
        self.test_user2 = User.objects.create_user(
            email='test2@user.com', name='test2', password='test123')
        self.image_width = 300
        self.image_height = 300

    @staticmethod
    def get_image_file(name, ext, size=(500, 500), color=(256, 0, 0)):
        file_obj = BytesIO()
        image = Image.new("RGB", size=size, color=color)
        image.save(file_obj, ext)
        file_obj.seek(0)
        return File(file_obj, name=name)

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

    def test_picture_save_with_correct_size(self):
        self.test_user1.picture = self.get_image_file(
            'image.jpg', "png", (300, 300))
        self.test_user1.save()
        image = Image.open(self.test_user1.picture.path)
        actual_image_width, actual_image_height = image.size
        self.assertLessEqual(actual_image_width, self.image_width)
        self.assertLessEqual(actual_image_height, self.image_height)

    def test_picture_save_with_wrong_size(self):
        self.test_user1.picture = self.get_image_file(
            'image.jpg', "png", (500, 500))
        self.test_user1.save()
        image = Image.open(self.test_user1.picture.path)
        actual_image_width, actual_image_height = image.size
        self.assertLessEqual(actual_image_width, self.image_width)
        self.assertLessEqual(actual_image_height, self.image_height)
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
