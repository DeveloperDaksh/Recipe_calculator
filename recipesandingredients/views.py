import json

from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, redirect
from django.http import HttpResponse
from wsgiref.util import FileWrapper
import io
import csv

from recipeapp.models import UserModel
from company.models import Company

from .forms import IngredientsForm, RecipeForm, SuppliersForm, UpdateSupplier, StorageAreaForm
from .models import Ingredients, RecipesModel, IngredientData, Suppliers, IngredientCategories, StorageAreas


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
                indredients.save()
                if form.cleaned_data['suppliers'] == 'Add Supplier':
                    indredients.suppliers = request.POST.get('customsupplier')
                    indredients.save()
                    Suppliers.objects.create(supplier_name=request.POST.get('customsupplier'),
                                             user=request.user.username, company_name=company_name).save()
                    print("Saved Suppliers")
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
            'company_name': company_name
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
            'company_name': company_name
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
                check_recipe = RecipesModel.objects.get(recipe_user=str(request.user),
                                                        recipe_name=form.cleaned_data['recipe_name'],
                                                        company_name=company_name)
                form = RecipeForm()
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
                    recipe.recipe_user = str(request.user)
                    recipe.save()
                    recipedetails = RecipesModel.objects.get(recipe_user=str(request.user),
                                                             recipe_name=form.cleaned_data['recipe_name'])
                    recipedetails.company_name = company_name
                    recipedetails.save()
                    return redirect('/recipe/details/' + str(recipe.id))
                else:
                    recipe = form.save(commit=False)
                    recipe.recipe_user = str(request.user)
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
                        print("Recipe Added")
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
    recipe = RecipesModel.objects.get(recipe_user=str(request.user), id=ing_id)
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
    recipe = RecipesModel.objects.get(recipe_user=str(request.user), id=ing_id)
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
    ingredient = Ingredients.objects.get(username=request.user, id=ing_id)
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
            'company_name': company_name
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
    ingredient = Ingredients.objects.get(username=request.user, id=ing_id)
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
            indredients.save()
            if form.cleaned_data['suppliers'] == 'Add Supplier':
                indredients.suppliers = request.POST.get('customsupplier')
                indredients.save()
                form = IngredientsForm(instance=ingredient, request=request)
                Suppliers.objects.create(supplier_name=request.POST.get('customsupplier'),
                                         user=request.user.username, company_name=company_name).save()
            ingMeasurementsData = request.POST.get('ingMeasurementsData')
            if ingMeasurementsData == '':
                print("delete all")
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
    ingredient = Ingredients.objects.get(username=request.user, id=ing_id)
    ingredient.delete()
    return redirect('/recipe/page')


@login_required(login_url='/login')
def delete_recipe(request, rec_id):
    recipe = RecipesModel.objects.get(recipe_user=request.user, id=rec_id)
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
    with open('./measurments/measurements.csv', 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        fields = next(csv_reader)
        data = []
        for row in csv_reader:
            if row[1] == request.POST.get('selected_food'):
                if row[7] != 'Quantity not specified':
                    for each_qty in Ingredients.qtyUnits_Choices:
                        for qty in each_qty[1:2]:
                            for each in qty:
                                if each[0][each[0].index("(") + 1:each[0].index(")")] == row[7].split(' ')[-1]:
                                    data.append([row[7], row[8], each[0]])
        print(data)
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
