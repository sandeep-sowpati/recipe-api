"""
URL's for the recipe API
"""
from django.urls import path

from recipe import views


app_name = 'recipe'

urlpatterns = [
    path(
        'recipelist/',
        views.RetrieveRecipeView.as_view({'get': 'list'}),
        name='recipelist'
    ),
]
