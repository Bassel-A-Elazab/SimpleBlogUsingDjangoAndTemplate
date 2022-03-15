from urllib import response
from django.urls import reverse
from django.test import TestCase

from webblog.users.models import MyUser


class BloggerListViewTest(TestCase):

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get(reverse('bloggers'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('bloggers'))
        template_use_expected = 'blog/blog_author_list.html'
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_use_expected)
    
    def test_view_uses_correct_context_object(self):
        response = self.client.get(reverse('bloggers'))
        context_object_name_expected = 'blogger_list'
        self.assertEqual(response.status_code, 200)
        self.assertIn(context_object_name_expected, response.context)