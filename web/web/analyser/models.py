from django.db import models


class Creator(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, unique=True)
    times_watched = models.IntegerField(default=1)
    url = models.URLField(null=True, blank=True, unique=True)

    @classmethod
    def create(cls, name, url):
        return cls(name=name, url=url)

    def __str__(self):
        return self.name


class VideoRecord(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=150)
    creator = models.ForeignKey(to=Creator, on_delete=models.CASCADE)
    time_watched = models.DateTimeField()
    url = models.URLField(null=True, blank=True)

    @classmethod
    def create(cls, title, creator, time_watched, url):
        return cls(title=title, creator=creator, time_watched=time_watched, url=url)
