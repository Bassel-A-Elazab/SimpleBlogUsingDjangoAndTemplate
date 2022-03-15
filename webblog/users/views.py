from re import template
from django.views.generic import ListView

from .models import MyUser


class BloggerListView(ListView):
    model = MyUser
    template_name = "blog/blog_author_list.html"
    context_object_name = "blogger_list"
