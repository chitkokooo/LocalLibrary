from django.contrib import admin
from .models import Author, Genre, Book, BookInstance

admin.site.register(Genre)


class BooksInstanceInline(admin.TabularInline):
	model = BookInstance


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
	list_display = ('title', 'author', 'display_genre')
	# list_search = ('title', 'isbn')
	filter_display = ('author')
	inlines = [BooksInstanceInline]


@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
	list_filter = ('status', 'due_back')

	# Challenge - yourself (1)
	list_display = ('book', 'status', 'borrower', 'due_back', 'id')

	fieldsets = (
		(None, {
			'fields': ('book', 'imprint', 'id')
		}),
		('Availability', {
			'fields': ('status', 'due_back', 'borrower')
		}),
	)

# Challenge youself (2.1)
class BookInline(admin.TabularInline):
	model = Book


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
	list_display = ('last_name', 'first_name', 'date_of_birth', 'date_of_death')
	fields = ['first_name', 'last_name', ('date_of_birth', 'date_of_death')]
	inlines = [BookInline]  # Challenge yourself (2.2)
