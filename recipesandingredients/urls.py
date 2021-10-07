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
    path('download', views.download_ingredients, name='download_ing'),
    path('downloadrecipies', views.download_recipes, name='download_recipe'),
    path('delete-ing/<int:ing_id>', views.delete_ingredient, name='delete_ing'),
    path('delete-recipe/<int:rec_id>', views.delete_recipe, name='delete_rec'),
    path('suppliers', views.suppliers_dashboard, name='suppliers_dashboard'),
    path('suppliers/new', views.create_supplier, name='new_supplier'),
    path('suppliers/info/<int:supplier_id>', views.each_supplier_info),
    path('suppliers/edit/<int:supplier_id>', views.edit_supplier),
    path('suppliers/delete/<int:supplier_id>', views.delete_supplier),
    path('download/suppliers', views.download_suppliers, name='download_suppliers'),
    path('listcategories', views.category_dashboard, name='category_dashboard'),
    path('delete-cat/<int:cat_id>', views.delete_category),
    path('handle_measurements', views.handle_measurement),
    path('storagearea/new', views.crate_storage_area, name='create_storage'),
    path('storagearea/edit/<int:storage_area_id>', views.edit_storage_area)
]
