from django.urls import path

from . import views


app_name = 'core'
urlpatterns = [
    path('authors/', views.authors, name='list-authors'),
    path('books/', views.book_list_create, name='create-book'),
    path('books/<int:pk>/', views.book_read_update_delete, name='read-update-delete-book'),
    path('books/export/', views.export_csv, name='export')
]
