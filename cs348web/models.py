from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Library(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    isbn = models.CharField(max_length=13, unique=True)
    publish_year = models.IntegerField()
    genre = models.CharField(max_length=100)


    def __str__(self):
        return f"{self.title} by {self.author}"
    class Meta:
        indexes = [
            models.Index(fields=['title']),
            models.Index(fields=['author']),
        ]

class BookCopy(models.Model):
    STATUS_CHOICES = [
        ('available', 'Available'),
        ('borrowed', 'Borrowed'),
        ('maintenance', 'Maintenance'),
    ]
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    library = models.ForeignKey(Library, on_delete=models.CASCADE)
    status = models.CharField(max_length=11, choices=STATUS_CHOICES, default='available')

    def __str__(self):
        return f"{self.book.title} - {self.status} at {self.library.name}"
    class Meta:
        indexes = [
            models.Index(fields=['status']),
        ]
        db_table = 'library_bookcopy'

class BorrowingRecord(models.Model):
    book_copy = models.ForeignKey(BookCopy, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    borrow_date = models.DateField()
    return_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} borrowed {self.book_copy.book.title}"