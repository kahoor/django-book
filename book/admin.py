from django.contrib import admin

from .models import Book
from .models import BookInstance
from .models import Author
from .models import Ganre
# Register your models here.

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'date_of_birth', 'date_of_death']

    fields = [
        'first_name',
        'last_name',
        ('date_of_birth', 'date_of_death')
    ]


class BookInstanceInline(admin.TabularInline):
    model = BookInstance


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'isbn', 'author','display_ganre']
    inlines = [BookInstanceInline]

    def display_ganre(self, obj):
        return ', '.join([ganre.name for ganre in obj.ganre.all()[:3]])

    display_ganre.short_description = 'ganre'


@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
    list_display = ['book', 'status', 'borrower', 'due_back']
    list_filter = ['status', 'due_back']

    fieldsets = (
        (None, {
            "fields": (
                'book',
                'imprint'
            ),
        }),
        ('Availablity',{
            "fields": (
                'status',
                'due_back',
                'borrower'
            )
        })
    )
    