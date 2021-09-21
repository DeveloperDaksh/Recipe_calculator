from django.urls import path
from . import views

urlpatterns = [
    path('new', views.handleIngredients, name='ingredients'),
    path('page', views.ingredientsDashboard, name='ingredientdashboard'),
    path('recipelist', views.recipeDashboard, name='recipedashboard'),
    path('newrecipe', views.handleRecipes, name='recipes'),
    path('details/<int:ing_id>', views.recipe_detail, name='recipe_detail'),
    path('edit/<int:ing_id>', views.edit_recipe, name='edit_recipe'),
    path('editing/<int:ing_id>', views.edit_ingredient, name='edit_recipe'),
    path('ingridientdetails/<int:ing_id>', views.ingredient_details, name='ingredient_details'),
]
