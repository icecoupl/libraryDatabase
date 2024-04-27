from django.contrib import admin
from .models import Library, Book, BookCopy, BorrowingRecord

admin.site.register(Library)
admin.site.register(Book)
admin.site.register(BookCopy)
admin.site.register(BorrowingRecord)