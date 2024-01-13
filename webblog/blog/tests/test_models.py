from io import BytesIO
from PIL import Image

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.files.base import File
from django.test import TestCase
from django.utils.translation import gettext_lazy as _

from webblog.blog.models import Blog, BlogComment, BlogTag


class BlogModelTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        user = get_user_model()
        cls.user_email = 'test@user.com'
        cls.user_name = 'test'
        cls.user_password = 'test123'
        cls.blog_title = 'Test Blog'
        cls.blog_description = 'Test Blog Description'
        cls.width = 4096
        cls.height = 4096

        cls.test_user = user.objects.create_user(
            email=cls.user_email, name=cls.user_name, password=cls.user_password)
        cls.test_user.save()
        cls.blog = Blog.objects.create(
            title=cls.blog_title, author=cls.test_user, description=cls.blog_description)
        cls.blog.save()

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
        blog_id = self.blog.id
        self.assertEqual(self.blog.get_absolute_url(), '/blogs/'+str(blog_id))

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
    def setUpTestData(cls):
        user = get_user_model()
        cls.user_email = 'test@user.com'
        cls.user_name = 'test'
        cls.user_password = 'test123'
        cls.blog_title = 'Test Blog'
        cls.blog_description = 'Test Blog Description'
        cls.comment_one = 'Test Comment'
        cls.comment_two = "test comment 2 test comment 2 test comment 2 test comment 2 test comment 2 test comment 2 test comment 2 test comment 2 "

        cls.test_user = user.objects.create_user(
            email=cls.user_email, name=cls.user_name, password=cls.user_password)
        cls.test_user.save()

        cls.blog = Blog.objects.create(
            title=cls.blog_title, author=cls.test_user, description=cls.blog_description)
        cls.blog_comment_one = BlogComment.objects.create(
            comment=cls.comment_one, blog=cls.blog, author=cls.test_user)
        cls.blog_comment_two = BlogComment.objects.create(
            comment=cls.comment_two, blog=cls.blog, author=cls.test_user)

    def test_object_name_with_small_length(self):
        expected_object_name = self.blog_comment_one.comment
        self.assertEqual(expected_object_name, str(
            self.blog_comment_one))

    def test_object_name_with_high_length(self):
        len_comment = 75
        expected_object_name = self.blog_comment_two.comment[:len_comment] + '...'
        self.assertEqual(expected_object_name, str(
            self.blog_comment_two))

    def test_comment_label(self):
        expected_comment_label = 'comment'
        actual_comment_label = self.blog_comment_one._meta.get_field(
            'comment').verbose_name
        self.assertEqual(expected_comment_label, actual_comment_label)

    def test_blog_label(self):
        expected_blog_label = 'blog'
        actual_blog_label = self.blog_comment_one._meta.get_field(
            'blog').verbose_name
        self.assertEqual(actual_blog_label, expected_blog_label)

    def test_author_label(self):
        expected_author_label = 'author'
        actual_author_label = self.blog_comment_one._meta.get_field(
            'author').verbose_name
        self.assertEqual(actual_author_label, expected_author_label)

    def test_comment_date_label(self):
        expected_comment_date_label = 'date'
        actual_comment_date_label = self.blog_comment_one._meta.get_field(
            'comment_date').verbose_name
        self.assertEqual(actual_comment_date_label,
                         expected_comment_date_label)

    def test_comment_max_length(self):
        max_length = self.blog_comment_one._meta.get_field('comment').max_length
        self.assertEqual(max_length, 1000)


class BlogTagModelTests(TestCase):

    def setUp(self):
        self.tag_name = 'Test Tag'
        self.tag = BlogTag.objects.create(name=self.tag_name)

    def test_get_absolute_url(self):
        self.assertEqual(self.tag.get_absolute_url(), '/tags/'+str(self.tag.id))
