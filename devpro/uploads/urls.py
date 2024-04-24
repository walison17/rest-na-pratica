from django.urls import path

from . import views

app_name = 'uploads'
urlpatterns = [
    path('uploads', views.create_upload, name='create_upload'),
    path('uploads/<int:upload_id>', views.get_upload),
]
