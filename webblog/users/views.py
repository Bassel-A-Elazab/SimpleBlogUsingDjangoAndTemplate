from django.shortcuts import get_object_or_404
from django.views.generic import ListView
from django.views.generic import DetailView

from .models import MyUser

from webblog.blog.models import Blog


class BloggerListView(ListView):
    paginate_by = 5
    model = MyUser
    template_name = "blog/blog_author_list.html"
    context_object_name = "blogger_list"


class BloggerDetailView(DetailView):
    model = MyUser
    template_name = "blog/blog_author_detail.html"
    context_object_name = "blogger"

    def get_context_data(self, *args, **kwargs):
        context = super(BloggerDetailView, self).get_context_data(
            *args, **kwargs)
        self.blogger = get_object_or_404(MyUser, pk=self.kwargs['pk'])
        context['blogger_blog_list'] = Blog.objects.filter(author=self.blogger)
        return context
