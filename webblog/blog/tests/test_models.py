from django.test import TestCase
from django.utils.translation import gettext_lazy as _

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

    def test_title_label(self):
        blog = Blog.objects.get(id=1)
        title_label = blog._meta.get_field('title').verbose_name
        self.assertEqual(title_label, _("blog's title"))  
    
    def test_author_label(self):
        blog = Blog.objects.get(id=1)
        author_label = blog._meta.get_field('author').verbose_name
        self.assertEqual(author_label, _("blog's author"))
    
    def test_description_label(self):
        blog = Blog.objects.get(id=1)
        description_label = blog._meta.get_field('description').verbose_name
        self.assertEqual(description_label, _("blog's description"))

    def test_post_date_label(self):
        blog = Blog.objects.get(id=1)
        post_date_label = blog._meta.get_field("post_date").verbose_name
        self.assertEqual(post_date_label, _("blog's posted date"))

    def test_title_max_length(self):
        blog = Blog.objects.get(id=1)
        max_length = blog._meta.get_field('title').max_length
        self.assertEqual(max_length, 200)

    def test_description_max_length(self):
        blog = Blog.objects.get(id=1)
        max_length = blog._meta.get_field('description').max_length
        self.assertEqual(max_length, 2000)

    def test_get_absolute_url(self):
        blog = Blog.objects.get(id=1)
        self.assertEqual(blog.get_absolute_url(), '/blog/blogs/1')
        