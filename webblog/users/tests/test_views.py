from django.urls import reverse
from django.test import TestCase

from webblog.users.models import MyUser
from webblog.blog.models import Blog


class BloggerListViewTest(TestCase):

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


class BloggerDetailViewTest(TestCase):

    @classmethod
    def setUpTestData(self):
        self.test_user1 = MyUser.objects.create_user(
            email='test@user.com', name='test', password='test123')
        self.blog = Blog.objects.create(
            title='Test Blog 1', author=self.test_user1, description='Test Blog 1 Description')

    def test_view_uses_correct_template(self):
        response = self.client.get(
            reverse('blogger-detail', kwargs={"pk": self.test_user1.pk}))
        expected_template_used = "blog/blog_author_detail.html"
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, expected_template_used)

    def test_view_uses_correct_context_object_name(self):
        response = self.client.get(
            reverse('blogger-detail', kwargs={"pk": self.test_user1.pk}))
        expected_context_object_name = "blogger"
        self.assertEqual(response.status_code, 200)
        self.assertIn(expected_context_object_name, response.context)

    def test_view_uses_correct_blog_list_context(self):
        response = self.client.get(
            reverse('blogger-detail', kwargs={"pk": self.test_user1.pk}))

        expected_blog_context_object_name = "blogger_blog_list"
        expected_blog_title = "Test Blog 1"
        expected_blog_description = "Test Blog 1 Description"
        expected_blog_author = self.test_user1

        output_blogger_blog = response.context_data['blogger_blog_list'][0]
        
        self.assertEqual(response.status_code, 200)
        self.assertIn(expected_blog_context_object_name, response.context)
        self.assertEqual(expected_blog_title, output_blogger_blog.title)
        self.assertEqual(expected_blog_description, output_blogger_blog.description)
        self.assertEqual(expected_blog_author, self.test_user1)
