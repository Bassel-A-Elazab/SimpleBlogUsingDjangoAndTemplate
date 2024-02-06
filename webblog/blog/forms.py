from django import forms
from django_summernote.widgets import SummernoteWidget

from .models import Blog, BlogComment


class BlogBaseForm(forms.ModelForm):

    class Meta:
        model = Blog 
        fields = ['title', 'description', 'cover', 'tags']
        widgets = {
            'description': SummernoteWidget(),
        }


class BlogCreateForm(BlogBaseForm):
    class Meta(BlogBaseForm.Meta):
        pass


class BlogUpdateForm(BlogBaseForm):
    class Meta(BlogBaseForm.Meta):
        pass


class BlogCommentForm(forms.ModelForm):
    comment = forms.CharField(
        widget=forms.Textarea(
            attrs={'placeholder': 'Add your comment...'}
        )
    )

    class Meta:
        model = BlogComment
        fields = ['comment']
