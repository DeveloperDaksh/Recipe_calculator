from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, redirect
from .forms import RegistrationForm, LoginForm
from django.utils.translation import gettext as _
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate

from .models import UserModel


def index_page(request):
    if request.user.is_authenticated:
        return redirect('/dashboard')
    else:
        return render(request, 'index_page.html', {'menu': 'index'})


def login_user(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('/dashboard')
            else:
                return render(
                    request,
                    'login.html',
                    {
                        'form': form,
                        'menu': 'login',
                        'fail': 'Invalid Username Or Password'
                    }
                )
        else:
            return render(
                request,
                'login.html',
                {
                    'form': form,
                    'menu': 'login',
                    'fail': 'Invalid Data'
                }
            )
    else:
        form = LoginForm()
        return render(request, 'login.html', {'form': form, 'menu': 'login'})


@login_required(login_url='/login')
def dashboard(request):
    return render(
        request,
        'dashboard.html',
        {'username': request.user}
    )


def create_user(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            email = form.cleaned_data['email']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            try:
                UserModel.objects.get(Q(username=username) | Q(email=email))
                return render(
                    request,
                    'register.html',
                    {
                        'form': form,
                        'menu': 'login',
                        'fail': 'User Or Email Already Exists'
                    }
                )
            except UserModel.DoesNotExist:
                user = UserModel.objects.create_user(
                    username=username,
                    password=password,
                    email=email
                )
                user.first_name = first_name
                user.last_name = last_name
                user.save()
                print(user.is_superuser)
                login(request, user)
                messages.success(request, _('Account created'))
                return redirect('/dashboard')
    else:
        form = RegistrationForm()
        return render(request, 'register.html', {'form': form, 'menu': 'create'})


def about_us(request):
    return render(request, 'about_page.html', {'menu': 'about'})


def contact_us(request):
    return render(request, 'contact_page.html', {'menu': 'contact'})


def help_us(request):
    return render(request, 'help_page.html', {'menu': 'help'})


@login_required(login_url='/login')
def user_logout(request):
    logout(request)
    return redirect('/')
