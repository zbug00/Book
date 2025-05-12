from django.urls import path
from .views import *

urlpatterns = [
    path('new_quote/', create_quote, name='create-quote'),
    path('quotes/<int:pk>/', get_quote, name='get/update/delete'),
    path('quotes/', list_quotes, name='list-quotes'),
    path('categories/', list_categories, name='list-categories'),
    path('tags/', list_tags, name='list-tags'),
    path('data/', get_all_data, name='get-all-data'),

]