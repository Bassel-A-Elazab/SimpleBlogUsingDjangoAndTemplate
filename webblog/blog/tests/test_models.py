from django.test import TestCase
from django.utils.translation import gettext_lazy as _

from webblog.blog.models import Blog, BlogComment
from webblog.users.models import MyUser


class BlogModelTests(TestCase):

    @classmethod
    def setUpTestData(self):
        self.test_user1 = MyUser.objects.create_user(
            email='test@user.com', name='test', password='test123')
        self.test_user1.save()
        self.blog = Blog.objects.create(
            title='Test Blog 1', author=self.test_user1, description='Test Blog 1 Description')
        self.blog.save()

    def test_object_title(self):
        expected_object_title = self.blog.title
        self.assertEqual(expected_object_title, str(self.blog))

    def test_title_label(self):
        title_label = self.blog._meta.get_field('title').verbose_name
        self.assertEqual(title_label, _("blog's title"))

    def test_author_label(self):
        author_label = self.blog._meta.get_field('author').verbose_name
        self.assertEqual(author_label, _("blog's author"))

    def test_description_label(self):
        description_label = self.blog._meta.get_field(
            'description').verbose_name
        self.assertEqual(description_label, _("blog's description"))

    def test_post_date_label(self):
        post_date_label = self.blog._meta.get_field("post_date").verbose_name
        self.assertEqual(post_date_label, _("blog's posted date"))

    def test_title_max_length(self):
        max_length = self.blog._meta.get_field('title').max_length
        self.assertEqual(max_length, 200)

    def test_description_max_length(self):
        max_length = self.blog._meta.get_field('description').max_length
        self.assertEqual(max_length, 2000)

    def test_get_absolute_url(self):
        id = self.blog.id
        self.assertEqual(self.blog.get_absolute_url(), '/blogs/'+str(id))


class BlogCommentModelTests(TestCase):

    @classmethod
    def setUpTestData(self):
        self.test_user1 = MyUser.objects.create_user(
            email='test1@user.com', name='test1', password='test123')
        self.test_user1.save()
        self.test_user2 = MyUser.objects.create_user(
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
        comment_label = self.blog_comment._meta.get_field(
            'comment').verbose_name
        self.assertEqual(comment_label, _("blog's comment"))

    def test_blog_label(self):
        blog_label = self.blog_comment._meta.get_field('blog').verbose_name
        self.assertEqual(blog_label, "blog's resource")

    def test_author_label(self):
        author_label = self.blog_comment._meta.get_field('author').verbose_name
        self.assertEqual(author_label, "author's comment")

    def test_comment_date_label(self):
        comment_date_label = self.blog_comment._meta.get_field(
            'comment_date').verbose_name
        self.assertEqual(comment_date_label, "comment's date")

    def test_comment_max_length(self):
        max_length = self.blog_comment._meta.get_field('comment').max_length
        self.assertEqual(max_length, 1000)
