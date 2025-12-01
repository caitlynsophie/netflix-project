from django.db import models

class NetflixTitle(models.Model):
    TYPE_CHOICES = [
        ('Movie', 'Movie'),
        ('TV Show', 'TV Show'),
    ]

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

class Review(models.Model):
    title = models.ForeignKey(NetflixTitle, on_delete=models.CASCADE, related_name='reviews')
    # Allow half-star ratings (0.0 - 5.0 in 0.5 increments)
    rating = models.DecimalField(max_digits=2, decimal_places=1, default=0.0)
    review_text = models.TextField(blank=True)
    date_watched = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date_watched', '-created_at']

    def __str__(self):
        return f"{self.title.title} - {self.rating}/5"