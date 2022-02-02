import datetime

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Avg, Count
from django.db.models.functions import Round
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse_lazy
from django.views import generic

from tasks import celery_send_mail

from hw_11.models import Author, Book, Publisher, Store
from hw_11.forms import CeleryForm


def home(request):
    return render(request, 'home.html')


class AuthorListView(generic.ListView):
    template_name = 'author_list.html'
    queryset = Author.objects.all().prefetch_related('book_set').annotate(books_count=Count('book'))
    paginate_by = 25


class AuthorDetailView(generic.DetailView):
    queryset = Author.objects.prefetch_related('book_set').annotate(average_rating=Round(Avg('book__rating')))


class AuthorCreateView(LoginRequiredMixin, SuccessMessageMixin, generic.CreateView):
    model = Author
    template_name = 'author_form.html'
    fields = '__all__'
    success_message = 'Author successfully created'
    success_url = reverse_lazy('author-list')
    login_url = '/admin/'


class AuthorUpdateView(LoginRequiredMixin, SuccessMessageMixin, generic.UpdateView):
    model = Author
    template_name = 'author_form.html'
    fields = '__all__'
    success_message = 'Author successfully updated'
    success_url = reverse_lazy('author-list')
    login_url = '/admin/'


class AuthorDeleteView(LoginRequiredMixin, SuccessMessageMixin, generic.DeleteView):
    model = Author
    template_name = 'author_confirm_delete.html'
    success_message = 'Author successfully deleted'
    success_url = reverse_lazy('author-list')
    login_url = '/admin/'


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


def celery(request):
    if request.method == "POST":
        form = CeleryForm(request.POST)
        if form.is_valid():
            question = form.cleaned_data['question']
            email = form.cleaned_data['email']
            reminder_date = form.cleaned_data['reminder_date']
            celery_send_mail.apply_async((question, email), eta=reminder_date)
            messages.success(request, 'Remind is created')
            print(datetime.datetime.utcnow(), '|||||||', reminder_date)
            return redirect('/')
    else:
        form = CeleryForm(initial={
            'reminder_date': f'{(datetime.datetime.now() + datetime.timedelta(hours=2)).strftime("%Y-%m-%d %H:%M:%S")}'
        })
    return render(request, 'celery.html', {'form': form})








