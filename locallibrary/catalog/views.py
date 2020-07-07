from django.shortcuts import render
from django.views import generic
from .models import Book, BookInstance, Author, Genre


def index(request):
	"""View function for home page of site."""

	# Generate counts of some of the main ojbects
	num_books = Book.objects.all().count()
	num_instances = BookInstance.objects.all().count()

	# Available books (status = 'a')
	num_instances_available = BookInstance.objects.filter(status__exact='a').count()

	# The 'all()' is implied by default.
	num_authors = Author.objects.count()

	# Number of visits to this view, as counted in the session variable.
	num_visits = request.session.get('num_visits', 0)
	request.session['num_visits'] = num_visits + 1

	# Challenge yourself (2.1)
	num_genre = Genre.objects.count()
	grammer_books = Book.objects.filter(title__icontains='grammer').count()

	context = {
		'num_books': num_books,
		'num_instances': num_instances,
		'num_instances_available': num_instances_available,
		'num_authors': num_authors,
		'num_visits': num_visits,

		# Challenge yourself (2.2)
		'num_genre': num_genre,
		'grammer_books': grammer_books,
	}

	# Render the HTML template index.html with the data in the context variable
	return render(request, 'index.html', context=context)


class BookListView(generic.ListView):
	model = Book
	context_object_name = 'book_list'  # your own name for the list as a template variable
	# queryset = Book.objects.filter(title__icontains='war')[:5] 	# Get 5 books containing the title war
	# template_name = 'books/my_arbitary_template_name_list.html'  # Specify your own template name/location
	paginate_by = 10

	def get_queryset(self):
		return Book.objects.all()
		# return Book.objects.filter(title__icontains='war')[:5]  # Get 5 books containing the title war

	"""def get_context_data(self, **kwargs):
					# Call the base implementation first to get the context
					context = super(BookListView, self).get_context_data(**kwargs)
					# Create any data and add it to the context
					context['some_data'] = 'This is just some data'
					return context"""


class BookDetailView(generic.DetailView):
	model = Book


class AuthorListView(generic.ListView):
	model = Author
	context_object_name = 'author_list'
	paginate_by = 10


class AuthorDetailView(generic.DetailView):
	model = Author
	context_object_name = 'author'

	def get_context_data(self, **kwargs):
		context = super(AuthorDetailView, self).get_context_data(**kwargs)
		context ['author_books'] = Book.objects.filter(author=self.kwargs['pk'])
		return context