from django.db import models
import logging

class Batch(models.Model):
    title = models.CharField(max_length=100)
    number = models.IntegerField(unique=True)
    playlist = models.CharField(max_length=100)
    
    def __str__(self):
        return self.title

class Channel(models.Model):
    title = models.CharField(max_length=100, unique=True)
    logo = models.URLField(null=True)
    wallpaper = models.URLField(null=True)
    description = models.CharField(max_length=5000, null=True)
    subscribers = models.IntegerField()

    def __str__(self):
        return self.title
    
    def get_class_name(self):
        return self.__class__.__name__
    
    def save(self, *args, **kwargs):
        try:
            super().save(*args, **kwargs)
            return self  # Return the saved instance
        except Exception as e:
            logging.error(f"Error saving video: {e}")
            raise
    
class Video(models.Model):
    title = models.CharField(max_length=100, unique=True)
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE)  # Chave estrangeira para o show
    url = models.URLField()
    thumbnail = models.URLField()
    uploadedDate = models.CharField(max_length=50)
    duration = models.CharField(max_length=100)
    views = models.CharField(max_length=100)

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        try:
            super().save(*args, **kwargs)
            return self  # Return the saved instance
        except Exception as e:
            logging.error(f"Error saving video: {e}")
            raise
        