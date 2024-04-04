from django.test import TestCase

from webblog.blog.forms import BlogCommentForm


class BlogFormsTests(TestCase):

    def test_valid_comment_form(self):
        form = BlogCommentForm(
            {
                "comment": "Test comment 1",
            }
        )
        self.assertTrue(form.is_valid())
