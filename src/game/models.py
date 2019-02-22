import datetime

from django.db import models
from django.utils import timezone


class Game(models.Model):
    name = models.CharField(max_length=128, default='Yar')
    sea_map = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    map_size = models.IntegerField(default=0)
    rows = models.CharField(max_length=45)
    cols = models.CharField('columns', max_length=45)
    initial_data = models.CharField(max_length=60)

    def was_published_recently(self, days=1):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=days)

    def __str__(self):
        return self.name
