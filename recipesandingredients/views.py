from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, redirect
from recipeapp.models import UserModel
from .forms import IngredientsForm
from .models import Ingredients


@login_required(login_url='/login')
def handleIngredients(request):
    if request.method == 'POST':
        form = IngredientsForm(request=request, data=request.POST)
        print(form.is_valid())
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
                if form.cleaned_data['suppliers'] == 'Add Supplier':
                    indredients = Ingredients.objects.get(username=request.user, name=form.cleaned_data['name'])
                    indredients.suppliers = request.POST.get('customsupplier')
                    indredients.save()
                    print("Saved Suppliers")
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
