from django.db import models
from django.conf import settings
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill
import datetime


def photo_path(instance, filename):
    now= datetime.datetime.now()
    return 'post/{}/{}.jpg'.format(instance.author, now.strftime('%Y/%m/%d'))


class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=255, default="")
    content = models.TextField(default="")
    photo = ProcessedImageField(upload_to=photo_path, 
                                       processors=[ResizeToFill(600,600)],
                                       format="JPEG",
                                       options={'quality':90},
                                       blank = True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.content
