from django.db import models

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class Channel(models.Model):
    title = models.CharField(max_length=100)
    wallpaper = models.URLField()
    logo = models.URLField()

    def __str__(self):
        return self.title
    
    def get_class_name(self):
        return self.__class__.__name__
    
class Video(models.Model):
    title = models.CharField(max_length=100)
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE)  # Chave estrangeira para o show
    url = models.URLField()
    thumbnail = models.URLField()
    published_date = models.DateTimeField()
    tags = models.ManyToManyField('Tag')
    watched = models.BooleanField(default=False)

    def __str__(self):
        return self.title