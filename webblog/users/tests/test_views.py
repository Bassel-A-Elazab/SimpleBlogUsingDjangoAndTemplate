from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile
from django.test import TestCase
from django.urls import reverse

from webblog.blog.models import Blog
from webblog.users.utils import Avatar


class BloggerListViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        user = get_user_model()
        cls.user_name = 'test'
        cls.user_password = 'test123'
        number_of_users = 13
        for user_num in range(number_of_users):
            email = f'{cls.user_name}{user_num}@user.com'
            name = f'{cls.user_name}{user_num}'
            user.objects.create_user(
                email=email, name=name, password=cls.user_password)

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get(reverse('bloggers'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('bloggers'))
        template_use_expected = 'blog/blog_author_list.html'
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_use_expected)

    def test_view_uses_correct_context_object_name(self):
        response = self.client.get(reverse('bloggers'))
        expected_context_object_name = 'blogger_list'
        self.assertEqual(response.status_code, 200)
        self.assertIn(expected_context_object_name, response.context)

    def test_pagination_is_five(self):
        response = self.client.get(reverse('bloggers'))
        expected_pagination_number = 5
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['is_paginated'])
        self.assertEqual(
            len(response.context['blogger_list']), expected_pagination_number)


class BloggerDetailViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        user = get_user_model()
        cls.user_email = 'test@user.com'
        cls.user_name = 'test'
        cls.user_password = 'test123'
        cls.blog_title = 'Test Blog'
        cls.blog_description = 'Test Blog Description'
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

        for blog_num in range(number_of_blogs):
            title = f'{cls.blog_title}{blog_num}'
            description = f'{cls.blog_description}{blog_num}'
            Blog.objects.create(title=title, author=cls.test_user,
                                description=description)

    def test_view_uses_correct_template(self):
        response = self.client.get(
            reverse('blogger-detail', kwargs={"pk": self.test_user.pk}))
        expected_template_used = "blog/blog_author_detail.html"
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, expected_template_used)

    def test_view_uses_correct_context_object_name(self):
        response = self.client.get(
            reverse('blogger-detail', kwargs={"pk": self.test_user.pk}))
        expected_context_object_name = "blogger"
        self.assertEqual(response.status_code, 200)
        self.assertIn(expected_context_object_name, response.context)

    def test_view_uses_correct_blog_list_context(self):
        response = self.client.get(
            reverse('blogger-detail', kwargs={"pk": self.test_user.pk}))

        expected_blog_context_object_name = "blogger_blog_list"
        expected_blog_title = "Test Blog12"
        expected_blog_description = "Test Blog Description12"
        expected_blog_author = self.test_user
        output_blogger_blog = response.context_data['blogger_blog_list'][0]

        self.assertEqual(response.status_code, 200)
        self.assertIn(expected_blog_context_object_name, response.context)
        self.assertEqual(expected_blog_title, output_blogger_blog.title)
        self.assertEqual(expected_blog_description,
                         output_blogger_blog.description)
        self.assertEqual(expected_blog_author, self.test_user)

    def test_pagination_is_five(self):
        response = self.client.get(
            reverse('blogger-detail', kwargs={"pk": self.test_user.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['blogger_blog_list']), 5)


class BloggerUpdateViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        user = get_user_model()
        cls.user_email = 'test@user.com'
        cls.user_name = 'test'
        cls.user_password = 'test123'

        cls.test_user = user.objects.create_user(
            email=cls.user_email, name=cls.user_name, password=cls.user_password)
        cls.test_user.is_active = True
        cls.test_user.save()

    def test_view_get_desired_success_url(self):
        expected_success_url = '/bloggers/%s/settings' % self.test_user.pk
        data = {
            'name': 'newTest'
        }

        self.client.login(email=self.user_email, password=self.user_password)
        response = self.client.post(
            reverse('blogger-settings', kwargs={'pk': self.test_user.pk}), data=data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, expected_success_url)

    def test_view_updated_name_correct(self):
        expected_name = 'newTest'
        data = {
            'name': expected_name
        }

        self.client.login(email=self.user_email, password=self.user_password)
        response = self.client.post(
            reverse('blogger-settings', kwargs={'pk': self.test_user.pk}), data=data)
        self.test_user.refresh_from_db()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.test_user.name, expected_name)
