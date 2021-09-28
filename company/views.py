import json

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect

from .models import Company
from recipeapp.models import UserModel
from recipesandingredients.models import Ingredients,RecipesModel
from .forms import CompanyForm, CompanySettings, CurrencyDisplay, BillingCountry,DeleteForm


@login_required(login_url='/login')
def create_company(request):
    user = UserModel.objects.get(username=request.user)
    company_details = Company.objects.filter(user=request.user)
    if company_details.count() > 1:
        many_companies = True
    else:
        many_companies = False
    company_name = request.session.get('company_name')
    if request.method == 'POST':
        form = CompanyForm(request.POST)
        if form.is_valid():
            company_detail = form.save(commit=False)
            company_detail.user = request.user
            company_detail.save()
            print(company_detail.name)
            request.session['company_name'] = company_detail.name
            return redirect('/company/edit')
        else:
            return render(
                request,
                'company_new.html',
                {
                    'form': form,
                    'username': user.username,
                    'email': user.email,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'many_companies': many_companies,
                    'company_details': company_details,
                    'company_name': company_name,
                    'fail': 'Invalid Data'
                }
            )
    else:
        form = CompanyForm()
        return render(
            request,
            'company_new.html',
            {
                'form': form,
                'username': user.username,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'many_companies': many_companies,
                'company_details': company_details,
                'company_name': company_name,
            }
        )


@login_required(login_url='/login')
def save_company_name(request):
    if request.method == 'POST':
        name = request.POST.get('valueSelected')
        print(name)
        request.session['company_name'] = name
        return HttpResponse(json.dumps({'status': 'ok'}), content_type='application/json')


@login_required(login_url='/login')
def edit_company(request):
    user = UserModel.objects.get(username=request.user)
    company_details = Company.objects.filter(user=request.user)
    if company_details.count() > 1:
        many_companies = True
    else:
        many_companies = False
    company_name = request.session.get('company_name')
    company_detail = Company.objects.get(user=request.user, name=company_name)
    if request.method == 'POST':
        form = CompanyForm(instance=company_detail, data=request.POST)
        if form.is_valid():
            form.save()
            request.session['company_name'] = company_detail.name
            return render(
                request,
                'company_info.html',
                {
                    'form': form,
                    'username': user.username,
                    'email': user.email,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'many_companies': many_companies,
                    'company_details': company_details,
                    'company_name': company_name,
                }
            )
    else:
        form = CompanyForm(instance=company_detail)
        return render(
            request,
            'company_info.html',
            {
                'form': form,
                'username': user.username,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'many_companies': many_companies,
                'company_details': company_details,
                'company_name': company_name,
            }
        )


@login_required(login_url='/login')
def company_settings(request):
    user = UserModel.objects.get(username=request.user)
    company_details = Company.objects.filter(user=request.user)
    if company_details.count() > 1:
        many_companies = True
    else:
        many_companies = False
    company_name = request.session.get('company_name')
    company_instance = Company.objects.get(name=company_name,user=request.user)
    form1 = CompanySettings(instance=company_instance)
    form2 = CurrencyDisplay(instance=company_instance,
                            initial={'display_currency': 'before', 'round_currency': 'No'})
    form3 = BillingCountry(instance=company_instance)
    form4 = DeleteForm()
    if request.method == 'POST':
        if 'currency_codes' in request.POST or 'display_currency' in request.POST or 'round_currency' in request.POST:
            form2 = CurrencyDisplay(instance=company_instance, data=request.POST)
            print(form2.is_valid())
            if form2.is_valid():
                form2.save()
            else:
                return render(
                    request,
                    'company_settings.html',
                    {
                        'username': user.username,
                        'email': user.email,
                        'first_name': user.first_name,
                        'last_name': user.last_name,
                        'many_companies': many_companies,
                        'company_details': company_details,
                        'company_name': company_name,
                        'form1': form1,
                        'form2': form2,
                        'form3': form3,
                        'form4': form4
                    }
                )
        if 'preferred_units' in request.POST or 'use_advanced_cal' in request.POST:
            form1 = CompanySettings(instance=company_instance, data=request.POST)
            print(form1.is_valid())
            if form1.is_valid():
                form1.save()
            else:
                return render(
                    request,
                    'company_settings.html',
                    {
                        'username': user.username,
                        'email': user.email,
                        'first_name': user.first_name,
                        'last_name': user.last_name,
                        'many_companies': many_companies,
                        'company_details': company_details,
                        'company_name': company_name,
                        'form1': form1,
                        'form2': form2,
                        'form3': form3,
                        'form4': form4
                    }
                )
        if 'billing_country' in request.POST:
            form3 = BillingCountry(instance=company_instance, data=request.POST)
            print(form3.is_valid())
            if form3.is_valid():
                form3.save()
            else:
                return render(
                    request,
                    'company_settings.html',
                    {
                        'username': user.username,
                        'email': user.email,
                        'first_name': user.first_name,
                        'last_name': user.last_name,
                        'many_companies': many_companies,
                        'company_details': company_details,
                        'company_name': company_name,
                        'form1': form1,
                        'form2': form2,
                        'form3': form3,
                        'form4': form4
                    }
                )
        if 'password' in request.POST:
            form4 = DeleteForm(request.POST)
            if form4.is_valid():
                password = form4.cleaned_data['password']
                form4 = DeleteForm()
                if user.check_password(password):
                    ingredients_info = Ingredients.objects.filter(username=request.user,company_name=company_name)
                    recipe_info = RecipesModel.objects.filter(recipe_user=request.user,company_name=company_name)
                    ingredients_info.delete()
                    recipe_info.delete()
                    return render(
                        request,
                        'company_settings.html',
                        {
                            'username': user.username,
                            'email': user.email,
                            'first_name': user.first_name,
                            'last_name': user.last_name,
                            'many_companies': many_companies,
                            'company_details': company_details,
                            'company_name': company_name,
                            'form1': form1,
                            'form2': form2,
                            'form3': form3,
                            'form4': form4,
                            'success': 'All the data in the company is deleted'
                        }
                    )
                else:
                    return render(
                        request,
                        'company_settings.html',
                        {
                            'username': user.username,
                            'email': user.email,
                            'first_name': user.first_name,
                            'last_name': user.last_name,
                            'many_companies': many_companies,
                            'company_details': company_details,
                            'company_name': company_name,
                            'form1': form1,
                            'form2': form2,
                            'form3': form3,
                            'form4': form4,
                            'fail': 'Invalid Password'
                        }
                    )
        return redirect('/company/settings')
    else:
        print(company_instance.preferred_units)
        return render(
            request,
            'company_settings.html',
            {
                'username': user.username,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'many_companies': many_companies,
                'company_details': company_details,
                'company_name': company_name,
                'form1': form1,
                'form2': form2,
                'form3': form3,
                'form4': form4
            }
        )


@login_required(login_url='/login')
def view_subscription(request):
    user = UserModel.objects.get(username=request.user)
    company_details = Company.objects.filter(user=request.user)
    if company_details.count() > 1:
        many_companies = True
    else:
        many_companies = False
    company_name = request.session.get('company_name')
    return render(
        request,
        'subscription_page.html',
        {
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'many_companies': many_companies,
            'company_details': company_details,
            'company_name': company_name,
        }
    )
