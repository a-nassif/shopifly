from django.db import models

# Create your models here.


class themes(models.Model):
    name = models.CharField(max_length=255)
    logo = models.ImageField(upload_to='themes_logos')
    theme = models.CharField(max_length=255)