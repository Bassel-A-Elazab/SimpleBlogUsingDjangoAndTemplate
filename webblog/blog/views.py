from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView
from django.views.generic import DetailView
from django.views.generic.edit import CreateView

from .models import Blog, BlogComment


class BlogListView(ListView):
    context_object_name = 'my_blog_list'
    queryset = Blog.objects.order_by('-post_date')


class BlogDetailView(DetailView):
    model = Blog


class BlogCommentCreateView(LoginRequiredMixin, CreateView):
    model = BlogComment
    fields = ['comment']

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.blog = get_object_or_404(Blog, pk=self.kwargs['pk'])
        return super(BlogCommentCreateView, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('blog-detail', kwargs={'pk': self.kwargs['pk'], })
