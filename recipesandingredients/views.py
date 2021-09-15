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
        print(form)
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
                    print(ingdata)
                    print(fromdata)
                    print(fromunits)
                    print(todata)
                    print(tounits)
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
                checkingridient = RecipesModel.objects.get(recipe_user=str(request.user),
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
    return render(
        request,
        'edit_recipe.html'
    )
