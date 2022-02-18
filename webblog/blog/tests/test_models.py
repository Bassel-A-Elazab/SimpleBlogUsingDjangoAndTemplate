from django.test import TestCase

from datetime import datetime

from webblog.blog.models import Blog
from webblog.users.models import MyUser


class BlogModelTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        test_user1 = MyUser.objects.create_user(email='test@user.com', name='test', password='test123')
        test_user1.save()
        Blog.objects.create(title='Test Blog 1', author=test_user1, description='Test Blog 1 Description')

    def test_object_title(self):
        blog=Blog.objects.get(id=1)
        expected_object_title = blog.title 
        self.assertEqual(expected_object_title, str(blog))
        
    def test_title_max_length(self):
        blog = Blog.objects.get(id=1)
        max_length = blog._meta.get_field('title').max_length
        self.assertEqual(max_length, 200)

    def test_description_max_length(self):
        blog = Blog.objects.get(id=1)
        max_length = blog._meta.get_field('description').max_length
        self.assertEqual(max_length, 2000)

    