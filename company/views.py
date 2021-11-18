import json
import io
import csv

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
from wsgiref.util import FileWrapper

from .models import Company, Customers, ShippingCarriers
from recipeapp.models import UserModel
from recipesandingredients.models import Ingredients, RecipesModel, IngredientCategories, NutritionDetails, \
    StorageAreas, Suppliers
from .forms import CompanyForm, CompanySettings, CurrencyDisplay, BillingCountry, DeleteForm, CustomerForm, \
    ShippingCarrierForm


# user creating a new company
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
            name_company = form.cleaned_data['name']
            try:
                # check weather the company name is exists in the current user
                company_check = Company.objects.get(user=request.user, name=name_company)
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
                        'fail': 'Company Name Already Exists'
                    }
                )
            except Company.DoesNotExist:
                # if the company name doesn't exists in current user it will create a company and switched to that company
                company_detail = form.save(commit=False)
                company_detail.user = request.user
                company_detail.save()
                request.session['company_name'] = company_detail.name
                # default it will create some categories in the ingredient when user creates a new company
                IngredientCategories.objects.create(
                    user=request.user.username,
                    company_name=request.session['company_name'],
                    category='Food',
                    category_type='ingredient'
                ).save()
                IngredientCategories.objects.create(
                    user=request.user.username,
                    company_name=request.session['company_name'],
                    category='Labor',
                    category_type='ingredient'
                ).save()
                IngredientCategories.objects.create(
                    user=request.user.username,
                    company_name=request.session['company_name'],
                    category='Packaging',
                    category_type='ingredient'
                ).save()
                IngredientCategories.objects.create(
                    user=request.user.username,
                    company_name=request.session['company_name'],
                    category='UnCategorized',
                    category_type='ingredient'
                ).save()
                # after creating a company it will redirect to the update page of the company
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


# when the user switched or changed his company it will store the company name in the session
@login_required(login_url='/login')
def save_company_name(request):
    if request.method == 'POST':
        name = request.POST.get('valueSelected')
        request.session['company_name'] = name
        return HttpResponse(json.dumps({'status': 'ok'}), content_type='application/json')


# updating the company information
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


# updating or modifying the settings of the company
@login_required(login_url='/login')
def company_settings(request):
    user = UserModel.objects.get(username=request.user)
    company_details = Company.objects.filter(user=request.user)
    if company_details.count() > 1:
        many_companies = True
    else:
        many_companies = False
    company_name = request.session.get('company_name')
    # setting contain 4 forms preferred units,currency display settings,company billing information,delete data in the company respectively
    company_instance = Company.objects.get(name=company_name, user=request.user)
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
                # checking the password is valid or not if valid it will delete data in the company
                if user.check_password(password):
                    ingredients_info = Ingredients.objects.filter(username=request.user, company_name=company_name)
                    recipe_info = RecipesModel.objects.filter(recipe_user=request.user, company_name=company_name)
                    ingredients_info.delete()
                    recipe_info.delete()
                    Customers.objects.filter(user=request.user.username, company_name=company_name).delete()
                    ShippingCarriers.objects.filter(user=request.user.username, company_name=company_name).delete()
                    IngredientCategories.objects.filter(user=request.user.username, company_name=company_name).delete()
                    NutritionDetails.objects.filter(user=request.user.username, company_name=company_name).delete()
                    StorageAreas.objects.filter(user=request.user.username, company_name=company_name).delete()
                    Suppliers.objects.filter(user=request.user.username,company_name=company_name).delete()
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


# display the subscription details
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


# list all the customers in the current company of the current user
@login_required(login_url='/login')
def customer_dashboard(request):
    user = UserModel.objects.get(username=request.user)
    company_details = Company.objects.filter(user=request.user)
    if company_details.count() > 1:
        many_companies = True
    else:
        many_companies = False
    company_name = request.session.get('company_name')
    customers = Customers.objects.filter(user=request.user, company_name=company_name)
    return render(
        request,
        'customers.html',
        {
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'many_companies': many_companies,
            'company_details': company_details,
            'company_name': company_name,
            'customers': customers
        }
    )


# creates a new customer in the current company
@login_required(login_url='/login')
def new_customer(request):
    user = UserModel.objects.get(username=request.user)
    company_details = Company.objects.filter(user=request.user)
    if company_details.count() > 1:
        many_companies = True
    else:
        many_companies = False
    company_name = request.session.get('company_name')
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            try:
                # check if the customer name is exists in the current company of that user
                check_customer = Customers.objects.get(user=request.user, company_name=company_name,
                                                       name=form.cleaned_data['name'])
                return render(
                    request,
                    'customer_new.html',
                    {
                        'username': user.username,
                        'email': user.email,
                        'first_name': user.first_name,
                        'last_name': user.last_name,
                        'many_companies': many_companies,
                        'company_details': company_details,
                        'company_name': company_name,
                        'form': form,
                        'fail': 'Customer Name Already exists'
                    }
                )
            except Customers.DoesNotExist:
                # if the customer name doesn't exists it will create a new customer with the given details
                customer = form.save(commit=False)
                customer.user = request.user
                customer.company_name = company_name
                customer.save()
                return redirect('/company/customers')
        else:
            return render(
                request,
                'customer_new.html',
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
        form = CustomerForm()
        return render(
            request,
            'customer_new.html',
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


# display the details of the particular customer that the user selected
@login_required(login_url='/login')
def each_customer(request, customer_id):
    user = UserModel.objects.get(username=request.user)
    company_details = Company.objects.filter(user=request.user)
    if company_details.count() > 1:
        many_companies = True
    else:
        many_companies = False
    company_name = request.session.get('company_name')
    customer = Customers.objects.get(id=customer_id)
    return render(
        request,
        'each_customer_info.html',
        {
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'many_companies': many_companies,
            'company_details': company_details,
            'company_name': company_name,
            'customer': customer
        }
    )


# edit or update the details of the particular customer
@login_required(login_url='/login')
def edit_customer(request, customer_id):
    user = UserModel.objects.get(username=request.user)
    company_details = Company.objects.filter(user=request.user)
    if company_details.count() > 1:
        many_companies = True
    else:
        many_companies = False
    company_name = request.session.get('company_name')
    customer_instance = Customers.objects.get(id=customer_id)
    if request.method == 'POST':
        form = CustomerForm(instance=customer_instance, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('/company/customers/edit/' + str(customer_id))
        else:
            return render(
                request,
                'customer_edit.html',
                {
                    'username': user.username,
                    'email': user.email,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'many_companies': many_companies,
                    'company_details': company_details,
                    'company_name': company_name,
                    'form': form,
                    'customer': customer_instance
                }
            )
    else:
        form = CustomerForm(instance=customer_instance)
        return render(
            request,
            'customer_edit.html',
            {
                'username': user.username,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'many_companies': many_companies,
                'company_details': company_details,
                'company_name': company_name,
                'form': form,
                'customer': customer_instance
            }
        )


# delete particular customer
@login_required(login_url='/login')
def delete_customer(request, customer_id):
    customer_instance = Customers.objects.get(id=customer_id)
    customer_instance.delete()
    return redirect('/company/customers')


# download all the customers in the current company of the curent user
@login_required(login_url='/login')
def download_customers(request):
    company_name = request.session.get('company_name')
    customers = Customers.objects.filter(user=request.user, company_name=company_name)
    fields = ['Name', 'First Name', 'Last Name', 'Email', 'Phone Number']
    data = []
    for customer in customers:
        data.append([customer.name, customer.contact_first_name, customer.contact_last_name, customer.email,
                     customer.phone_number])
    file = io.StringIO()
    writer = csv.writer(file, delimiter=',')
    writer.writerow(fields)
    writer.writerows(data)
    csv_data = file.getvalue()
    final_data = csv_data.encode('utf-8')
    byte_io = io.BytesIO(final_data)
    response = HttpResponse(FileWrapper(byte_io), content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=Customers.csv'
    return response


# display all the shipping carriers in current company of current user
@login_required(login_url='/login')
def shipping_carriers_dashboard(request):
    user = UserModel.objects.get(username=request.user)
    company_details = Company.objects.filter(user=request.user)
    if company_details.count() > 1:
        many_companies = True
    else:
        many_companies = False
    company_name = request.session.get('company_name')
    shipping_carriers = ShippingCarriers.objects.filter(user=request.user, company_name=company_name)
    return render(
        request,
        'shipping_carriers.html',
        {
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'many_companies': many_companies,
            'company_details': company_details,
            'company_name': company_name,
            'shipping_carriers': shipping_carriers
        }
    )


# create a new shipping carrier in current company
@login_required(login_url='/login')
def new_shipping_carrier(request):
    user = UserModel.objects.get(username=request.user)
    company_details = Company.objects.filter(user=request.user)
    if company_details.count() > 1:
        many_companies = True
    else:
        many_companies = False
    company_name = request.session.get('company_name')
    if request.method == 'POST':
        form = ShippingCarrierForm(request.POST)
        if form.is_valid():
            try:
                # check if the shipping carrier name is exists in the current company of that user
                check_shipping = ShippingCarriers.objects.get(user=request.user, company_name=company_name,
                                                              name=form.cleaned_data['name'])
                return render(
                    request,
                    'shipping_carriers_new.html',
                    {
                        'username': user.username,
                        'email': user.email,
                        'first_name': user.first_name,
                        'last_name': user.last_name,
                        'many_companies': many_companies,
                        'company_details': company_details,
                        'company_name': company_name,
                        'form': form,
                        'fail': 'Shipping Carrier Name Already exists'
                    }
                )
            except ShippingCarriers.DoesNotExist:
                # if the customer name doesn't exists it will create a new customer with the given details
                shipping_carrier = form.save(commit=False)
                shipping_carrier.user = request.user
                shipping_carrier.company_name = company_name
                shipping_carrier.save()
                return redirect('/company/shipping-carriers')
        else:
            return render(
                request,
                'shipping_carriers_new.html',
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
        form = ShippingCarrierForm()
        return render(
            request,
            'shipping_carriers_new.html',
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


# display details of a particular shipping carrier
@login_required(login_url='/login')
def each_shipping_carrier(request, shipping_id):
    user = UserModel.objects.get(username=request.user)
    company_details = Company.objects.filter(user=request.user)
    if company_details.count() > 1:
        many_companies = True
    else:
        many_companies = False
    company_name = request.session.get('company_name')
    shipping_carrier = ShippingCarriers.objects.get(id=shipping_id)
    return render(
        request,
        'each_shipping_carrier_info.html',
        {
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'many_companies': many_companies,
            'company_details': company_details,
            'company_name': company_name,
            'shipping_carrier': shipping_carrier
        }
    )


# edit or update the details of the shipping carriers
@login_required(login_url='/login')
def edit_shipping_carrier(request, shipping_id):
    user = UserModel.objects.get(username=request.user)
    company_details = Company.objects.filter(user=request.user)
    if company_details.count() > 1:
        many_companies = True
    else:
        many_companies = False
    company_name = request.session.get('company_name')
    shipping_instance = ShippingCarriers.objects.get(id=shipping_id)
    if request.method == 'POST':
        form = ShippingCarrierForm(instance=shipping_instance, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('/company/shipping-carriers/edit/' + str(shipping_id))
        else:
            return render(
                request,
                'shipping_carriers_edit.html',
                {
                    'username': user.username,
                    'email': user.email,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'many_companies': many_companies,
                    'company_details': company_details,
                    'company_name': company_name,
                    'form': form,
                    'shipping_carrier': shipping_instance
                }
            )
    else:
        form = ShippingCarrierForm(instance=shipping_instance)
        return render(
            request,
            'shipping_carriers_edit.html',
            {
                'username': user.username,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'many_companies': many_companies,
                'company_details': company_details,
                'company_name': company_name,
                'form': form,
                'shipping_carrier': shipping_instance
            }
        )


# delete particular shipping carrier
@login_required(login_url='/login')
def delete_shipping_carrier(request, shipping_id):
    shipping_instance = ShippingCarriers.objects.get(id=shipping_id)
    shipping_instance.delete()
    return redirect('/company/shipping-carriers')


# downloads the shipping carriers in the current company of the current user
@login_required(login_url='/login')
def download_shipping_carriers(request):
    company_name = request.session.get('company_name')
    shipping_carriers = ShippingCarriers.objects.filter(user=request.user, company_name=company_name)
    fields = ['Name', 'First Name', 'Last Name', 'Email', 'Phone Number']
    data = []
    for shipping_carrier in shipping_carriers:
        data.append([shipping_carrier.name, shipping_carrier.contact_first_name, shipping_carrier.contact_last_name,
                     shipping_carrier.email,
                     shipping_carrier.phone_number])
    file = io.StringIO()
    writer = csv.writer(file, delimiter=',')
    writer.writerow(fields)
    writer.writerows(data)
    csv_data = file.getvalue()
    final_data = csv_data.encode('utf-8')
    byte_io = io.BytesIO(final_data)
    response = HttpResponse(FileWrapper(byte_io), content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=ShippingCarriers.csv'
    return response
