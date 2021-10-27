from django.db import models
from django.utils import timezone

# Create your models here.

class Species(models.Model):
    name = models.CharField(max_length=30, primary_key=True)
    class Meta:
        db_table = 'species'


class Animal(models.Model):
    name = models.CharField(max_length=30)
    species = models.ForeignKey(Species, on_delete=models.CASCADE)
    last_feed_time = models.DateTimeField(default=timezone.now)
    class Meta:
        db_table = 'animal'
