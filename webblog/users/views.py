from pyexpat import model
from django.views.generic import ListView
from django.views.generic import DetailView

from .models import MyUser


class BloggerListView(ListView):
    model = MyUser
    template_name = "blog/blog_author_list.html"
    context_object_name = "blogger_list"

class BloggerDetailView(DetailView):
    model = MyUser
    template_name = "blog/blog_author_detail.html"
    context_object_name = "blogger"

