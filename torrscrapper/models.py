from django.db import models

# Create your models here.


class Movies(models.Model):
    title=models.TextField()
    image_url=models.TextField()
    release_date=models.CharField(max_length=20)
    synopsis=models.TextField()
    quality_720p=models.TextField(default='NULL')
    quality_720p_size=models.CharField(max_length=20,default='NULL')
    quality_1080p=models.TextField(default='NULL')
    quality_1080p_size=models.CharField(max_length=20,default='NULL')


