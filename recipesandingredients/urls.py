from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
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
    path('storagearea/edit/<int:storage_area_id>', views.edit_storage_area),
    path('uploadimage/<int:ing_id>', views.ingredient_images),
    path('deleteimage/<int:img_id>', views.delete_ingredient_image),
    path('replaceingredients/<int:ing_id>', views.replace_ingredient),
    path('confirm_replace/<int:from_id>/<int:to_id>', views.confirm_replace),
    path('edit_nutrition_details/<int:ing_id>', views.edit_nutrition_details),
    path('preparation/<int:recipe_id>', views.recipe_preparation_instructions),
    path('ingridientdetails/addsupplier/<int:ing_id>', views.add_ingredient_supplier),
    path('edit_ingredient_suppliers/<int:ing_id>', views.edit_ingredient_suppliers),
    path('edit_ingredient_supplier/edit/<int:ing_id>/<int:ing_supplier_id>', views.edit_each_ingredient_supplier),
    path('edit_ingredient_supplier/delete/<int:ing_id>/<int:ing_supplier_id>', views.delete_each_ingredient_supplier),
    path('preferred/<int:ing_id>/<int:ing_supplier_id>', views.set_preferred_ingredient_supplier),
    path('allergens/<int:rec_id>', views.allergen_recipes),
    path('images/<int:rec_id>', views.recipe_images),
    path('deleterecipeimage/<int:img_id>', views.delete_recipe_image)
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
