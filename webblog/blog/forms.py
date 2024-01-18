from django import forms

from .models import Blog, BlogComment


class BlogCreateForm(forms.ModelForm):
    class Meta:
        model = Blog 
        fields = ['title', 'description', 'cover', 'tags']


class BlogCommentForm(forms.ModelForm):
    comment = forms.CharField(
        widget=forms.Textarea(
            attrs={'placeholder': 'Add your comment...'}
        )
    )

    class Meta:
        model = BlogComment
        fields = ['comment']
