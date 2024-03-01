from django.db import models
class Movies(models.Model):
    title = models.TextField()
    image_url = models.TextField()
    release_date = models.CharField(max_length=20)
    synopsis = models.TextField()
    quality_720p = models.TextField(default="NULL")
    quality_720p_size = models.CharField(max_length=20, default="NULL")
    quality_1080p = models.TextField(default="NULL")
    quality_1080p_size = models.CharField(max_length=20, default="NULL")

class Games(models.Model):
    title = models.TextField()
    image_url = models.TextField()
    release_date = models.CharField(max_length=20)
    description = models.TextField()
    size = models.CharField(max_length=40)
    developer = models.CharField(max_length=100)
    magnet = models.TextField()

class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.CharField(max_length=500)
