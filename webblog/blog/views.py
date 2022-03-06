
from django.http import HttpResponseForbidden
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView
from django.views.generic import DetailView
from django.views.generic import FormView
from django.views.generic.detail import SingleObjectMixin

from .models import Blog
from .forms import BlogCommentForm


class BlogListView(ListView):
    context_object_name = 'my_blog_list'
    queryset = Blog.objects.order_by('-post_date')


class BlogDetailView(DetailView):
    model = Blog
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = BlogCommentForm()
        return context


class BlogCommentFormView(SingleObjectMixin, FormView):
    model = Blog
    form_class = BlogCommentForm
    template_name = "blog/blog_detail.html"

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseForbidden()
        self.object = self.get_object()
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        comment = form.save(commit=False)
        comment.blog = self.object
        comment.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('blog-detail', kwargs={'pk': self.object.pk})


class BlogDetailCommentView(View):
    def get(self, request, *args, **kwargs):
        view = BlogDetailView.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = BlogCommentFormView.as_view()
        return view(request, *args, **kwargs)
