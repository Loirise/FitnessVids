from django.db import models

# Create your models here.

class VideoModel(models.Model):
    title = models.CharField(max_length=100, null=False, blank=False)
    video = models.FileField(upload_to="uploads/")  # for uploads with date/time = uploads/%Y/%m/%d/



