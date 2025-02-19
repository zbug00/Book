from django.urls import path
from .views import *

urlpatterns = [
    path('quotes/<int:pk>/', get_quote, name='quote-detail'),
]