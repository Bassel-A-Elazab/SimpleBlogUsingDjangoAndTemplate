from django.core.paginator import Paginator
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
from django.http import HttpResponseForbidden
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import DetailView
from django.views.generic import FormView
from django.views.generic import ListView
from django.views.generic import CreateView
from django.views.generic import DeleteView
from django.views.generic.detail import SingleObjectMixin

from .forms import BlogCommentForm, BlogCreateForm

from .models import Blog, BlogTag


class BlogListView(ListView):
    paginate_by = 10
    queryset = Blog.objects.order_by('-post_date')
    template_name = "home/index.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        featured_blog = self.queryset.annotate(tag_count=Count('tags')).order_by('-tag_count').first()
        recent_blog = self.queryset.latest('post_date') 
        top_tags = BlogTag.objects.annotate(num_blogs=Count('blogs')).order_by('-num_blogs')[:10]

        context["featured_blog"] = featured_blog
        context["recent_blog"] = recent_blog
        context["top_tags"] = top_tags
        return context


class BlogDetailView(DetailView):
    model = Blog

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = BlogCommentForm()
        return context


class BlogDeleteView(LoginRequiredMixin, DeleteView):
    model = Blog

    def get_success_url(self):
        return reverse_lazy('blogger-dashboard', kwargs={'pk': self.request.user.pk})
    

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
        comment.author = self.request.user
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


class BlogCreateView(LoginRequiredMixin, CreateView):
    model = Blog
    form_class = BlogCreateForm
    template_name = 'blog/blog_add.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class BlogTagList(ListView):
    paginate_by = 10
    model = BlogTag
    template_name = "blog/blog_tag_list.html"
    context_object_name = "tag_list"


class BlogTagDetail(DetailView):
    paginate_by = 5
    model = BlogTag
    template_name = "blog/blog_tag_detail.html"
    context_object_name = "tag"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        blogs = self.object.blogs.all()

        paginator = Paginator(blogs, self.paginate_by)
        page_number = self.request.GET.get("page")
        page_obj = paginator.get_page(page_number)
        context["blogs"] = page_obj
        return context
