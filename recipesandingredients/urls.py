from django.urls import path
from . import views

urlpatterns = [
    path('new', views.handleIngredients, name='ingredients'),
    path('page', views.ingredientsDashboard, name='ingredientdashboard'),
]
