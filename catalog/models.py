from django.db import models

class NetflixTitle(models.Model):
    TYPE_CHOICES = [
        ('Movie', 'Movie'),
        ('TV Show', 'TV Show'),
    ]
    
    show_id = models.CharField(max_length=10, unique=True)
    title_type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    title = models.CharField(max_length=200)
    director = models.CharField(max_length=300, blank=True, null=True)
    cast = models.TextField(blank=True, null=True)
    country = models.CharField(max_length=200, blank=True, null=True)
    date_added = models.DateField(blank=True, null=True)
    release_year = models.IntegerField()
    rating = models.CharField(max_length=10, blank=True, null=True)
    duration = models.CharField(max_length=50)
    genres = models.CharField(max_length=200)
    description = models.TextField()
    
    def __str__(self):
        return f"{self.title} ({self.release_year})"
    
    class Meta:
        ordering = ['-release_year']