# urls.py

from django.urls import path
from . import views  # Make sure to import your views

urlpatterns = [
    path('upload_image/', views.upload_image, name='upload_image'),  # Map URL to the view
]
