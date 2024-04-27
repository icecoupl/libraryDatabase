from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Library, Book, BookCopy, BorrowingRecord
from django.http import JsonResponse
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.db import connection
from django.db import transaction

# Create your views here.
def home(request):
    all_books = Book.objects.all
    return render(request, 'home.html', {'all': all_books} )

def report(request):
    all_books = Book.objects.all
    return render(request, 'report.html', {'all': all_books} )

def join(request):
    return render(request, 'join.html', {} )

@transaction.atomic
def add(request):
    if request.method == "POST":
        library_id = request.POST.get('library_id')
        book_id = request.POST.get('book_id')

        # Raw SQL to insert a new BookCopy
        with connection.cursor() as cursor:
            sql = """
            INSERT INTO library_bookcopy (book_id, library_id, status)
            VALUES (%s, %s, %s)
            """
            # Default status for new book copies
            status = 'available'
            cursor.execute(sql, [book_id, library_id, status])

        messages.success(request, 'Book copy added successfully!')
        return redirect('add')
    else:
        # Fetch libraries and books to populate the form options
        libraries = Library.objects.all()
        books = Book.objects.all()
        return render(request, 'add.html', {'libraries': libraries, 'books': books})
    
@transaction.atomic
def delete(request):
    if request.method == 'POST':
        book_copy_id = request.POST.get('book_copy_id')
        if book_copy_id:
            with connection.cursor() as cursor:
                sql = "DELETE FROM library_bookcopy WHERE id = %s"
                cursor.execute(sql, [book_copy_id])
            messages.success(request, "Book copy deleted successfully.")
        else:
            messages.error(request, "No book copy selected.")
        return HttpResponseRedirect(reverse('delete'))
    else:
        libraries = Library.objects.all()
        return render(request, 'delete.html', {'libraries': libraries})

@transaction.atomic
def update(request):
    if request.method == "POST":
        book_copy_id = request.POST.get('book_copy_id')
        new_status = request.POST.get('status')
        if book_copy_id and new_status:
            with connection.cursor() as cursor:
                sql = "UPDATE library_bookcopy SET status = %s WHERE id = %s"
                cursor.execute(sql, [new_status, book_copy_id])
            messages.success(request, "Book copy status updated successfully.")
        else:
            messages.error(request, "Invalid input or book copy not found.")
        return redirect('update')
    else:
        libraries = Library.objects.all()
        return render(request, 'update.html', {'libraries': libraries})

# View with prepared statement
@transaction.atomic
def report(request):
    author = request.GET.get('author', '')
    title = request.GET.get('title', '')
    books = None
    if author or title:
        with connection.cursor() as cursor:
            sql = """
            SELECT DISTINCT b.id, b.title, b.author, b.isbn, b.publish_year, b.genre, l.name
            FROM cs348web_book b
            INNER JOIN library_bookcopy bc ON b.id = bc.book_id
            INNER JOIN cs348web_library l ON bc.library_id = l.id
            WHERE bc.status = 'available'
            AND b.author LIKE %s
            AND b.title LIKE %s
            ORDER BY b.title, b.author, l.name
            """
            cursor.execute(sql, ['%' + author + '%', '%' + title + '%'])
            rows = cursor.fetchall()
            books = [{'id': row[0], 'title': row[1], 'author': row[2], 'isbn': row[3],
                      'publish_year': row[4], 'genre': row[5], 'library_name': row[6]}
                     for row in rows]
    return render(request, 'report.html', {'books': books})

def search_books(request):
    author = request.GET.get('author', '')
    title = request.GET.get('title', '')
    books = Book.objects.filter(author__icontains=author, title__icontains=title, bookcopy__status='available').distinct()
    return render(request, 'report.html', {'books': books})




def get_books_for_library(request, library_id):
    books = Book.objects.filter(bookcopy__library_id=library_id).distinct().values('id', 'title')
    return JsonResponse({"books": list(books)})


# In your_app/views.py
def get_book_copies_for_book(request, book_id, library_id):
    # Assuming BookCopy model has both 'book' and 'library' fields
    book_copies = BookCopy.objects.filter(book_id=book_id, library__id=library_id).values('id', 'status')
    return JsonResponse({"book_copies": list(book_copies)})




