from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import *


class GenreFilmworkInline(admin.TabularInline):
    model = GenreFilmwork
    autocomplete_fields = ('genre', 'film_work')


class PersonFilmworkInline(admin.TabularInline):
    model = PersonFilmwork
    autocomplete_fields = ('person', 'film_work')


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_filter = ('name',)
    search_fields = ('name', 'description', 'id')

    list_display = (
        'name',
        'description',
        'created',
        'modified',
    )

    class Meta:
        model = Genre


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_filter = ('full_name',)
    search_fields = ('full_name',)

    list_display = (
        'full_name',
        'created',
        'modified',
    )

    class Meta:
        model = Person


@admin.register(Filmwork)
class FilmworkAdmin(admin.ModelAdmin):
    inlines = [GenreFilmworkInline, PersonFilmworkInline]

    list_filter = ('type',)
    search_fields = ('title', 'description', 'id')

    list_display = (
        'title',
        'creation_date',
        'file_path',
        'rating',
        'type',
        'created',
        'modified',
        'get_genres',
    )

    list_prefetch_related = ('genres', 'persons')

    def get_queryset(self, request):
        queryset = (
            super()
            .get_queryset(request)
            .prefetch_related(*self.list_prefetch_related)
        )
        return queryset

    def get_genres(self, obj):
        return ','.join([genre.name for genre in obj.genres.all()])

    get_genres.short_description = _('Genres of the film')

    class Meta:
        model = Filmwork
