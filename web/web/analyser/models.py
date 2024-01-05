from django.db import models


class VideoRecord(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=150)
    creator = models.CharField(max_length=100)
    time_watched = models.DateTimeField()
    url = models.URLField()

    @classmethod
    def create(cls, title, creator, time_watched, url):
        return cls(title=title, creator=creator, time_watched=time_watched, url=url)
