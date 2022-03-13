from django import forms

from .models import BlogComment


class BlogCommentForm(forms.ModelForm):
    comment = forms.CharField(
        widget=forms.Textarea(
            attrs={'placeholder': 'Add your comment...'}
        )
    )

    class Meta:
        model = BlogComment
        fields = ['comment']
