import json

from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, redirect
from django.http import HttpResponse
from wsgiref.util import FileWrapper
import io
import csv
import openpyxl

from recipeapp.models import UserModel
from company.models import Company

from .forms import IngredientsForm, RecipeForm, SuppliersForm, UpdateSupplier, StorageAreaForm, NutritionDetailsForm, \
    RecipePreparationInstructions, Ingredient_SupplierForm, UpdateIngredientSupplierForm,ProductionPlanTemplateForm,ProductionPlanForm
from .models import Ingredients, RecipesModel, IngredientData, Suppliers, IngredientCategories, StorageAreas, \
    IngredientImages, NutritionDetails, IngredientSuppliers,RecipeImages,ProductionPlanTemplate,ProductionPlan,Recipes
from .units import qty_units


@login_required(login_url='/login')
def handleIngredients(request):
    user = UserModel.objects.get(username=request.user)
    company_details = Company.objects.filter(user=request.user)
    if company_details.count() > 1:
        many_companies = True
    else:
        many_companies = False
    company_name = request.session['company_name']
    if request.method == 'POST':
        print(request.POST)
        form = IngredientsForm(request=request, data=request.POST)
        print(form.is_valid())
        ingMeasurementsData = request.POST.get('ingMeasurementsData')
        print(ingMeasurementsData)
        if form.is_valid():
            ingname = form.cleaned_data['name']
            try:
                Ingredients.objects.get(Q(name=ingname) & Q(username=request.user) & Q(company_name=company_name))
                return render(
                    request,
                    'add_ingredients.html',
                    {
                        'form': form,
                        'fail': 'Name Already Exists',
                        'username': user.username,
                        'email': user.email,
                        'first_name': user.first_name,
                        'last_name': user.last_name,
                        'many_companies': many_companies,
                        'company_details': company_details,
                        'company_name': company_name
                    }
                )
            except Ingredients.DoesNotExist:
                ingredientsdata = form.save(commit=False)
                ingredientsdata.username = request.user
                ingredientsdata.company_name = company_name
                ingredientsdata.save()
                print("Saved")
                indredients = Ingredients.objects.get(username=request.user, name=form.cleaned_data['name'],
                                                      company_name=company_name)
                indredients.nutriationData = request.POST.get('nutri-data-link-value')
                indredients.fdcId = request.POST.get('nutri-data-fdcid')
                indredients.save()
                if form.cleaned_data['suppliers'] == 'Add Supplier':
                    indredients.suppliers = request.POST.get('customsupplier')
                    indredients.save()
                    Suppliers.objects.create(supplier_name=request.POST.get('customsupplier'),
                                             user=request.user.username, company_name=company_name).save()
                    IngredientSuppliers.objects.create(ingredient_relation=indredients,
                                                       supplier=request.POST.get('customsupplier'),
                                                       price=form.cleaned_data['price'],
                                                       order_code=form.cleaned_data['orderCode'],
                                                       caseQuantity=form.cleaned_data['caseQuantity'],
                                                       packSize=form.cleaned_data['packSize'],
                                                       qtyUnits=form.cleaned_data['qtyUnits'], preferred=True).save()
                if form.cleaned_data['suppliers'] != 'Add Supplier' and form.cleaned_data['suppliers'] != '':
                    IngredientSuppliers.objects.create(ingredient_relation=indredients,
                                                       supplier=form.cleaned_data['suppliers'],
                                                       price=form.cleaned_data['price'],
                                                       order_code=form.cleaned_data['orderCode'],
                                                       caseQuantity=form.cleaned_data['caseQuantity'],
                                                       packSize=form.cleaned_data['packSize'],
                                                       qtyUnits=form.cleaned_data['qtyUnits'], preferred=True).save()
                if form.cleaned_data['category'] == 'Add Category':
                    indredients.category = request.POST.get('customcategory')
                    indredients.save()
                    IngredientCategories.objects.create(user=request.user.username, company_name=company_name,
                                                        category=request.POST.get('customcategory'),
                                                        category_type='ingredient').save()
                if ingMeasurementsData == '':
                    pass
                else:
                    ingdata = ingMeasurementsData.split(';')
                    fromdata = ingdata[0].split(',')
                    todata = ingdata[1].split(',')
                    fromunits = ingdata[2].split(',')
                    tounits = ingdata[3].split(',')
                    indredients.fromMeasurementUnits = fromunits[:-1]
                    indredients.fromMeasurementData = fromdata[:-1]
                    indredients.toMeasurementUnits = tounits[:-1]
                    indredients.toMeasurementData = todata[:-1]
                    indredients.save()
                    print("Ingredients Saved")
                return redirect('/recipe/page')
        else:
            return render(
                request,
                'add_ingredients.html',
                {
                    'form': form,
                    'username': user.username,
                    'email': user.email,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'many_companies': many_companies,
                    'company_details': company_details,
                    'company_name': company_name
                }
            )
    else:
        form = IngredientsForm(request=request)
        return render(
            request,
            'add_ingredients.html',
            {
                'username': user.username,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'form': form,
                'many_companies': many_companies,
                'company_details': company_details,
                'company_name': company_name
            }
        )


@login_required(login_url='/login')
def ingredientsDashboard(request):
    user = UserModel.objects.get(username=request.user)
    company_name = request.session['company_name']
    company_details = Company.objects.filter(user=request.user)
    if company_details.count() > 1:
        many_companies = True
    else:
        many_companies = False
    ingridients = Ingredients.objects.filter(username=request.user, company_name=company_name)
    ingredient_categories = IngredientCategories.objects.filter(user=request.user.username, company_name=company_name,
                                                                category_type='ingredient')
    return render(
        request,
        'ingredients_dashboard.html',
        {
            'ingridients': ingridients,
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'many_companies': many_companies,
            'company_details': company_details,
            'company_name': company_name,
            'ingredient_categories': ingredient_categories,
            'qty_units': qty_units
        }
    )


@login_required(login_url='/login')
def recipeDashboard(request):
    user = UserModel.objects.get(username=request.user)
    company_details = Company.objects.filter(user=request.user)
    if company_details.count() > 1:
        many_companies = True
    else:
        many_companies = False
    company_name = request.session['company_name']
    recipies = RecipesModel.objects.filter(recipe_user=str(request.user), company_name=company_name)
    recipe_categories = IngredientCategories.objects.filter(user=request.user.username, company_name=company_name,
                                                            category_type='recipe')
    return render(
        request,
        'recipe_dashboard.html',
        {
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'recipies': recipies,
            'many_companies': many_companies,
            'company_details': company_details,
            'company_name': company_name,
            'recipe_categories': recipe_categories
        }
    )


@login_required(login_url='/login')
def handleRecipes(request):
    user = UserModel.objects.get(username=request.user)
    company_details = Company.objects.filter(user=request.user)
    if company_details.count() > 1:
        many_companies = True
    else:
        many_companies = False
    company_name = request.session['company_name']
    ingredients = Ingredients.objects.filter(username=request.user, company_name=company_name)
    if request.method == 'POST':
        form = RecipeForm(request=request, data=request.POST)
        if form.is_valid():
            try:
                check_recipe = RecipesModel.objects.get(recipe_user=request.user.username,
                                                        recipe_name=form.cleaned_data['recipe_name'],
                                                        company_name=company_name)
                form = RecipeForm(request=request)
                return render(
                    request,
                    'add_recipe.html',
                    {
                        'fail': 'Recipe Name Already Exists',
                        'username': user.username,
                        'email': user.email,
                        'first_name': user.first_name,
                        'last_name': user.last_name,
                        'form': form,
                        'many_companies': many_companies,
                        'company_details': company_details,
                        'company_name': company_name
                    }
                )
            except RecipesModel.DoesNotExist:
                if 'ingAmount' not in request.POST:
                    recipe = form.save(commit=False)
                    recipe.recipe_user = request.user.username
                    recipe.company_name = company_name
                    recipe.save()
                    return redirect('/recipe/details/' + str(recipe.id))
                else:
                    recipe = form.save(commit=False)
                    recipe.recipe_user = request.user.username
                    recipe.company_name = company_name
                    recipe.save()
                    recipedetails = RecipesModel.objects.get(recipe_user=str(request.user),
                                                             recipe_name=form.cleaned_data['recipe_name'],
                                                             company_name=company_name)
                    for i in range(len(request.POST.getlist('ingAmount'))):
                        ingredient = IngredientData.objects.create(
                            ing_name=request.POST.getlist('ingridientName')[i],
                            ing_amount=request.POST.getlist('ingAmount')[i],
                            ing_units=request.POST.getlist('ingUnits')[i],
                            ing_description=request.POST.getlist('ingDescription')[i]
                        )
                        recipe.other_ing_data.add(ingredient)
                    return redirect('/recipe/details/' + str(recipe.id))

    else:
        form = RecipeForm(request=request)
        return render(
            request,
            'add_recipe.html',
            {
                'username': user.username,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'form': form,
                'ingredients': ingredients,
                'many_companies': many_companies,
                'company_details': company_details,
                'company_name': company_name
            }
        )


@login_required(login_url='/login')
def recipe_detail(request, ing_id):
    user = UserModel.objects.get(username=request.user)
    company_details = Company.objects.filter(user=request.user)
    if company_details.count() > 1:
        many_companies = True
    else:
        many_companies = False
    company_name = request.session['company_name']
    recipe = RecipesModel.objects.get(id=ing_id)
    return render(
        request,
        'each_recipe_detail.html',
        {
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'recipe': recipe,
            'many_companies': many_companies,
            'company_details': company_details,
            'company_name': company_name
        }
    )


@login_required(login_url='/login')
def edit_recipe(request, ing_id):
    user = UserModel.objects.get(username=request.user)
    company_details = Company.objects.filter(user=request.user)
    if company_details.count() > 1:
        many_companies = True
    else:
        many_companies = False
    company_name = request.session['company_name']
    recipe = RecipesModel.objects.get(id=ing_id)
    ingredients = Ingredients.objects.filter(username=request.user, company_name=company_name)
    other_ing = []
    unit_options = ['Milliliter (ml)', 'US Teaspoon (tsp) (4.93 ml)', 'US Tablespoon (tbsp) (14.79 ml)',
                    'Fluid-ounce (floz) (29.57 ml)', 'Deciliter (dL) (100 ml)', 'US Cup (cup) (236.59 ml)',
                    'Pint (pt) (473.18 ml)', 'Quart (qt) (946.35 ml)', 'Liter (L) (1000 ml)',
                    'Gallon (gal) (3785.41 ml)',
                    'Cubic metre (kL) (1000000 ml)']
    if recipe.other_ing_data.all().count() == 0:
        has_other = False
    else:
        has_other = True
        for each_ing in recipe.other_ing_data.all():
            other_ing.append([each_ing.ing_name, each_ing.ing_amount, each_ing.ing_units, each_ing.ing_description])
    options = IngredientCategories.objects.filter(user=request.user.username, company_name=company_name,
                                                  category_type='recipe')
    recipe_options = []
    for option in options:
        if option.category == recipe.recipe_category:
            continue
        else:
            recipe_options.append(option.category)
    if request.method == 'POST':
        print(request.POST)
        recipe_name = request.POST.get('recipe_name')
        try:
            if recipe_name == recipe.recipe_name:
                raise RecipesModel.DoesNotExist
            else:
                check_recipe = RecipesModel.objects.get(recipe_user=str(request.user),
                                                        recipe_name=recipe_name, company_name=company_name)
                return render(
                    request,
                    'edit_recipe.html',
                    {
                        'recipe': recipe,
                        'recipe_options': recipe_options,
                        'has_other': has_other,
                        'ingredients': ingredients,
                        'other_ing': other_ing,
                        'unit_options': unit_options,
                        'fail': 'Recipe Name Already Exists',
                        'username': user.username,
                        'email': user.email,
                        'first_name': user.first_name,
                        'last_name': user.last_name,
                        'many_companies': many_companies,
                        'company_details': company_details,
                        'company_name': company_name
                    }
                )
        except RecipesModel.DoesNotExist:
            recipe_category = request.POST.get('recipe_category')
            recipe_yield_count = request.POST.get('recipe_yield_count')
            yield_units = request.POST.get('yield_units')
            recipe.recipe_name = recipe_name
            recipe.recipe_category = recipe_category
            recipe.recipe_yield_count = recipe_yield_count
            recipe.yield_units = yield_units
            recipe.save()
            print(request.POST.getlist('ingridientName'))
            print("Recipe Saved")
            if 'ingAmount' not in request.POST:
                recipe.other_ing_data.clear()
            else:
                recipe.other_ing_data.clear()
                for i in range(len(request.POST.getlist('ingAmount'))):
                    ingredient_data = IngredientData.objects.create(
                        ing_name=request.POST.getlist('ingridientName')[i],
                        ing_amount=request.POST.getlist('ingAmount')[i],
                        ing_units=request.POST.getlist('ingUnits')[i],
                        ing_description=request.POST.getlist('ingDescription')[i]
                    )
                    recipe.other_ing_data.add(ingredient_data)
                    print("Recipe Updated")
            return redirect('/recipe/edit/' + str(ing_id))
    else:
        return render(
            request,
            'edit_recipe.html',
            {
                'recipe': recipe,
                'recipe_options': recipe_options,
                'has_other': has_other,
                'ingredients': ingredients,
                'other_ing': other_ing,
                'unit_options': unit_options,
                'username': user.username,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'many_companies': many_companies,
                'company_details': company_details,
                'company_name': company_name
            }
        )


@login_required(login_url='/login')
def ingredient_details(request, ing_id):
    user = UserModel.objects.get(username=request.user)
    company_details = Company.objects.filter(user=request.user)
    if company_details.count() > 1:
        many_companies = True
    else:
        many_companies = False
    company_name = request.session['company_name']
    ingredient = Ingredients.objects.get(id=ing_id)
    ingredient_recipes = RecipesModel.objects.filter(other_ing_data__ing_name=ingredient.name,
                                                     company_name=company_name, recipe_user=request.user.username)
    ingredient_suppliers = IngredientSuppliers.objects.filter(ingredient_relation=ingredient)
    file_loc = "./measurments/nutrition_data.xlsx"
    wookbook = openpyxl.load_workbook(file_loc)
    worksheet = wookbook.active
    nutri_data = []
    nutri_fields = []
    if ingredient.nutriationData == '':
        has_nutridata = False
    else:
        if ingredient.fromMeasurementData == '':
            has_nutridata = False
        else:
            has_nutridata = True
            for i,j in enumerate(worksheet):
                if i==1:
                    for each_j in j:
                        nutri_fields.append(each_j.value)
                    break
            for each in worksheet:
                if each[1].value == ingredient.nutriationData:
                    for col in each:
                        nutri_data.append(col.value)
    return render(
        request,
        'each_ingridient_detail.html',
        {
            'ingredient': ingredient,
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'many_companies': many_companies,
            'company_details': company_details,
            'company_name': company_name,
            'ingredient_suppliers': ingredient_suppliers,
            'qty_units': qty_units,
            'ingredient_recipes': ingredient_recipes,
            'has_major_allergens': ingredient.hasMajorAllergens,
            'major_allergens': ingredient.majorAllergens,
            'nutri_data': zip(nutri_data,nutri_fields),
            'has_nutridata': has_nutridata,
            'ingredient_measurments': zip(ingredient.fromMeasurementData,ingredient.fromMeasurementUnits,ingredient.toMeasurementData,ingredient.toMeasurementUnits)
        }
    )


@login_required(login_url='/login')
def edit_ingredient(request, ing_id):
    user = UserModel.objects.get(username=request.user)
    company_details = Company.objects.filter(user=request.user)
    company_name = request.session['company_name']
    if company_details.count() > 1:
        many_companies = True
    else:
        many_companies = False
    ingredient = Ingredients.objects.get(id=ing_id)
    allergens_list = ['Cerly', 'Eggs', 'Fish', 'Milk', 'Lupin', 'Molluscs', 'Mustard', 'Peanuts', 'Sesame', 'Shellfish',
                      'Soy', 'Sulfites', 'Tree Nuts', 'Wheat']
    if ingredient.hasMajorAllergens:
        allergens = ingredient.majorAllergens
        print(allergens)
    else:
        allergens = None
    if ingredient.fromMeasurementData is None:
        has_measurments = False
        measurements = None
        ing_val = ''
    else:
        has_measurments = True
        measurements = zip(ingredient.fromMeasurementData, ingredient.fromMeasurementUnits,
                           ingredient.toMeasurementData, ingredient.toMeasurementUnits)
        from_md = ''
        from_mu = ''
        to_md = ''
        to_mu = ''
        for each in zip(ingredient.fromMeasurementData, ingredient.fromMeasurementUnits,
                        ingredient.toMeasurementData, ingredient.toMeasurementUnits):
            from_md = from_md + str(each[0]) + ','
            from_mu = from_mu + str(each[1]) + ','
            to_md = to_md + str(each[2]) + ','
            to_mu = to_mu + str(each[3]) + ','
        ing_val = from_md + ';' + to_md + ';' + from_mu + ';' + to_mu
    if request.method == 'POST':
        form = IngredientsForm(instance=ingredient, request=request, data=request.POST)
        if form.is_valid():
            form.save()
            indredients = Ingredients.objects.get(username=request.user, name=form.cleaned_data['name'],
                                                  company_name=company_name)
            indredients.nutriationData = request.POST.get('nutri-data-link-value')
            indredients.fdcId = request.POST.get('nutri-data-fdcid')
            indredients.save()
            if form.cleaned_data['suppliers'] == 'Add Supplier':
                indredients.suppliers = request.POST.get('customsupplier')
                indredients.save()
                Suppliers.objects.create(supplier_name=request.POST.get('customsupplier'),
                                         user=request.user.username, company_name=company_name).save()
                IngredientSuppliers.objects.create(ingredient_relation=indredients,
                                                   supplier=request.POST.get('customsupplier'),
                                                   price=form.cleaned_data['price'],
                                                   order_code=form.cleaned_data['orderCode'],
                                                   caseQuantity=form.cleaned_data['caseQuantity'],
                                                   packSize=form.cleaned_data['packSize'],
                                                   qtyUnits=form.cleaned_data['qtyUnits'], preferred=True).save()
            if form.cleaned_data['category'] == 'Add Category':
                indredients.category = request.POST.get('customcategory')
                indredients.save()
                IngredientCategories.objects.create(user=request.user.username, company_name=company_name,
                                                    category=request.POST.get('customcategory'),
                                                    category_type='ingredient').save()
            ingMeasurementsData = request.POST.get('ingMeasurementsData')
            if ingMeasurementsData == '':
                indredients.fromMeasurementUnits = []
                indredients.fromMeasurementData = []
                indredients.toMeasurementUnits = []
                indredients.toMeasurementData = []
                indredients.save()
            else:
                print(ingMeasurementsData)
                ingdata = ingMeasurementsData.split(';')
                fromdata = ingdata[0].split(',')
                todata = ingdata[1].split(',')
                fromunits = ingdata[2].split(',')
                tounits = ingdata[3].split(',')
                indredients.fromMeasurementUnits = fromunits[:-1]
                indredients.fromMeasurementData = fromdata[:-1]
                indredients.toMeasurementUnits = tounits[:-1]
                indredients.toMeasurementData = todata[:-1]
                indredients.save()
                print("Ingredients Saved")
            return redirect('/recipe/editing/' + str(ing_id))
        else:
            return render(
                request,
                'edit_ingridient.html',
                {
                    'ingredient': ingredient,
                    'form': form,
                    'has_major_Allergens': ingredient.hasMajorAllergens,
                    'has_measurements': has_measurments,
                    'measurements': measurements,
                    'allergens': allergens,
                    'allergens_list': allergens_list,
                    'username': user.username,
                    'email': user.email,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'many_companies': many_companies,
                    'company_details': company_details,
                    'company_name': company_name,
                    'ing_val': ing_val
                }
            )
    else:
        form = IngredientsForm(instance=ingredient, request=request)
        print(ingredient.hasMajorAllergens)
        return render(
            request,
            'edit_ingridient.html',
            {
                'ingredient': ingredient,
                'form': form,
                'has_major_Allergens': ingredient.hasMajorAllergens,
                'has_measurements': has_measurments,
                'measurements': measurements,
                'allergens': allergens,
                'allergens_list': allergens_list,
                'username': user.username,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'many_companies': many_companies,
                'company_details': company_details,
                'company_name': company_name,
                'ing_val': ing_val
            }
        )


@login_required(login_url='/login')
def delete_ingredient(request, ing_id):
    ingredient = Ingredients.objects.get(id=ing_id)
    ingredient.delete()
    return redirect('/recipe/page')


@login_required(login_url='/login')
def delete_recipe(request, rec_id):
    recipe = RecipesModel.objects.get(id=rec_id)
    recipe.delete()
    return redirect('/recipe/recipelist')


@login_required(login_url='/login')
def download_ingredients(request):
    ingredients = Ingredients.objects.filter(username=request.user)
    fields = ['Name', 'price', 'case quantity', 'pack size', 'quantity units', 'category', 'suppliers', 'order code',
              'brand', 'country of origin', 'storage areas', 'par levels', 'par units'
              ]
    data = []
    for ingredient in ingredients:
        data.append(
            [str(ingredient.name), str(ingredient.price), str(ingredient.caseQuantity), str(ingredient.packSize),
             str(ingredient.qtyUnits), str(ingredient.category), str(ingredient.suppliers), str(ingredient.orderCode),
             str(ingredient.brand), str(ingredient.countryOfOrigin), str(ingredient.storageAreas),
             str(ingredient.parLevel), str(ingredient.parUnits)])
    file = io.StringIO()
    writer = csv.writer(file, delimiter=',')
    writer.writerow(fields)
    writer.writerows(data)
    csv_data = file.getvalue()
    final_data = csv_data.encode('utf-8')
    byte_io = io.BytesIO(final_data)
    response = HttpResponse(FileWrapper(byte_io), content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=ingredients.csv'
    return response


@login_required(login_url='/login')
def download_recipes(request):
    recipies = RecipesModel.objects.filter(recipe_user=str(request.user))
    fields = ['recipe names', 'recipe category', 'recipe yield count', 'yield units']
    data = []
    for recipe in recipies:
        data.append([recipe.recipe_name, recipe.recipe_category, recipe.recipe_yield_count, recipe.yield_units])
    file = io.StringIO()
    writer = csv.writer(file, delimiter=',')
    writer.writerow(fields)
    writer.writerows(data)
    csv_data = file.getvalue()
    final_data = csv_data.encode('utf-8')
    byte_io = io.BytesIO(final_data)
    response = HttpResponse(FileWrapper(byte_io), content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=Recipe.csv'
    return response


@login_required(login_url='/login')
def suppliers_dashboard(request):
    user = UserModel.objects.get(username=request.user)
    company_details = Company.objects.filter(user=request.user)
    if company_details.count() > 1:
        many_companies = True
    else:
        many_companies = False
    company_name = request.session['company_name']
    suppliers = Suppliers.objects.filter(user=request.user, company_name=company_name)
    return render(
        request,
        'suppliers.html',
        {
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'many_companies': many_companies,
            'company_details': company_details,
            'company_name': company_name,
            'suppliers': suppliers
        }
    )


@login_required(login_url='/login')
def create_supplier(request):
    user = UserModel.objects.get(username=request.user)
    company_details = Company.objects.filter(user=request.user)
    if company_details.count() > 1:
        many_companies = True
    else:
        many_companies = False
    company_name = request.session['company_name']
    if request.method == 'POST':
        form = SuppliersForm(request.POST)
        if form.is_valid():
            supplier = form.save(commit=False)
            supplier.user = request.user
            supplier.company_name = company_name
            supplier.save()
            return redirect('/recipe/suppliers')
        else:
            return render(
                request,
                'suppliers_new.html',
                {
                    'username': user.username,
                    'email': user.email,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'many_companies': many_companies,
                    'company_details': company_details,
                    'company_name': company_name,
                    'form': form
                }
            )
    else:
        form = SuppliersForm()
        return render(
            request,
            'suppliers_new.html',
            {
                'username': user.username,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'many_companies': many_companies,
                'company_details': company_details,
                'company_name': company_name,
                'form': form
            }
        )


@login_required(login_url='/login')
def each_supplier_info(request, supplier_id):
    user = UserModel.objects.get(username=request.user)
    company_details = Company.objects.filter(user=request.user)
    if company_details.count() > 1:
        many_companies = True
    else:
        many_companies = False
    company_name = request.session.get('company_name')
    supplier = Suppliers.objects.get(id=supplier_id)
    return render(
        request,
        'each_supplier_info.html',
        {
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'many_companies': many_companies,
            'company_details': company_details,
            'company_name': company_name,
            'supplier': supplier
        }
    )


@login_required(login_url='/login')
def edit_supplier(request, supplier_id):
    user = UserModel.objects.get(username=request.user)
    company_details = Company.objects.filter(user=request.user)
    if company_details.count() > 1:
        many_companies = True
    else:
        many_companies = False
    company_name = request.session.get('company_name')
    supplier = Suppliers.objects.get(id=supplier_id)
    options = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    if request.method == 'POST':
        form = SuppliersForm(instance=supplier, data=request.POST)
        if form.is_valid():
            form.save()
            supplier.delivery_days = request.POST.getlist('delivery_days')
            supplier.save()
            return redirect('/recipe/suppliers/edit/' + str(supplier_id))
        else:
            return render(
                request,
                'supplier_edit.html',
                {
                    'username': user.username,
                    'email': user.email,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'many_companies': many_companies,
                    'company_details': company_details,
                    'company_name': company_name,
                    'supplier': supplier,
                    'form': form,
                    'options': options
                }
            )
    else:
        form = UpdateSupplier(instance=supplier)
        return render(
            request,
            'supplier_edit.html',
            {
                'username': user.username,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'many_companies': many_companies,
                'company_details': company_details,
                'company_name': company_name,
                'supplier': supplier,
                'form': form,
                'options': options
            }
        )


@login_required(login_url='/login')
def delete_supplier(request, supplier_id):
    supplier = Suppliers.objects.get(id=supplier_id)
    supplier.delete()
    return redirect('/recipe/suppliers')


@login_required(login_url='/login')
def download_suppliers(request):
    company_name = request.session.get('company_name')
    suppliers = Suppliers.objects.filter(user=request.user, company_name=company_name)
    fields = ['Supplier Name', 'Order Email', 'Phone Number', 'Sales Rep First Name', 'Sales Rep Last Name',
              'Sales Rep Email', 'Sales Rep Phone Number', 'Preferred Order Method', 'Delivery Days', 'Note']
    data = []
    for supplier in suppliers:
        data.append([supplier.supplier_name, supplier.order_email, supplier.phone_number, supplier.sales_rep_first_name,
                     supplier.sales_rep_last_name, supplier.sales_rep_email, supplier.sales_rep_phone_number,
                     supplier.preferred_order_method, supplier.delivery_days, supplier.note])
    file = io.StringIO()
    writer = csv.writer(file, delimiter=',')
    writer.writerow(fields)
    writer.writerows(data)
    csv_data = file.getvalue()
    final_data = csv_data.encode('utf-8')
    byte_io = io.BytesIO(final_data)
    response = HttpResponse(FileWrapper(byte_io), content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=Suppliers.csv'
    return response


@login_required(login_url='/login')
def category_dashboard(request):
    user = UserModel.objects.get(username=request.user)
    company_details = Company.objects.filter(user=request.user)
    if company_details.count() > 1:
        many_companies = True
    else:
        many_companies = False
    company_name = request.session.get('company_name')
    ingredient_categories = IngredientCategories.objects.filter(user=request.user, company_name=company_name,
                                                                category_type='ingredient')
    recipe_categories = IngredientCategories.objects.filter(user=request.user, company_name=company_name,
                                                            category_type='recipe')
    ingredients = Ingredients.objects.filter(username=request.user.username, company_name=company_name)
    if request.method == 'POST':
        if 'ingredientCategory' in request.POST:
            IngredientCategories.objects.create(
                user=request.user.username,
                company_name=company_name,
                category=request.POST.get('ingredientCategory'),
                category_type='ingredient'
            ).save()
        if 'recipeCategory' in request.POST:
            IngredientCategories.objects.create(
                user=request.user.username,
                company_name=company_name,
                category=request.POST.get('recipeCategory'),
                category_type='recipe'
            ).save()
        return redirect('/recipe/listcategories')
    else:
        return render(
            request,
            'ingredient_recipe_category.html',
            {
                'username': user.username,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'many_companies': many_companies,
                'company_details': company_details,
                'company_name': company_name,
                'ingredient_categories': ingredient_categories,
                'recipe_categories': recipe_categories,
                'ingredients': ingredients
            }
        )


@login_required(login_url='/login')
def delete_category(request, cat_id):
    category = IngredientCategories.objects.get(id=cat_id)
    category.delete()
    return redirect('/recipe/listcategories')


@login_required(login_url='/login')
def handle_measurement(request):
    print(request.POST)
    units = ['oz', 'lb', 'Kg', 'T', 'g', 'pinch', 'tsp', 'tbsp', 'floz', 'dL', 'cup', 'pt', 'ml', 'qt', 'L', 'gal',
             'kl', 'each', 'dozen', 'hundred', 'thousand', 'million', 's', 'min', 'hr']
    data = []
    with open('./measurments/measurements.csv', 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        fields = next(csv_reader)
        for row in csv_reader:
            if row[1] == request.POST.get('selected_food'):
                print(row)
                if row[7] != 'Quantity not specified':
                    if row[7].split(' ')[-1] in units and len(row[7].split(' ')) == 2:
                        for each_qty in Ingredients.qtyUnits_Choices:
                            for qty in each_qty[1:2]:
                                for each in qty:
                                    if each[0][each[0].index("(") + 1:each[0].index(")")] == row[7].split(' ')[-1]:
                                        data.append([row[7], row[8], each[0]])
                    else:
                        data.append(['1 each ' + row[7], row[8], 'Each (each)'])
    with open('./measurments/food_portion.csv','r') as csvfile:
        csvreader = csv.reader(csvfile)
        for each in csvreader:
            if each[1] == request.POST.get('fdcId'):
                for each_qty in Ingredients.qtyUnits_Choices:
                    for qty in each_qty[1:2]:
                        for eachq in qty:
                            if eachq[0][eachq[0].index("(") + 1:eachq[0].index(")")] == each[6]:
                                data.append([each[3] + ' ' + each[6], each[7],eachq[0]])
    return HttpResponse({json.dumps({'measurement_units': data})}, content_type='application/json')


@login_required(login_url='/login')
def crate_storage_area(request):
    user = UserModel.objects.get(username=request.user)
    company_details = Company.objects.filter(user=request.user)
    if company_details.count() > 1:
        many_companies = True
    else:
        many_companies = False
    company_name = request.session.get('company_name')
    storage_areas = StorageAreas.objects.filter(user=request.user.username, company_name=company_name)
    if request.method == 'POST':
        form = StorageAreaForm(request.POST)
        if form.is_valid():
            storage_area = form.save(commit=False)
            storage_area.user = request.user.username
            storage_area.company_name = company_name
            storage_area.save()
            print(storage_area.id)
            return redirect('/recipe/storagearea/edit/' + str(storage_area.id))
        else:
            return render(
                request,
                'storage_areas.html',
                {
                    'username': user.username,
                    'email': user.email,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'many_companies': many_companies,
                    'company_details': company_details,
                    'company_name': company_name,
                    'storage_areas': storage_areas,
                    'form': form
                }
            )
    else:
        form = StorageAreaForm()
        return render(
            request,
            'storage_areas.html',
            {
                'username': user.username,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'many_companies': many_companies,
                'company_details': company_details,
                'company_name': company_name,
                'storage_areas': storage_areas,
                'form': form
            }
        )


@login_required(login_url='/login')
def edit_storage_area(request, storage_area_id):
    user = UserModel.objects.get(username=request.user)
    company_details = Company.objects.filter(user=request.user)
    if company_details.count() > 1:
        many_companies = True
    else:
        many_companies = False
    company_name = request.session.get('company_name')
    storage_area = StorageAreas.objects.get(id=storage_area_id)
    if request.method == 'POST':
        form = StorageAreaForm(instance=storage_area, data=request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            try:
                if name != storage_area.name:
                    check_area = StorageAreas.objects.get(user=request.user.username, company_name=company_name,
                                                          name=name)
                else:
                    form.save()
                    return redirect('/recipe/storagearea/edit/' + str(storage_area_id))
                return render(
                    request,
                    'edit_storage_area.html',
                    {
                        'username': user.username,
                        'email': user.email,
                        'first_name': user.first_name,
                        'last_name': user.last_name,
                        'many_companies': many_companies,
                        'company_details': company_details,
                        'company_name': company_name,
                        'storage_area': storage_area,
                        'form': form,
                        'fail': 'Name Already taken'
                    }
                )
            except StorageAreas.DoesNotExist:
                form.save()
                return redirect('/recipe/storagearea/edit/' + str(storage_area_id))
        else:
            return render(
                request,
                'edit_storage_area.html',
                {
                    'username': user.username,
                    'email': user.email,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'many_companies': many_companies,
                    'company_details': company_details,
                    'company_name': company_name,
                    'storage_area': storage_area,
                    'form': form
                }
            )
    else:
        form = StorageAreaForm(instance=storage_area)
        return render(
            request,
            'edit_storage_area.html',
            {
                'username': user.username,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'many_companies': many_companies,
                'company_details': company_details,
                'company_name': company_name,
                'storage_area': storage_area,
                'form': form
            }
        )


@login_required(login_url='/login')
def ingredient_images(request, ing_id):
    user = UserModel.objects.get(username=request.user)
    company_details = Company.objects.filter(user=request.user)
    if company_details.count() > 1:
        many_companies = True
    else:
        many_companies = False
    company_name = request.session.get('company_name')
    ingredient_detail = Ingredients.objects.get(id=ing_id)
    if request.method == 'POST':
        image = request.FILES.get('ingredient_image')
        ingredient_image = IngredientImages.objects.create(ingredient_image=image)
        ingredient_image.save()
        ingredient_detail.ingredient_images.add(ingredient_image)
        if 'back-to-ingredients' in request.POST:
            return redirect('/recipe/uploadimage/' + str(ing_id))
        if 'back-to-dashboard' in request.POST:
            return redirect('/recipe/page')
    else:
        return render(
            request,
            'ingredient_images.html',
            {
                'username': user.username,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'many_companies': many_companies,
                'company_details': company_details,
                'company_name': company_name,
                'ingredient_images': ingredient_detail.ingredient_images.all(),
                'ingredient': ingredient_detail
            }
        )


@login_required(login_url='/login')
def delete_ingredient_image(request, img_id):
    ing_image = IngredientImages.objects.get(id=img_id)
    ing_image.delete()
    return redirect('/recipe/page')


@login_required(login_url='/login')
def replace_ingredient(request, ing_id):
    user = UserModel.objects.get(username=request.user)
    company_details = Company.objects.filter(user=request.user)
    if company_details.count() > 1:
        many_companies = True
    else:
        many_companies = False
    company_name = request.session.get('company_name')
    ingredient = Ingredients.objects.get(id=ing_id)
    recipes = RecipesModel.objects.filter(recipe_user=request.user.username, company_name=company_name,
                                          other_ing_data__ing_name=ingredient.name)
    ingredient_categories = IngredientCategories.objects.filter(user=request.user, company_name=company_name,
                                                                category_type='ingredient')
    ingredient_list = Ingredients.objects.filter(username=request.user.username, company_name=company_name)
    if recipes.count() == 0:
        has_recipe = False
    else:
        has_recipe = True
    return render(
        request,
        'replace_ingredient.html',
        {
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'many_companies': many_companies,
            'company_details': company_details,
            'company_name': company_name,
            'ingredient_list': ingredient_list,
            'has_recipe': has_recipe,
            'ingredient_categories': ingredient_categories,
            'ingredient': ingredient
        }
    )


@login_required(login_url='/login')
def confirm_replace(request, from_id, to_id):
    user = UserModel.objects.get(username=request.user)
    company_details = Company.objects.filter(user=request.user)
    if company_details.count() > 1:
        many_companies = True
    else:
        many_companies = False
    company_name = request.session.get('company_name')
    from_ingredient = Ingredients.objects.get(id=from_id)
    recipes = RecipesModel.objects.filter(recipe_user=request.user.username, company_name=company_name,
                                          other_ing_data__ing_name=from_ingredient.name)
    to_ingredient = Ingredients.objects.get(id=to_id)

    if request.method == 'POST':
        for each_ing in request.POST.getlist('replaceIng'):
            recipe = RecipesModel.objects.get(recipe_user=request.user.username, company_name=company_name,
                                              recipe_name=each_ing)
            for each in recipe.other_ing_data.all():
                each.ing_name = to_ingredient.name
                each.save()
        return redirect('/recipe/ingridientdetails/' + str(from_id))
    else:
        for each in recipes.all():
            print(each.recipe_name)
            '''for i in each.other_ing_data.all():
                print(i.ing_name)'''
        return render(
            request,
            'confirm_ingredient_replacement.html',
            {
                'username': user.username,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'many_companies': many_companies,
                'company_details': company_details,
                'company_name': company_name,
                'recipes': recipes.all(),
                'from_ingredient': from_ingredient,
                'to_ingredient': to_ingredient,
                'ingredient': from_ingredient
            }
        )


@login_required(login_url='/login')
def edit_nutrition_details(request, ing_id):
    user = UserModel.objects.get(username=request.user)
    company_details = Company.objects.filter(user=request.user)
    if company_details.count() > 1:
        many_companies = True
    else:
        many_companies = False
    company_name = request.session.get('company_name')
    ingredient = Ingredients.objects.get(id=ing_id)
    try:
        nutrition_details = NutritionDetails.objects.get(user=request.user.username, company_name=company_name,
                                                         ingredient=ingredient.name)
        form = NutritionDetailsForm(instance=nutrition_details)
    except NutritionDetails.DoesNotExist:
        form = NutritionDetailsForm()
    if request.method == 'POST':
        try:
            nutrition_details = NutritionDetails.objects.get(user=request.user.username, company_name=company_name,
                                                             ingredient=ingredient.name)
            form = NutritionDetailsForm(instance=nutrition_details, data=request.POST)
            if form.is_valid():
                form.save()
                return redirect('/recipe/edit_nutrition_details/' + str(ing_id))
            else:
                return render(
                    request,
                    'edit_ingredient_details.html',
                    {
                        'username': user.username,
                        'email': user.email,
                        'first_name': user.first_name,
                        'last_name': user.last_name,
                        'many_companies': many_companies,
                        'company_details': company_details,
                        'company_name': company_name,
                        'ingredient': ingredient,
                        'form': form
                    }
                )
        except NutritionDetails.DoesNotExist:
            form = NutritionDetailsForm(request.POST)
            if form.is_valid():
                nutrition = form.save(commit=False)
                nutrition.user = request.user.username
                nutrition.company_name = company_name
                nutrition.ingredient = ingredient.name
                nutrition.save()
                return redirect('/recipe/edit_nutrition_details/' + str(ing_id))
            else:
                return render(
                    request,
                    'edit_ingredient_details.html',
                    {
                        'username': user.username,
                        'email': user.email,
                        'first_name': user.first_name,
                        'last_name': user.last_name,
                        'many_companies': many_companies,
                        'company_details': company_details,
                        'company_name': company_name,
                        'ingredient': ingredient,
                        'form': form
                    }
                )
    else:
        return render(
            request,
            'edit_ingredient_details.html',
            {
                'username': user.username,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'many_companies': many_companies,
                'company_details': company_details,
                'company_name': company_name,
                'ingredient': ingredient,
                'form': form
            }
        )


@login_required(login_url='/login')
def recipe_preparation_instructions(request, recipe_id):
    user = UserModel.objects.get(username=request.user)
    company_details = Company.objects.filter(user=request.user)
    if company_details.count() > 1:
        many_companies = True
    else:
        many_companies = False
    company_name = request.session['company_name']
    recipe = RecipesModel.objects.get(id=recipe_id)
    if request.method == 'POST':
        form = RecipePreparationInstructions(instance=recipe, data=request.POST)
        if form.is_valid():
            form.save()
            if 'backtorecipedashboard' in request.POST:
                return redirect('/recipe/recipelist')
            if 'backtorecipes' in request.POST:
                return redirect('/recipe/preparation/' + str(recipe_id))
        else:
            return render(
                request,
                'recipe_preparation_instructions.html',
                {
                    'username': user.username,
                    'email': user.email,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'recipe': recipe,
                    'many_companies': many_companies,
                    'company_details': company_details,
                    'company_name': company_name,
                    'form': form
                }
            )
    else:
        form = RecipePreparationInstructions(instance=recipe)
        return render(
            request,
            'recipe_preparation_instructions.html',
            {
                'username': user.username,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'recipe': recipe,
                'many_companies': many_companies,
                'company_details': company_details,
                'company_name': company_name,
                'form': form
            }
        )


@login_required(login_url='/login')
def add_ingredient_supplier(request, ing_id):
    user = UserModel.objects.get(username=request.user)
    company_details = Company.objects.filter(user=request.user)
    if company_details.count() > 1:
        many_companies = True
    else:
        many_companies = False
    company_name = request.session['company_name']
    ingredient = Ingredients.objects.get(id=ing_id)
    ingredient_suppliers = IngredientSuppliers.objects.filter(ingredient_relation=ingredient)
    ingredient_recipes = RecipesModel.objects.filter(other_ing_data__ing_name=ingredient.name,
                                                     company_name=company_name, recipe_user=request.user.username)
    if request.method == 'POST':
        form = Ingredient_SupplierForm(request=request, data=request.POST)
        if form.is_valid():
            nutri_instance = form.save(commit=False)
            nutri_instance.ingredient_relation = ingredient
            if request.POST.get('supplier') == 'Add Supplier':
                nutri_instance.supplier = request.POST.get('customsupplier')
                nutri_instance.save()
                Suppliers.objects.create(user=request.user.username, company_name=company_name,
                                         supplier_name=request.POST.get('customsupplier')).save()
            else:
                nutri_instance.save()
            return redirect('/recipe/ingridientdetails/' + str(ing_id))
        else:
            return render(
                request,
                'each_ingridient_detail.html',
                {
                    'username': user.username,
                    'email': user.email,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'many_companies': many_companies,
                    'company_details': company_details,
                    'company_name': company_name,
                    'ingredient': ingredient,
                    'form': form,
                    'ingredient_suppliers': ingredient_suppliers,
                    'qty_units': qty_units,
                    'ingredient_recipes': ingredient_recipes,
                    'has_major_allergens': ingredient.hasMajorAllergens,
                    'major_allergens': ingredient.majorAllergens
                }
            )
    else:
        form = Ingredient_SupplierForm(request=request)
        return render(
            request,
            'each_ingridient_detail.html',
            {
                'username': user.username,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'many_companies': many_companies,
                'company_details': company_details,
                'company_name': company_name,
                'ingredient': ingredient,
                'form': form,
                'ingredient_suppliers': ingredient_suppliers,
                'qty_units': qty_units,
                'ingredient_recipes': ingredient_recipes,
                'has_major_allergens': ingredient.hasMajorAllergens,
                'major_allergens': ingredient.majorAllergens
            }
        )


@login_required(login_url='/login')
def edit_ingredient_suppliers(request, ing_id):
    user = UserModel.objects.get(username=request.user)
    company_details = Company.objects.filter(user=request.user)
    if company_details.count() > 1:
        many_companies = True
    else:
        many_companies = False
    company_name = request.session['company_name']
    ingredient = Ingredients.objects.get(id=ing_id)
    ingredient_suppliers = IngredientSuppliers.objects.filter(ingredient_relation=ingredient)
    return render(
        request,
        'edit_ingredient_suppliers.html',
        {
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'many_companies': many_companies,
            'company_details': company_details,
            'company_name': company_name,
            'ingredient': ingredient,
            'ingredient_suppliers': ingredient_suppliers,
            'qty_units': qty_units
        }
    )


@login_required(login_url='/login')
def edit_each_ingredient_supplier(request, ing_id, ing_supplier_id):
    user = UserModel.objects.get(username=request.user)
    company_details = Company.objects.filter(user=request.user)
    if company_details.count() > 1:
        many_companies = True
    else:
        many_companies = False
    company_name = request.session['company_name']
    ingredient = Ingredients.objects.get(id=ing_id)
    ingredient_supplier = IngredientSuppliers.objects.get(id=ing_supplier_id)
    ingredient_suppliers = IngredientSuppliers.objects.filter(ingredient_relation=ingredient)
    form = UpdateIngredientSupplierForm(instance=ingredient_supplier, request=request)
    if request.method == 'POST':
        form = UpdateIngredientSupplierForm(instance=ingredient_supplier, request=request, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('/recipe/edit_ingredient_suppliers/' + str(ing_id))
        else:
            return render(
                request,
                'edit_ingredient_suppliers.html',
                {
                    'username': user.username,
                    'email': user.email,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'many_companies': many_companies,
                    'company_details': company_details,
                    'company_name': company_name,
                    'ingredient': ingredient,
                    'form': form,
                    'ingredient_suppliers': ingredient_suppliers,
                    'qty_units': qty_units
                }
            )
    else:
        return render(
            request,
            'edit_ingredient_suppliers.html',
            {
                'username': user.username,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'many_companies': many_companies,
                'company_details': company_details,
                'company_name': company_name,
                'ingredient': ingredient,
                'form': form,
                'ingredient_suppliers': ingredient_suppliers,
                'qty_units': qty_units
            }
        )


@login_required(login_url='/login')
def delete_each_ingredient_supplier(request, ing_id, ing_supplier_id):
    IngredientSuppliers.objects.get(id=ing_supplier_id).delete()
    return redirect('/recipe/edit_ingredient_suppliers/' + str(ing_id))


@login_required(login_url='/login')
def set_preferred_ingredient_supplier(request, ing_id, ing_supplier_id):
    ingredient = Ingredients.objects.get(id=ing_id)
    try:
        ingredient_supplier = IngredientSuppliers.objects.get(ingredient_relation=ingredient, preferred=True)
        ingredient_supplier.preferred = False
        ingredient_supplier.save()
        ing_supplier = IngredientSuppliers.objects.get(id=ing_supplier_id)
        ing_supplier.preferred = True
        ing_supplier.save()
        ingredient.price = ing_supplier.price
        ingredient.caseQuantity = ing_supplier.caseQuantity
        ingredient.packSize = ing_supplier.packSize
        ingredient.qtyUnits = ing_supplier.qtyUnits
        ingredient.orderCode = ing_supplier.order_code
        ingredient.brand = ing_supplier.brand
        ingredient.countryOfOrigin = ing_supplier.country_of_origin
        ingredient.save()
    except IngredientSuppliers.DoesNotExist:
        ing_supp =  IngredientSuppliers.objects.get(ingredient_relation=ingredient)
        ing_supp.preferred = True
        ing_supp.save()
    return redirect('/recipe/edit_ingredient_suppliers/' + str(ing_id))


@login_required(login_url='/login')
def allergen_recipes(request, rec_id):
    user = UserModel.objects.get(username=request.user)
    company_details = Company.objects.filter(user=request.user)
    if company_details.count() > 1:
        many_companies = True
    else:
        many_companies = False
    company_name = request.session['company_name']
    recipe = RecipesModel.objects.get(id=rec_id)
    recipe_allergens = []
    ingredient_recipes = []
    for each_recipe in recipe.other_ing_data.all():
        ingredient = Ingredients.objects.get(username=request.user.username, company_name=company_name,
                                             name=each_recipe.ing_name)
        if ingredient.hasMajorAllergens is None or ingredient.hasMajorAllergens == 'No':
            ingredient_recipes.append(ingredient)
        else:
            recipe_allergens.append(ingredient.majorAllergens)
    return render(
        request,
        'recipe_allergens.html',
        {
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'many_companies': many_companies,
            'company_details': company_details,
            'company_name': company_name,
            'recipe': recipe,
            'recipe_allergens': recipe_allergens,
            'qty_units': qty_units,
            'ingredient_recipes': ingredient_recipes,
            'weight_units': Ingredients.qtyUnits_Choices[0],
            'volume_units': Ingredients.qtyUnits_Choices[1],
            'quantity_units': Ingredients.qtyUnits_Choices[2]
        }
    )


@login_required(login_url='/login')
def recipe_images(request,rec_id):
    user = UserModel.objects.get(username=request.user)
    company_details = Company.objects.filter(user=request.user)
    if company_details.count() > 1:
        many_companies = True
    else:
        many_companies = False
    company_name = request.session.get('company_name')
    recipe = RecipesModel.objects.get(id=rec_id)
    if request.method == 'POST':
        image = request.FILES.get('recipe_image')
        recipe_image = RecipeImages.objects.create(recipe_image=image)
        recipe_image.save()
        recipe.recipe_images.add(recipe_image)
        if 'back-to-recipe' in request.POST:
            return redirect('/recipe/images/' + str(rec_id))
        if 'back-to-dashboard' in request.POST:
            return redirect('/recipe/recipelist')
    else:
        return render(
            request,
            'recipe_images.html',
            {
                'username': user.username,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'many_companies': many_companies,
                'company_details': company_details,
                'company_name': company_name,
                'recipe': recipe,
                'recipe_images': recipe.recipe_images.all()
            }
        )


@login_required(login_url='/login')
def delete_recipe_image(request,img_id):
    RecipeImages.objects.get(id=img_id).delete()
    return redirect('/recipe/recipelist')


@login_required(login_url='/login')
def production_plan_dashboard(request):
    user = UserModel.objects.get(username=request.user)
    company_details = Company.objects.filter(user=request.user)
    if company_details.count() > 1:
        many_companies = True
    else:
        many_companies = False
    company_name = request.session.get('company_name')
    productionplans = ProductionPlan.objects.filter(user=request.user.username,company_name=company_name)
    return render(
        request,
        'planning_dashboard.html',
        {
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'many_companies': many_companies,
            'company_details': company_details,
            'company_name': company_name,
            'productionplans': productionplans
        }
    )


@login_required(login_url='/login')
def productionplantemplate(request):
    user = UserModel.objects.get(username=request.user)
    company_details = Company.objects.filter(user=request.user)
    if company_details.count() > 1:
        many_companies = True
    else:
        many_companies = False
    company_name = request.session.get('company_name')
    try:
        instance = ProductionPlanTemplate.objects.get(user=request.user.username,company_name=company_name)
        if request.method == 'POST':
            form = ProductionPlanTemplateForm(instance=instance,data=request.POST)
            if form.is_valid():
                form.save()
                return redirect('/recipe/productionplantemplate')
        else:
            form = ProductionPlanTemplateForm(instance=instance)
            return render(
                request,
                'production_plan_templete.html',
                {
                    'username': user.username,
                    'email': user.email,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'many_companies': many_companies,
                    'company_details': company_details,
                    'company_name': company_name,
                    'form': form
                }
            )
    except ProductionPlanTemplate.DoesNotExist:
        if request.method == 'POST':
            form = ProductionPlanTemplateForm(request.POST)
            if form.is_valid():
                productionplan = form.save(commit=False)
                productionplan.user = request.user.username
                productionplan.company_name = company_name
                productionplan.save()
                return redirect('/recipe/productionplantemplate')
        else:
            form = ProductionPlanTemplateForm()
            return render(
                request,
                'production_plan_templete.html',
                {
                    'username': user.username,
                    'email': user.email,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'many_companies': many_companies,
                    'company_details': company_details,
                    'company_name': company_name,
                    'form': form
                }
            )

@login_required(login_url='/login')
def new_production_plan(request):
    user = UserModel.objects.get(username=request.user)
    company_details = Company.objects.filter(user=request.user)
    if company_details.count() > 1:
        many_companies = True
    else:
        many_companies = False
    company_name = request.session.get('company_name')
    recipes = RecipesModel.objects.filter(recipe_user=request.user.username,company_name=company_name)
    recipe_categories = IngredientCategories.objects.filter(user=request.user.username,company_name=company_name,
                                                            category_type='recipe')
    if request.method == 'POST':
        form = ProductionPlanForm(request.POST)
        if form.is_valid():
            plan = form.save(commit=False)
            plan.user = request.user.username
            plan.company_name = company_name
            plan.save()
            planinstance = ProductionPlan.objects.get(id=plan.id)
            if 'recipename' in request.POST:
                recipenames = request.POST.getlist('recipename')
                recipeyieldcounts = request.POST.getlist('yieldCount')
                recipebatches = request.POST.getlist('categorybatch')
                for i in range(len(recipenames)):
                    recipe = Recipes.objects.create(recipe_name=recipenames[i],target_yield=recipeyieldcounts[i],
                                           category_batch=recipebatches[i])
                    planinstance.recipes.add(recipe)
            return redirect('/recipe/productionplan')
        else:
            return render(
                request,
                'create_production_plan.html',
                {
                    'username': user.username,
                    'email': user.email,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'many_companies': many_companies,
                    'company_details': company_details,
                    'company_name': company_name,
                    'recipes': recipes,
                    'form': form,
                    'recipe_categories': recipe_categories
                }
            )
    else:
        form = ProductionPlanForm()
        return render(
            request,
            'create_production_plan.html',
            {
                'username': user.username,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'many_companies': many_companies,
                'company_details': company_details,
                'company_name': company_name,
                'recipes': recipes,
                'form': form,
                'recipe_categories': recipe_categories
            }
        )

@login_required(login_url='/login')
def get_recipe_details(request):
    if request.method == 'POST':
        other_ingredients = []
        selected_recipe = request.POST.get('selected_recipe')
        recipe = RecipesModel.objects.get(recipe_name=selected_recipe,recipe_user=request.user.username,
                                          company_name=request.session.get('company_name'))
        for other_ingredient in recipe.other_ing_data.all():
            ingredient = Ingredients.objects.get(name=other_ingredient.ing_name,username=request.user.username,
                                                 company_name=request.session.get('company_name'))
            other_ingredients.append([other_ingredient.ing_name,other_ingredient.ing_amount,ingredient.caseQuantity,ingredient.packSize,ingredient.qtyUnits])
        return HttpResponse(json.dumps({'recipe_name':recipe.recipe_name,'yield_count':recipe.recipe_yield_count,'yield_units':recipe.yield_units,'other_ingredient':other_ingredients}),content_type='application/json')


@login_required(login_url='/login')
def get_recipes_from_category(request):
    if request.method == 'POST':
        recipes_data = []
        selected_category = request.POST.get('selected_category')
        recipes = RecipesModel.objects.filter(recipe_category=selected_category,recipe_user=request.user.username,
                                              company_name=request.session.get('company_name'))
        for recipe in recipes:
            other_ingredients = []
            for other_ingredient in recipe.other_ing_data.all():
                ingredient = Ingredients.objects.get(name=other_ingredient.ing_name, username=request.user.username,
                                                     company_name=request.session.get('company_name'))
                other_ingredients.append(
                    [other_ingredient.ing_name, other_ingredient.ing_amount, ingredient.caseQuantity,
                     ingredient.packSize, ingredient.qtyUnits])
            recipes_data.append([recipe.recipe_name,recipe.recipe_yield_count,recipe.yield_units,other_ingredients])
        return HttpResponse(json.dumps({'recipe_data':recipes_data}),content_type='application/json')


@login_required(login_url='/login')
def edit_production_plan(request,plan_id):
    user = UserModel.objects.get(username=request.user)
    company_details = Company.objects.filter(user=request.user)
    if company_details.count() > 1:
        many_companies = True
    else:
        many_companies = False
    company_name = request.session.get('company_name')
    instance = ProductionPlan.objects.get(id=plan_id)
    if instance.recipes.count() == 0:
        has_recipes = False
    else:
        has_recipes = True
    recipes = RecipesModel.objects.filter(recipe_user=request.user.username, company_name=company_name)
    recipe_categories = IngredientCategories.objects.filter(user=request.user.username, company_name=company_name,
                                                            category_type='recipe')
    if request.method == 'POST':
        form = ProductionPlanForm(instance=instance,data=request.POST)
        if form.is_valid():
            form.save()
            if 'recipename' not in request.POST:
                instance.recipes.clear()
            else:
                instance.recipes.clear()
                recipenames = request.POST.getlist('recipename')
                recipeyieldcounts = request.POST.getlist('yieldCount')
                recipebatches = request.POST.getlist('categorybatch')
                for i in range(len(recipenames)):
                    recipe = Recipes.objects.create(recipe_name=recipenames[i], target_yield=recipeyieldcounts[i],
                                                    category_batch=recipebatches[i])
                    instance.recipes.add(recipe)
            return redirect('/recipe/editplan/'+str(plan_id))
        else:
            return render(
                request,
                'edit_production_plan.html',
                {
                    'username': user.username,
                    'email': user.email,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'many_companies': many_companies,
                    'company_details': company_details,
                    'company_name': company_name,
                    'recipes': recipes,
                    'form': form,
                    'recipe_categories': recipe_categories,
                    'has_recipes': has_recipes,
                    'linked_recipes': instance.recipes.all(),
                    'plan': instance
                }
            )
    else:
        form = ProductionPlanForm(instance=instance)
        return render(
            request,
            'edit_production_plan.html',
            {
                'username': user.username,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'many_companies': many_companies,
                'company_details': company_details,
                'company_name': company_name,
                'recipes': recipes,
                'form': form,
                'recipe_categories': recipe_categories,
                'has_recipes': has_recipes,
                'linked_recipes': instance.recipes.all(),
                'plan': instance
            }
        )

@login_required(login_url='/login')
def delete_production_plan(request,plan_id):
    ProductionPlan.objects.get(id=plan_id).delete()
    return redirect('/recipe/productionplan')

@login_required(login_url='/login')
def each_plan_details(request,plan_id):
    user = UserModel.objects.get(username=request.user)
    company_details = Company.objects.filter(user=request.user)
    if company_details.count() > 1:
        many_companies = True
    else:
        many_companies = False
    company_name = request.session.get('company_name')
    plan = ProductionPlan.objects.get(id=plan_id)
    print(plan.date_field)
    return render(
        request,
        'each_production_plan_details.html',
        {
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'many_companies': many_companies,
            'company_details': company_details,
            'company_name': company_name,
            'plan': plan
        }
    )


@login_required(login_url='/login')
def copy_recipe(request,rec_id):
    user = UserModel.objects.get(username=request.user)
    company_details = Company.objects.filter(user=request.user)
    other_ing = []
    if company_details.count() > 1:
        many_companies = True
    else:
        many_companies = False
    company_name = request.session.get('company_name')
    recipe = RecipesModel.objects.get(id=rec_id)
    ingredients = Ingredients.objects.filter(username=request.user, company_name=company_name)
    if recipe.other_ing_data.all().count() == 0:
        has_other = False
    else:
        has_other = True
        for each_ing in recipe.other_ing_data.all():
            other_ing.append([each_ing.ing_name, each_ing.ing_amount, each_ing.ing_units, each_ing.ing_description])
    form = RecipeForm(instance=recipe,request=request)
    return render(
        request,
        'copy_recipe.html',
        {
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'many_companies': many_companies,
            'company_details': company_details,
            'company_name': company_name,
            'form': form,
            'recipe': recipe,
            'has_other': has_other,
            'ingredients': ingredients,
            'other_ing': other_ing,
        }
    )