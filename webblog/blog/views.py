from django.views.generic import ListView
from django.views.generic import DetailView

from .models import Blog


class BlogListView(ListView):
    context_object_name = 'my_blog_list'
    queryset = Blog.objects.order_by('-post_date')


class BlogDetailView(DetailView):
    model = Blog