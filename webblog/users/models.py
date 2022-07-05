from PIL import Image

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.core.files.base import ContentFile
from django.db import models
from django.dispatch import receiver
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from allauth.account.signals import user_signed_up

from .managers import MyUserManager

from .utils import Avatar


class MyUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), unique=True)
    name = models.CharField(_('username'), max_length=150)
    bio = models.TextField(_('bio'), blank=True, null=True)
    date_of_birth = models.DateField(_('birthdate'), blank=True, null=True)
    picture = models.ImageField(
        _('profile picture'), upload_to="profile_pics/", blank=True, null=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def get_absolute_url(self):
        return reverse('blogger-detail', kwargs={'pk': self.pk})

    def save(self, *args, **kwargs):
        super(MyUser, self).save(*args, **kwargs)
        if self.picture:
            image = Image.open(self.picture.path)
            height, width = image.size
            if height <= 300 and width <= 300:
                image.close()
                return
            output_size = (300, 300)
            image.thumbnail(output_size)
            image.save(self.picture.path)
            image.close

    def __str__(self):
        return self.email


@receiver(user_signed_up)
def user_signed_up_(request, user, **kwargs):
    s = Avatar.generate(128, user.email, "PNG")
    user.picture.save('%s.png' %
                      (user.email[0] + str(user.pk)), ContentFile(s))
    user.is_active = True
    user.save()
