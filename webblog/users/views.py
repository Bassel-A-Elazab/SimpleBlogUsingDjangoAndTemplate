from django.core.paginator import Paginator
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views.generic import ListView, DetailView, UpdateView

from .forms import BloggerUpdateForm

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
        blog_list = Blog.objects.filter(author=self.blogger)

        paginator = Paginator(blog_list, 5)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context['blogger_blog_list'] = page_obj
        return context


class BloggerUpdateView(LoginRequiredMixin, UpdateView):
    model = MyUser
    form_class = BloggerUpdateForm
    template_name = 'users/settings.html'

    def get_success_url(self):
        pk = self.kwargs["pk"]
        return reverse("blogger-settings", kwargs={"pk": pk})
