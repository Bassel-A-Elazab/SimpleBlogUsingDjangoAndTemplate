from django.views.generic import ListView

from .models import Blog


class BlogListView(ListView):
    model = Blog
    context_object_name = 'my_blog_list'
    template_name = 'blog/blogs.html'
