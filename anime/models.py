from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator


class Genre(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name = 'Genere'
        verbose_name_plural = 'Generi'


class Studio(models.Model):
    name = models.CharField(max_length=200, unique=True)
    country = models.CharField(max_length=100, default='Giappone')
    founded_year = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name = 'Studio'
        verbose_name_plural = 'Studio di produzione'


class Anime(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    episodes = models.IntegerField()
    year = models.IntegerField(null=True, blank=True)
    studio = models.ForeignKey(
        Studio, on_delete=models.SET_NULL, null=True, blank=True, related_name='anime_set'
    )
    genres = models.ManyToManyField(Genre, blank=True, related_name='anime_set')

    def __str__(self):
        return self.title

    def average_rating(self):
        entries = self.useranime_set.filter(rating__isnull=False)
        if entries.exists():
            total = sum(e.rating for e in entries)
            return round(total / entries.count(), 1)
        return None

    class Meta:
        ordering = ['title']


class Episode(models.Model):
    anime = models.ForeignKey(Anime, on_delete=models.CASCADE, related_name='episode_set')
    number = models.PositiveIntegerField()
    title = models.CharField(max_length=300, blank=True, null=True)
    duration_minutes = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.anime.title} — Ep. {self.number}"

    class Meta:
        ordering = ['anime', 'number']
        unique_together = ('anime', 'number')
        verbose_name = 'Episodio'
        verbose_name_plural = 'Episodi'


class UserAnime(models.Model):
    STATUS_CHOICES = [
        ('watching', 'In visione'),
        ('completed', 'Completato'),
        ('planned', 'Da vedere'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    anime = models.ForeignKey(Anime, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='planned')
    rating = models.IntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(1), MaxValueValidator(10)]
    )
    comment = models.TextField(blank=True, null=True)

    class Meta:
        unique_together = ('user', 'anime')

    def __str__(self):
        return f"{self.user.username} — {self.anime.title}"


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    anime = models.ForeignKey(Anime, on_delete=models.CASCADE, related_name='reviews')
    title = models.CharField(max_length=200)
    content = models.TextField()
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)]
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'anime')
        ordering = ['-created_at']
        verbose_name = 'Recensione'
        verbose_name_plural = 'Recensioni'

    def __str__(self):
        return f"{self.user.username} su {self.anime.title} — {self.rating}/10"
