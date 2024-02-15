from django.db import models

class Channel(models.Model):
    title = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.title
    
    def get_class_name(self):
        return self.__class__.__name__
    
class Video(models.Model):
    title = models.CharField(max_length=100, unique=True)
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE)  # Chave estrangeira para o show
    url = models.URLField()
    thumbnail = models.URLField()

    def __str__(self):
        return self.title