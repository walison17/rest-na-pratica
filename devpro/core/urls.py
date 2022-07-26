from django.urls import path

from . import views


app_name = 'core'
urlpatterns = [
    path('authors/', views.authors, name='list-authors')
]
