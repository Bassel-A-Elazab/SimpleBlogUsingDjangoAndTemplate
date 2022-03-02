from django.test import TestCase
from django.urls import reverse


from webblog.blog.models import Blog
from webblog.users.models import MyUser


class BlogListViewTest(TestCase):

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/blog/blogs/')
        self.assertEqual(response.status_code, 200)
    
    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('blogs'))
        self.assertEqual(response.status_code, 200)
        
    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('blogs'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/blog_list.html')

class BlogCommentViewTest(TestCase):

    @classmethod
    def setUpTestData(self):
        self.test_user1 = MyUser.objects.create_superuser(email='test1@user.com', name='test1', password='Test123')
        self.blog = Blog.objects.create(title='Blog 1 title', description='Blog 1 description', author=self.test_user1)

    def test_view_get_correct_context(self):
        self.client.force_login(self.test_user1)

        data = {
            'comment': 'Blog 1 comment',
            'blog': self.blog,
            'author': self.test_user1
        }
        response = self.client.post(reverse('add-comment', args=[self.blog.pk]), data=data)
        self.assertEqual(response.status_code, 200)