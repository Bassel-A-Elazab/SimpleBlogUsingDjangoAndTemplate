from django.db import models 

from datetime import datetime
from webblog.users.models import MyUser

class Blog(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(MyUser, on_delete=models.SET_NULL, null=True)
    description = models.TextField(max_length=2000, help_text="Enter you blog text here.")
    post_date = models.DateTimeField(default=datetime.now)

    class Meta:
        ordering = ["-post_date"]
    