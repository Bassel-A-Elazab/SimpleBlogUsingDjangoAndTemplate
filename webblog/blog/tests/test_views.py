from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile
from django.test import TestCase
from django.urls import reverse

from webblog.blog.models import Blog, BlogComment, BlogTag
from webblog.users.utils import Avatar


class BlogListViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        user = get_user_model()
        cls.user_email = 'test@user.com'
        cls.user_name = 'test'
        cls.user_password = 'test123'
        cls.blog_title = 'Test Blog'
        cls.blog_description = 'Test Blog Description'
        cls.number_of_blogs = 13

        cls.test_user = user.objects.create_user(
            email=cls.user_email, name=cls.user_name, password=cls.user_password)
        cls.test_user.is_active = True
        cls.test_user.save()
        Blog.objects.create(
            title=cls.blog_title, author=cls.test_user, description=cls.blog_description)
        
        for blog_num in range(cls.number_of_blogs):
            Blog.objects.create(title='Test Blog %s' % blog_num, author=cls.test_user,
                                description='Test Blog %s Description' % blog_num)

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('blogs'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('blogs'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/blog_list.html')

    def test_pagination_is_ten(self):
        response = self.client.get(reverse('blogs'))
        expected_pagination_number = 10
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['is_paginated'])
        self.assertEqual(
            len(response.context['blog_list']), expected_pagination_number)


class BlogDetailCommentViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        user = get_user_model()
        cls.user_email = 'test@user.com'
        cls.user_name = 'test'
        cls.user_password = 'test123'
        cls.blog_title = 'Test Blog'
        cls.blog_description = 'Test Blog Description'
        cls.blog_comment = 'Test Comment'

        cls.test_user = user.objects.create_user(
            email=cls.user_email, name=cls.user_name, password=cls.user_password)
        s = Avatar.generate(128, cls.test_user.email, "PNG")
        cls.test_user.picture.save('%s.png' %
                      (cls.test_user.email[0] + str(cls.test_user.pk)), ContentFile(s))
        cls.test_user.is_active = True
        cls.test_user.save()
        cls.blog = Blog.objects.create(
            title=cls.blog_title, author=cls.test_user, description=cls.blog_description)

    def test_view_get_correct_blog_detail(self):
        response = self.client.get(
            reverse('blog-detail', kwargs={'pk': self.blog.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/blog_detail.html')
        self.assertEqual(response.context_data['blog'].title, self.blog_title)
        self.assertEqual(response.context_data['blog'].description, self.blog_description)

    def test_submit_comment_logged_in_success(self):
        data = {
            'comment': self.blog_comment,
            'blog': self.blog,
            'author': self.test_user
        }
        self.client.login(email=self.user_email, password=self.user_password)
        response = self.client.post(
            reverse('blog-detail', kwargs={'pk': self.blog.pk}), data=data)
        self.assertEqual(response.status_code, 302)  # Found redirect
        self.assertEqual(BlogComment.objects.last().comment, self.blog_comment)

    def test_submit_comment_logged_in_failed(self):
        data = {
            'comment': self.blog_comment,
            'blog': self.blog,
            'author': self.test_user
        }
        response = self.client.post(
            reverse('blog-detail', kwargs={'pk': self.blog.pk}), data=data)
        self.assertEqual(response.status_code, 403)


class BlogTagDetailViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        user = get_user_model()
        cls.user_email = 'test@user.com'
        cls.user_name = 'test'
        cls.user_password = 'test123'
        cls.blog_title = 'Test Blog'
        cls.blog_description = 'Test Blog Description'
        cls.blog_comment = 'Test Comment'
        cls.tag_name = 'Test Tag'
        number_of_blogs = 13

        cls.test_user = user.objects.create_user(
            email=cls.user_email, name=cls.user_name, password=cls.user_password)
        s = Avatar.generate(128, cls.test_user.email, "PNG")
        cls.test_user.picture.save('%s.png' %
                      (cls.test_user.email[0] + str(cls.test_user.pk)), ContentFile(s))
        cls.test_user.is_active = True
        cls.test_user.save()
        cls.blog = Blog.objects.create(
            title=cls.blog_title, author=cls.test_user, description=cls.blog_description)
        
        cls.tag = BlogTag.objects.create(name=cls.tag_name)

        for blog_num in range(number_of_blogs):
            title = f'{cls.blog_title}{blog_num}'
            description = f'{cls.blog_description}{blog_num}'
            blog = Blog.objects.create(title=title, author=cls.test_user,
                                description=description)
            blog.tags.add(cls.tag)
        
    def test_tag_blogs_pagination_is_five(self):
        response = self.client.get(reverse('tag-detail', kwargs={"pk": self.tag.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['blogs']), 5)

    def test_view_uses_correct_template(self):
        expected_template_used = 'blog/blog_tag_detail.html'
        response = self.client.get(reverse('tag-detail', kwargs={"pk": self.tag.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, expected_template_used)



