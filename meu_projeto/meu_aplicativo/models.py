from django.db import models

class Channel(models.Model):
    name = models.CharField(max_length=100)  # Nome do canal

    def __str__(self):
        return self.name

class Video(models.Model):
    title = models.CharField(max_length=100)
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE)  # Chave estrangeira para o canal
    url = models.URLField()
    thumbnail = models.URLField()
    wallpaper = models.URLField()
    logo = models.URLField()
    published_date = models.DateTimeField()
    tags = models.ManyToManyField('Tag')
    description = models.CharField(max_length=340)
    rating = models.IntegerField()

    def __str__(self):
        return self.title
    
    def get_class_name(self):
        return self.__class__.__name__

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name
    
class Show(models.Model):
    title = models.CharField(max_length=100)
    thumbnail = models.URLField()
    wallpaper = models.URLField()
    logo = models.URLField()
    tags = models.ManyToManyField('Tag')
    description = models.CharField(max_length=340)
    rating = models.IntegerField()

    def __str__(self):
        return self.title
    
    def get_class_name(self):
        return self.__class__.__name__
    
class Episode(models.Model):
    title = models.CharField(max_length=100)
    show = models.ForeignKey(Show, on_delete=models.CASCADE)  # Chave estrangeira para o show
    season = models.IntegerField()
    url = models.URLField()
    thumbnail = models.URLField()

    def __str__(self):
        return self.title