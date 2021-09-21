from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, redirect

from recipeapp.models import UserModel

from .forms import IngredientsForm, RecipeForm
from .models import Ingredients, RecipesModel, IngredientData


@login_required(login_url='/login')
def handleIngredients(request):
    if request.method == 'POST':
        form = IngredientsForm(request=request, data=request.POST)
        print(form.is_valid())
        ingMeasurementsData = request.POST.get('ingMeasurementsData')
        print(ingMeasurementsData)
        if form.is_valid():
            ingname = form.cleaned_data['name']
            try:
                Ingredients.objects.get(Q(name=ingname) & Q(username=request.user))
                return render(
                    request,
                    'add_ingredients.html',
                    {
                        'form': form,
                        'fail': 'Name Already Exists'
                    }
                )
            except Ingredients.DoesNotExist:
                print(form.is_valid())
                print(form.cleaned_data['suppliers'])
                print(request.POST.get('customsupplier'))
                ingredientsdata = form.save(commit=False)
                ingredientsdata.username = request.user
                ingredientsdata.save()
                print("Saved")
                indredients = Ingredients.objects.get(username=request.user, name=form.cleaned_data['name'])
                if form.cleaned_data['suppliers'] == 'Add Supplier':
                    indredients.suppliers = request.POST.get('customsupplier')
                    indredients.save()
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
        user = UserModel.objects.get(username=request.user)
        form = IngredientsForm(request=request)
        return render(
            request,
            'add_ingredients.html',
            {
                'username': user.username,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'form': form
            }
        )


@login_required(login_url='/login')
def ingredientsDashboard(request):
    user = UserModel.objects.get(username=request.user)
    ingridients = Ingredients.objects.filter(username=request.user)
    return render(
        request,
        'ingredients_dashboard.html',
        {
            'ingridients': ingridients,
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
        }
    )


@login_required(login_url='/login')
def recipeDashboard(request):
    user = UserModel.objects.get(username=request.user)
    recipies = RecipesModel.objects.filter(recipe_user=str(request.user))
    return render(
        request,
        'recipe_dashboard.html',
        {
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'recipies': recipies
        }
    )


@login_required(login_url='/login')
def handleRecipes(request):
    user = UserModel.objects.get(username=request.user)
    ingredients = Ingredients.objects.filter(username=request.user)
    if request.method == 'POST':
        form = RecipeForm(request.POST)
        if form.is_valid():
            try:
                check_recipe = RecipesModel.objects.get(recipe_user=str(request.user),
                                                        recipe_name=form.cleaned_data['recipe_name'])
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
                        'form': form
                    }
                )
            except RecipesModel.DoesNotExist:
                if 'ingAmount' not in request.POST:
                    recipe = form.save(commit=False)
                    recipe.recipe_user = str(request.user)
                    recipe.save()
                    return redirect('/recipe/details/' + str(recipe.id))
                else:
                    recipe = form.save(commit=False)
                    recipe.recipe_user = str(request.user)
                    recipe.save()
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
        form = RecipeForm()
        return render(
            request,
            'add_recipe.html',
            {
                'username': user.username,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'form': form,
                'ingredients': ingredients
            }
        )


@login_required(login_url='/login')
def recipe_detail(request, ing_id):
    user = UserModel.objects.get(username=request.user)
    recipe = RecipesModel.objects.get(recipe_user=str(request.user), id=ing_id)
    return render(
        request,
        'each_recipe_detail.html',
        {
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'recipe': recipe
        }
    )


@login_required(login_url='/login')
def edit_recipe(request, ing_id):
    recipe = RecipesModel.objects.get(recipe_user=str(request.user), id=ing_id)
    ingredients = Ingredients.objects.filter(username=request.user)
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
    options = ['Food', 'Labor', 'Packaging', 'UnCategorized']
    recipe_options = []
    for option in options:
        if option == recipe.recipe_category:
            continue
        else:
            recipe_options.append(option)
    if request.method == 'POST':
        print(request.POST)
        recipe_name = request.POST.get('recipe_name')
        try:
            if recipe_name == recipe.recipe_name:
                raise RecipesModel.DoesNotExist
            else:
                check_recipe = RecipesModel.objects.get(recipe_user=str(request.user),
                                                        recipe_name=recipe_name)
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
                        'fail': 'Recipe Name Already Exists'
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
                'unit_options': unit_options
            }
        )


@login_required(login_url='/login')
def ingredient_details(request, ing_id):
    ingredient = Ingredients.objects.get(username=request.user, id=ing_id)
    return render(
        request,
        'each_ingridient_detail.html',
        {
            'ingredient': ingredient
        }
    )


@login_required(login_url='/login')
def edit_ingredient(request, ing_id):
    ingredient = Ingredients.objects.get(username=request.user, id=ing_id)
    allergens_list = ['Cerly', 'Eggs', 'Fish', 'Milk']
    if ingredient.hasMajorAllergens:
        allergens = ingredient.majorAllergens
        print(allergens)
    else:
        allergens = None
    if ingredient.fromMeasurementData is None:
        has_measurments = False
        measurements = None
    else:
        has_measurments = True
        measurements = zip(ingredient.fromMeasurementData, ingredient.fromMeasurementUnits,
                           ingredient.toMeasurementData, ingredient.toMeasurementUnits)
    if request.method == 'POST':
        form = IngredientsForm(instance=ingredient, request=request, data=request.POST)
        if form.is_valid():
            print("Valid")
            print(request.POST)
            form.save()
            indredients = Ingredients.objects.get(username=request.user, name=form.cleaned_data['name'])
            if form.cleaned_data['suppliers'] == 'Add Supplier':
                indredients.suppliers = request.POST.get('customsupplier')
                indredients.save()
                form = IngredientsForm(instance=ingredient, request=request)
            ingMeasurementsData = request.POST.get('ingMeasurementsData')
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
                'allergens_list': allergens_list
            }
        )
    else:
        print(ingredient.fromMeasurementData)
        form = IngredientsForm(instance=ingredient, request=request)
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
                'allergens_list': allergens_list
            }
        )
