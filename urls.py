""" urlpatterns for this application."""
from django.urls import path
from . import views

app_name = "sentence_finder"
urlpatterns = [
path('', views.index, name="find")
]