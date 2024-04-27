
from django.urls import path 
from . import views
from .views import get_book_copies_for_book, get_books_for_library


urlpatterns = [
    path('', views.home, name = "home"),
    path('join', views.join, name = "join"),
    path('add', views.add, name = "add"),
    path('delete', views.delete, name = "delete"),
    path('update', views.update, name = "update"),
    path('report', views.report, name = "report"),
    path('get-books/<int:library_id>/', get_books_for_library, name='get_books_for_library'),
    path('get-book-copies/<int:book_id>/<int:library_id>/', views.get_book_copies_for_book, name='get_book_copies_for_book'),
]
