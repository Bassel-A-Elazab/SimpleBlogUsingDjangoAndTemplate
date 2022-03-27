from django.test import TestCase
from django.urls import reverse

from webblog.blog.models import Blog, BlogComment
from webblog.users.models import MyUser


class BlogListViewTest(TestCase):

    @classmethod
    def setUpTestData(self):
        self.test_user1 = MyUser.objects.create_user(
            email='test@user.com', name='test', password='test123')
        self.test_user1.is_active = True
        self.test_user1.save()
        self.blog = Blog.objects.create(
            title='Test Blog 1', author=self.test_user1, description='Test Blog 1 Description')

        number_of_blogs = 13
        for blog_num in range(number_of_blogs):
            Blog.objects.create(title='Test Blog %s' % blog_num, author=self.test_user1,
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

    def test_pagination_is_five(self):
        response = self.client.get(reverse('blogs'))
        expected_pagination_number = 5
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['is_paginated' == True])
        self.assertEqual(
            len(response.context['my_blog_list']), expected_pagination_number)


class BlogDetailCommentViewTest(TestCase):

    @classmethod
    def setUpTestData(self):
        self.test_user1 = MyUser.objects.create_user(
            email='test@user.com', name='test', password='test123')
        self.test_user1.is_active = True
        self.test_user1.save()
        self.blog = Blog.objects.create(
            title='Test Blog 1', author=self.test_user1, description='Test Blog 1 Description')

    def test_view_get_correct_blog_detail(self):
        response = self.client.get(
            reverse('blog-detail', kwargs={'pk': self.blog.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Blog 1')
        self.assertContains(response, 'Test Blog 1 Description')
        self.assertTemplateUsed(response, 'blog/blog_detail.html')

    def test_view_uses_corrext_form_in_context(self):
        response = self.client.get(
            reverse('blog-detail', kwargs={'pk': self.blog.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertIn('form', response.context)

    def test_submit_comment_logged_in_success(self):
        data = {
            'comment': 'Comment 1',
            'blog': self.blog,
            'author': self.test_user1
        }
        self.client.login(email='test@user.com', password="test123")
        response = self.client.post(
            reverse('blog-detail', kwargs={'pk': self.blog.pk}), data=data)
        self.assertEqual(response.status_code, 302)  # Found redirect
        self.assertEqual(BlogComment.objects.last().comment, 'Comment 1')

    def test_submit_comment_logged_in_failed(self):
        data = {
            'comment': 'Comment 1',
            'blog': self.blog,
            'author': self.test_user1
        }
        response = self.client.post(
            reverse('blog-detail', kwargs={'pk': self.blog.pk}), data=data)
        self.assertEqual(response.status_code, 403)
