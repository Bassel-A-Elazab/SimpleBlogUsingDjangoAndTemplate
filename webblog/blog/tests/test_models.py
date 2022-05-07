from io import BytesIO
from PIL import Image

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.files.base import File
from django.test import TestCase
from django.utils.translation import gettext_lazy as _

from webblog.blog.models import Blog, BlogComment


class BlogModelTests(TestCase):

    @classmethod
    def setUpTestData(self):
        User = get_user_model()
        self.width = 4096
        self.height = 4096

        self.test_user1 = User.objects.create_user(
            email='test@user.com', name='test', password='test123')
        self.test_user1.save()
        self.blog = Blog.objects.create(
            title='Test Blog 1', author=self.test_user1, description='Test Blog 1 Description')
        self.blog.save()

    @staticmethod
    def get_image_file(name, ext, size=(500, 500), color=(256, 0, 0)):
        file_obj = BytesIO()
        image = Image.new("RGB", size=size, color=color)
        image.save(file_obj, ext)
        file_obj.seek(0)
        return File(file_obj, name=name)

    def test_object_title(self):
        expected_object_title = self.blog.title
        self.assertEqual(expected_object_title, str(self.blog))

    def test_title_label(self):
        expected_title_label = 'title'
        actual_title_label = self.blog._meta.get_field('title').verbose_name
        self.assertEqual(actual_title_label, expected_title_label)

    def test_author_label(self):
        expected_author_label = 'author'
        actual_author_label = self.blog._meta.get_field('author').verbose_name
        self.assertEqual(actual_author_label, expected_author_label)

    def test_description_label(self):
        expected_description_label = 'description'
        actual_description_label = self.blog._meta.get_field(
            'description').verbose_name
        self.assertEqual(actual_description_label, expected_description_label)

    def test_post_date_label(self):
        expected_post_date_label = 'posted date'
        actual_post_date_label = self.blog._meta.get_field(
            "post_date").verbose_name
        self.assertEqual(actual_post_date_label, expected_post_date_label)

    def test_title_max_length(self):
        max_length = self.blog._meta.get_field('title').max_length
        self.assertEqual(max_length, 200)

    def test_description_max_length(self):
        max_length = self.blog._meta.get_field('description').max_length
        self.assertEqual(max_length, 2000)

    def test_get_absolute_url(self):
        id = self.blog.id
        self.assertEqual(self.blog.get_absolute_url(), '/blogs/'+str(id))

    def test_cover_label(self):
        expected_cover_label = 'cover image'
        actual_cover_label = self.blog._meta.get_field('cover').verbose_name
        self.assertEqual(actual_cover_label, expected_cover_label)

    def test_uploaded_correct_cover_image_size(self):
        self.blog.cover = self.get_image_file(
            'image.jpg', "png", (1024, 1024))
        self.blog.save()
        image = Image.open(self.blog.cover.path)
        actual_image_width, actual_image_height = image.size
        self.assertLessEqual(actual_image_width, self.width)
        self.assertLessEqual(actual_image_height, self.height)

    def test_uploaded_wrong_cover_image_size(self):
        cover_image = self.get_image_file(
            'image.jpg', "png", (5096, 5096))
        self.blog.cover = cover_image

        with self.assertRaises(ValidationError):
            self.blog.save()


class BlogCommentModelTests(TestCase):

    @classmethod
    def setUpTestData(self):
        User = get_user_model()
        self.test_user1 = User.objects.create_user(
            email='test1@user.com', name='test1', password='test123')
        self.test_user1.save()
        self.test_user2 = User.objects.create_user(
            email="test2@user.com", name="test2", password="test123")
        self.test_user2.save()
        self.blog = Blog.objects.create(
            title='Test Blog 1', author=self.test_user1, description='Test Blog 1 Description')
        self.blog_comment = BlogComment.objects.create(
            comment="test comment 1", blog=self.blog, author=self.test_user2)
        self.blog_comment_with_small_length = BlogComment.objects.create(
            comment="test comment 1", blog=self.blog, author=self.test_user2)
        comment2 = "test comment 2 test comment 2 test comment 2 test comment 2 test comment 2 test comment 2 test comment 2 test comment 2 "
        self.blog_comment_with_high_length = BlogComment.objects.create(
            comment=comment2, blog=self.blog, author=self.test_user2)

    def test_object_name_with_small_length(self):
        expected_object_name = self.blog_comment_with_small_length.comment
        self.assertEqual(expected_object_name, str(
            self.blog_comment_with_small_length))

    def test_object_name_with_high_length(self):
        len_comment = 75
        expected_object_name = self.blog_comment_with_high_length.comment[:len_comment] + '...'
        self.assertEqual(expected_object_name, str(
            self.blog_comment_with_high_length))

    def test_comment_label(self):
        expected_comment_label = 'comment'
        actual_comment_label = self.blog_comment._meta.get_field(
            'comment').verbose_name
        self.assertEqual(expected_comment_label, actual_comment_label)

    def test_blog_label(self):
        expected_blog_label = 'blog'
        actual_blog_label = self.blog_comment._meta.get_field(
            'blog').verbose_name
        self.assertEqual(actual_blog_label, expected_blog_label)

    def test_author_label(self):
        expected_author_label = 'author'
        actual_author_label = self.blog_comment._meta.get_field(
            'author').verbose_name
        self.assertEqual(actual_author_label, expected_author_label)

    def test_comment_date_label(self):
        expected_comment_date_label = 'date'
        actual_comment_date_label = self.blog_comment._meta.get_field(
            'comment_date').verbose_name
        self.assertEqual(actual_comment_date_label,
                         expected_comment_date_label)

    def test_comment_max_length(self):
        max_length = self.blog_comment._meta.get_field('comment').max_length
        self.assertEqual(max_length, 1000)
