from django.db import models

class Channel(models.Model):
    name = models.CharField(max_length=100)  # Nome do canal
    description = models.TextField()  # Descrição do canal
    background_image_url = models.URLField()  # URL da imagem de fundo do canal

    def __str__(self):
        return self.name

class Video(models.Model):
    title = models.CharField(max_length=100)
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE)  # Chave estrangeira para o canal
    description = models.TextField()
    url = models.URLField()
    thumbnail = models.URLField()

    def __str__(self):
        return self.title
