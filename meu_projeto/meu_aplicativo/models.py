from django.db import models

class Channel(models.Model):
    name = models.CharField(max_length=100)  # Nome do canal

    def __str__(self):
        return self.name

class Video(models.Model):
    title = models.CharField(max_length=100)
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE)  # Chave estrangeira para o canal
    description = models.TextField()
    url = models.URLField()
    thumbnail = models.URLField()
    published_date = models.DateTimeField()

    def __str__(self):
        return self.title
