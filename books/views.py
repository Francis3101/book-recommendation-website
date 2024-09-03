import random
from django.shortcuts import render, get_object_or_404
from .models import Book
from .recommendation import get_recommendations
from django.db.models import Q

def home(request):
    all_books = list(Book.objects.all())
    featured_books = random.sample(all_books, min(len(all_books), 10))  # Randomly select up to 10 books
    return render(request, 'books/home.html', {'featured_books': featured_books})

def book_detail(request, book_id):
    book = get_object_or_404(Book, book_id=book_id)
    recommendations = get_recommendations(book.title)
    return render(request, 'books/book_detail.html', {'book': book, 'recommendations': recommendations})

def search_books(request):
    query = request.GET.get('q', '')
    genre = request.GET.get('genre', '')
    author = request.GET.get('author', '')
    pub_year = request.GET.get('pub_year', '')

    books = Book.objects.all()

    if query:
        books = books.filter(Q(title__icontains=query) | Q(description__icontains=query))
    if genre:
        books = books.filter(genre__icontains=genre)
    if author:
        books = books.filter(author__icontains=author)
    if pub_year:
        books = books.filter(pub_year=pub_year)

    return render(request, 'books/search_results.html', {'books': books, 'query': query, 'genre': genre, 'author': author, 'pub_year': pub_year})