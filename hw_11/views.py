from django.db.models import Avg, Count
from django.db.models.functions import Round
from django.shortcuts import get_object_or_404, render

from hw_11.models import Author, Book, Publisher, Store


def home(request):
    return render(request, 'home.html')


def authors(request):
    author_list = Author.objects.all().prefetch_related('book_set').annotate(books_count=Count('book'))
    return render(request, 'authors_list.html', {'author_list': author_list})


def authors_info(request, pk):
    author_info = get_object_or_404(Author.objects.prefetch_related
                                    ('book_set').annotate(average_rating=Round(Avg('book__rating'))), pk=pk)
    return render(request, 'author_info.html', {'author_info': author_info})


def books(request):
    book_list = Book.objects.all()
    return render(request, 'book_list.html', {'book_list': book_list})


def book_info(request, pk):
    books_info = get_object_or_404(Book, pk=pk)
    return render(request, 'books_info.html', {'books_info': books_info})


def publishers(request):
    publisher_list = Publisher.objects.all().prefetch_related('book_set').annotate(books_count=Count('book'))
    return render(request, 'publisher.html', {'publisher_list': publisher_list})


def publisher_info(request, pk):
    publishers_info = get_object_or_404(Publisher.objects.all()
                                        .prefetch_related('book_set').annotate(books_count=Count('book')), pk=pk)
    return render(request, 'publisher_info.html', {'publishers_info': publishers_info})


def store(request):
    store_list = Store.objects.all().prefetch_related('books').annotate(books_count=Count('books'))
    return render(request, 'store_list.html', {'store_list': store_list})


def store_info(request, pk):
    stores_info = get_object_or_404(Store.objects.all().prefetch_related('books'), pk=pk)
    return render(request, "store_info.html", {'stores_info': stores_info})
