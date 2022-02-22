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


     