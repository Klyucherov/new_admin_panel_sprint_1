import uuid

from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _


class TimeStampedMixin(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class UUIDMixin(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


class Filmwork(UUIDMixin, TimeStampedMixin):
    title = models.CharField(_('title'), max_length=255)
    description = models.TextField(_('description'), blank=True, null=True)
    creation_date = models.DateField(_('creation_date'), blank=True, null=True)
    file_path = models.CharField(_('file_path'), max_length=255, blank=True, null=True)
    rating = models.FloatField(_('rating'),
                               blank=True, null=True,
                               validators=[MinValueValidator(0),
                                           MaxValueValidator(100)])

    class Status(models.TextChoices):
        MOVIE = 'movie', _('movie')
        TV_SHOW = 'tv_show', _('tv_show')

    type = models.CharField(
        _('type'),
        max_length=100,
        choices=Status.choices,
        default=Status.MOVIE,
    )

    genres = models.ManyToManyField('Genre',
                                    through='GenreFilmwork',
                                    verbose_name=_('genres'),
                                    related_name='films')

    persons = models.ManyToManyField('Person',
                                     through='PersonFilmwork',
                                     verbose_name=_('persons'),
                                     related_name='films')

    class Meta:
        db_table = "content\".\"film_work"
        verbose_name = _('Filmwork')
        verbose_name_plural = _('Filmworks')
        indexes = [
            models.Index(fields=['title']),
            models.Index(fields=['creation_date', 'rating']),
        ]

    def __str__(self):
        return self.title


class Genre(UUIDMixin, TimeStampedMixin):
    name = models.CharField(_('name'), max_length=255)
    description = models.TextField(_('description'), blank=True, null=True)

    class Meta:
        db_table = "content\".\"genre"
        verbose_name = _('Genre')
        verbose_name_plural = _('Genres')

    def __str__(self):
        return self.name


class Person(UUIDMixin, TimeStampedMixin):
    full_name = models.CharField(_('full_name'), max_length=255)

    class Meta:
        db_table = "content\".\"person"
        verbose_name = _('Person')
        verbose_name_plural = _('Persons')

    def __str__(self):
        return self.full_name


class GenreFilmwork(UUIDMixin):
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    film_work = models.ForeignKey(Filmwork, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "content\".\"genre_film_work"
        verbose_name = _('GenreFilmwork')
        verbose_name_plural = _('GenreFilmworks')
        constraints = [
            models.UniqueConstraint(
                fields=['film_work', 'genre'],
                name='genre_film_work_unique_idx',
            ),
        ]
        indexes = [
            models.Index(fields=['film_work']),
            models.Index(fields=['genre']),
        ]


class PersonFilmwork(UUIDMixin):
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    film_work = models.ForeignKey(Filmwork, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    class Roles(models.TextChoices):
        ACTOR = 'actor', _('actor')
        DIRECTOR = 'director', _('director')
        WRITER = 'writer', _('writer')

    role = models.CharField(
        _('role'),
        max_length=100,
        choices=Roles.choices,
        default=Roles.ACTOR,
    )

    class Meta:
        db_table = "content\".\"person_film_work"
        verbose_name = _('PersonFilmwork')
        verbose_name_plural = _('PersonFilmwork')
        constraints = [
            models.UniqueConstraint(
                fields=['film_work', 'person', 'role'],
                name='film_work_person_idx',
            ),
        ]
        indexes = [
            models.Index(fields=['film_work']),
            models.Index(fields=['person']),
        ]
