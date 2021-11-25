from django.contrib import admin
from .models import Ingredients, RecipesModel, IngredientData

admin.site.register(Ingredients)
admin.site.register(RecipesModel)
admin.site.register(IngredientData)
