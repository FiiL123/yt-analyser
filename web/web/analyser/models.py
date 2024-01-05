from django.db import models


class VideoRecord(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=150)
    creator = models.CharField(max_length=100)
    time_watched = models.DateTimeField()
    url = models.URLField()
