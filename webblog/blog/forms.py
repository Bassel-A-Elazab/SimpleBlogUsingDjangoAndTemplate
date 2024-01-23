from django import forms
from django_summernote.widgets import SummernoteWidget

from .models import Blog, BlogComment


class BlogCreateForm(forms.ModelForm):

    class Meta:
        model = Blog 
        fields = ['title', 'description', 'cover', 'tags']
        widgets = {
            'description': SummernoteWidget(),
        }

class BlogCommentForm(forms.ModelForm):
    comment = forms.CharField(
        widget=forms.Textarea(
            attrs={'placeholder': 'Add your comment...'}
        )
    )

    class Meta:
        model = BlogComment
        fields = ['comment']
