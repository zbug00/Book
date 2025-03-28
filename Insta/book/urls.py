from django.urls import path
from .views import *

urlpatterns = [
    path('quotes/', create_quote, name='quote-detail'),
]