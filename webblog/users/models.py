from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.core.mail import send_mail
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.dispatch import receiver 
from django.core.files.base import ContentFile

from allauth.account.signals import user_signed_up

from .managers import MyUserManager
from .utils import Avatar

class MyUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), unique=True)
    name = models.CharField(max_length=150)
    bio = models.TextField(blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    picture = models.ImageField(blank=True, null=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return self.email

    def email_user(self, subject, message, from_email=None, **kwargs):
        send_mail(subject, message, from_email, [self.email], **kwargs)

@receiver(user_signed_up)
def user_signed_up_(request, user, **kwargs):
    s = Avatar.generate(128, user.email, "PNG")
    user.picture.save('%s.png' % (user.email[0] + str(user.pk)), ContentFile(s))
    user.is_active = True
    user.save()
