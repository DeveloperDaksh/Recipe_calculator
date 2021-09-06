from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import UpdateView
from django.utils.translation import gettext as _
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate

from .models import UserModel
from .forms import RegistrationForm, LoginForm, UpdateEmailForm, UpdateContactInfoForm, ForgetPasswordForm, \
    UserSettingsForm


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
    user = UserModel.objects.get(username=request.user)
    return render(
        request,
        'dashboard.html',
        {
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name
        }
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


@login_required(login_url='/login')
def getPersonalInfo(request):
    user = UserModel.objects.get(username=request.user)
    if request.method == 'POST':
        form = UserSettingsForm(request.POST)
        if form.is_valid():
            user.timezone = form.cleaned_data['timezone']
            user.save()
            form = UserSettingsForm()
            return render(
                request,
                'update_settings.html',
                {
                    'username': user.username,
                    'email': user.email,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'form': form,
                    'success': 'TimeZone Is Updated'
                }
            )
    else:
        form = UserSettingsForm()
        return render(
            request,
            'update_settings.html',
            {
                'username': user.username,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'form': form
            }
        )


class UpdateEmail(LoginRequiredMixin, UpdateView):
    model = UserModel
    form_class = UpdateEmailForm
    template_name = 'update_email.html'
    success_url = reverse_lazy('change_email')

    def get_object(self, queryset=None):
        return self.request.user


@login_required(login_url='/login')
def updatePassword(request):
    if request.method == 'POST':
        form = ForgetPasswordForm(request.POST)
        if form.is_valid():
            current_password = form.cleaned_data['current_password']
            userInfo = UserModel.objects.get(username=request.user)
            if userInfo.check_password(current_password):
                new_password = form.cleaned_data['new_password']
                confirm_password = form.cleaned_data['confirm_password']
                if new_password == confirm_password:
                    userInfo.set_password(new_password)
                    userInfo.save()
                    return render(
                        request,
                        'update_password.html',
                        {
                            'form': form,
                            'success': 'Password Updated Valid After Login Again'
                        }
                    )
                else:
                    return render(
                        request,
                        'update_password.html',
                        {
                            'form': form,
                            'fail': 'Password Not Matched'
                        }
                    )
            else:
                return render(
                    request,
                    'update_password.html',
                    {
                        'form': form,
                        'fail': 'Current Password is Not Matched'
                    }
                )

    else:
        form = ForgetPasswordForm()
        return render(
            request,
            'update_password.html',
            {
                'form': form
            }
        )


class UpdateContactInfo(LoginRequiredMixin, UpdateView):
    model = UserModel
    form_class = UpdateContactInfoForm
    template_name = 'contact_info.html'
    success_url = reverse_lazy('contactInfo')

    def get_object(self, queryset=None):
        return self.request.user


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
