from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.files.images import get_image_dimensions
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.utils import timezone


class BlogTag(models.Model):
    name = models.CharField(max_length=250, unique=True)

    class Meta:
        ordering = ["name"]

    def get_absolute_url(self):
        return reverse("tag-detail", kwargs={"pk": self.pk})
    
    def __str__(self):
        return self.name
    

class Blog(models.Model):
    title = models.CharField(_("title"), max_length=200)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_(
        "author"), on_delete=models.SET_NULL, null=True)
    description = models.TextField(
        _("description"), max_length=2000, help_text="Enter you blog text here.")
    post_date = models.DateTimeField(
        _("posted date"), default=timezone.now)
    cover = models.ImageField(
        _("cover image"), upload_to="blog_cover_images/", blank=True, null=True)
    tags = models.ManyToManyField(to=BlogTag, related_name="blogs", blank=True)

    class Meta:
        ordering = ["-post_date"]

    @property
    def comment_count(self):
        return self.blogcomment_set.count()
    
    def get_absolute_url(self):
        return reverse("blog-detail", kwargs={"pk": self.pk})

    def clean(self):
        super(Blog, self).clean()
        if self.cover:
            width, height = get_image_dimensions(self.cover)
            if width > 4096 or height > 4096:
                raise ValidationError(
                    "Image size should be less than or equal to 4096x4096")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class BlogComment(models.Model):
    blog = models.ForeignKey(Blog, verbose_name=_(
        "blog"), on_delete=models.CASCADE)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_(
        "author"), on_delete=models.SET_NULL, null=True)
    comment = models.TextField(_("comment"), max_length=1000)
    comment_date = models.DateTimeField(
        _("date"), default=timezone.now)

    class Meta:
        ordering = ["comment_date"]

    def __str__(self):
        len_comment = 75
        if len(self.comment) > len_comment:
            return self.comment[:len_comment] + '...'
        return self.comment
