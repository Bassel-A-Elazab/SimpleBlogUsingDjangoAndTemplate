from pyexpat import model
from statistics import mode
from django.db import models 
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from datetime import datetime

from webblog.users.models import MyUser


class Blog(models.Model):
    title = models.CharField(_("blog's title"), max_length=200)
    author = models.ForeignKey(MyUser, verbose_name=_("blog's author"), on_delete=models.SET_NULL, null=True)
    description = models.TextField(_("blog's description"), max_length=2000, help_text="Enter you blog text here.")
    post_date = models.DateTimeField(_("blog's posted date"), default=datetime.now)


    class Meta:
        ordering = ["-post_date"]
    
    def get_absolute_url(self):
        return reverse("blog-detail", kwargs={"pk": self.pk})

    def __str__(self):
        return self.title


class BlogComment(models.Model):
    blog = models.ForeignKey(Blog, verbose_name=_("blog's resource"), on_delete=models.CASCADE)
    author = models.ForeignKey(MyUser, verbose_name=_("author's comment"), on_delete=models.SET_NULL, null=True)
    comment = models.TextField(_("blog's comment"), max_length=1000, help_text="Enter comment about blog here.")
    comment_date = models.DateTimeField(_("comment's date"), default=datetime.now)

    class Meta:
        ordering = ["comment_date"]

    def __str__(self):
        len_comment = 75
        if len(self.comment) > len_comment:
            return self.comment[:len_comment] + '...'
        return self.comment        