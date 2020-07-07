import datetime

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import permission_required
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from .models import Book, BookInstance, Author, Genre
from .forms import RenewBookForm


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


# Challenge yourself (1)
class AuthorListView(generic.ListView):
	model = Author
	context_object_name = 'author_list'
	paginate_by = 10


# Challenge yourself (2)
class AuthorDetailView(generic.DetailView):
	model = Author
	context_object_name = 'author'

	def get_context_data(self, **kwargs):
		context = super(AuthorDetailView, self).get_context_data(**kwargs)
		context ['author_books'] = Book.objects.filter(author=self.kwargs['pk'])
		return context


class LoanedBooksByUserListView(LoginRequiredMixin, generic.ListView):
	"""Generic class-based view listing books on loan to current user."""
	model = BookInstance
	template_name = 'catalog/bookinstance_list_borrowed_user.html'
	paginate_by = 10

	def get_queryset(self):
		return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')


class AllLoanedBooksListView(PermissionRequiredMixin, generic.ListView):
	permission_required = 'catalog.can_mark_returned'
	model = BookInstance
	template_name = 'catalog/bookinstance_list_all_borrowed_book.html'
	paginate_by = 10

	def get_queryset(self):
		return BookInstance.objects.filter(status__exact='o').order_by('due_back')
		

@permission_required('catalog.can_mark_returned')
def renew_book_librarian(request, pk):
	book_instance = get_object_or_404(BookInstance, pk=pk)

	# If this is a POST request then process the Form data
	if request.method == 'POST':

		# Create a form instance and populate it with data from the request (binding):
		form = RenewBookForm(request.POST)

		# Check if the form is valid:
		if form.is_valid():
			# process the data in form.cleaned_data as required (here we just write it to the model due_back field)
			book_instance.due_back = form.cleaned_data['renewal_date']
			book_instance.save()

			# redirect to a new URL:
			return HttpResponseRedirect(reverse('all-borrowed'))

	# if this is a GET (or any other method) create the default form.
	else:
		proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
		form = RenewBookForm(initial={'renewal_date': proposed_renewal_date})

	context = {
		'form': form,
		'book_instance': book_instance,
	}

	return render(request, 'catalog/book_renew_librarian.html', context)


class AuthorCreate(PermissionRequiredMixin, CreateView):
	permission_required = 'catalog.can_mark_returned'
	model = Author
	fields = '__all__'
	initial = {'date_of_death': '05/01/2018'}


class AuthorUpdate(PermissionRequiredMixin, UpdateView):
	permission_required = 'catalog.can_mark_returned'
	model = Author
	fields = ['first_name', 'last_name', 'date_of_birth', 'date_of_death']


class AuthorDelete(PermissionRequiredMixin, DeleteView):
	permission_required = 'catalog.can_mark_returned'
	model = Author
	success_url = reverse_lazy('authors')


# Challenge yourself
class BookCreate(PermissionRequiredMixin, CreateView):
	permission_required = 'catalog.can_mark_returned'
	model = Book
	fields = '__all__'


class BookUpdate(PermissionRequiredMixin, UpdateView):
	permission_required = 'catalog.can_mark_returned'
	model = Book
	fields = ['title', 'author', 'summary', 'isbn', 'genre', 'language']


class BookDelete(PermissionRequiredMixin, DeleteView):
	permission_required = 'catalog.can_mark_returned'
	model = Book
	success_url = reverse_lazy('books')
