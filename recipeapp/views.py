from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import UpdateView
from django.utils.translation import gettext as _
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from rest_framework.authtoken.models import Token
from django.conf import settings
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Email, To
from django.contrib.auth.models import User

from .models import UserModel
from company.models import Company
from recipesandingredients.models import IngredientCategories
from .forms import RegistrationForm, LoginForm, UpdateEmailForm, UpdateContactInfoForm, ForgetPasswordForm, \
    UserSettingsForm, FeedBackForm, EmailForm, ForgetPassword


# landing page
def index_page(request):
    if request.user.is_authenticated:
        return redirect('/dashboard')
    else:
        return render(request, 'index_page.html', {'menu': 'index'})


# checking if the user is authorized user or not if authorized it will redirect to user's dashboard
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
    company_details = Company.objects.filter(user=request.user)
    print(company_details.count())
    if request.session.has_key('company_name'):
        company_name = request.session['company_name']
    else:
        request.session['company_name'] = user.first_name + ' ' + user.last_name + "'s Company"
        company_name = request.session['company_name']
    if company_details.count() > 1:
        many_companies = True
    else:
        many_companies = False
    return render(
        request,
        'dashboard.html',
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
                login(request, user)
                company_new = Company.objects.create(
                    user=username,
                    name=first_name + ' ' + last_name + "'s Company",
                    billing_email=email
                )
                company_new.save()
                request.session['company_name'] = first_name + ' ' + last_name + "'s Company"
                IngredientCategories.objects.create(
                    user=username,
                    company_name=request.session['company_name'],
                    category='Food',
                    category_type='ingredient'
                ).save()
                IngredientCategories.objects.create(
                    user=username,
                    company_name=request.session['company_name'],
                    category='Labor',
                    category_type='ingredient'
                ).save()
                IngredientCategories.objects.create(
                    user=username,
                    company_name=request.session['company_name'],
                    category='Packaging',
                    category_type='ingredient'
                ).save()
                IngredientCategories.objects.create(
                    user=username,
                    company_name=request.session['company_name'],
                    category='UnCategorized',
                    category_type='ingredient'
                ).save()
                messages.success(request, _('Account created'))
                return redirect('/dashboard')
    else:
        form = RegistrationForm()
        return render(request, 'register.html', {'form': form, 'menu': 'create'})


@login_required(login_url='/login')
def getPersonalInfo(request):
    user = UserModel.objects.get(username=request.user)
    company_details = Company.objects.filter(user=request.user)
    if company_details.count() > 1:
        many_companies = True
    else:
        many_companies = False
    company_name = request.session['company_name']
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
                    'many_companies': many_companies,
                    'company_details': company_details,
                    'company_name': company_name,
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
                'form': form,
                'many_companies': many_companies,
                'company_details': company_details,
                'company_name': company_name
            }
        )


class UpdateEmail(LoginRequiredMixin, UpdateView):
    model = UserModel
    form_class = UpdateEmailForm
    template_name = 'update_email.html'
    success_url = reverse_lazy('change_email')

    def get_context_data(self, **kwargs):
        context = super(UpdateEmail, self).get_context_data(**kwargs)
        user = UserModel.objects.get(username=self.request.user)
        company_details = Company.objects.filter(user=self.request.user)
        company_name = self.request.session['company_name']
        if company_details.count() > 1:
            many_companies = True
        else:
            many_companies = False
        context['username'] = user.username
        context['first_name'] = user.first_name
        context['last_name'] = user.last_name
        context['email'] = user.email
        context['many_companies'] = many_companies
        context['company_details'] = company_details
        context['company_name'] = company_name
        return context

    def get_object(self, queryset=None):
        return self.request.user


@login_required(login_url='/login')
def updatePassword(request):
    user = UserModel.objects.get(username=request.user)
    company_details = Company.objects.filter(user=request.user)
    if company_details.count() > 1:
        many_companies = True
    else:
        many_companies = False
    company_name = request.session['company_name']
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
                            'success': 'Password Updated Valid After Login Again',
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
                    return render(
                        request,
                        'update_password.html',
                        {
                            'form': form,
                            'fail': 'Password Not Matched',
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
                return render(
                    request,
                    'update_password.html',
                    {
                        'form': form,
                        'fail': 'Current Password is Not Matched',
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
        form = ForgetPasswordForm()
        return render(
            request,
            'update_password.html',
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


class UpdateContactInfo(LoginRequiredMixin, UpdateView):
    model = UserModel
    form_class = UpdateContactInfoForm
    template_name = 'contact_info.html'
    success_url = reverse_lazy('contactInfo')

    def get_context_data(self, **kwargs):
        context = super(UpdateContactInfo, self).get_context_data(**kwargs)
        user = UserModel.objects.get(username=self.request.user)
        company_details = Company.objects.filter(user=self.request.user)
        if company_details.count() > 1:
            many_companies = True
        else:
            many_companies = False
        company_name = self.request.session['company_name']
        context['username'] = user.username
        context['first_name'] = user.first_name
        context['last_name'] = user.last_name
        context['email'] = user.email
        context['many_companies'] = many_companies
        context['company_details'] = company_details
        context['company_name'] = company_name
        return context

    def get_object(self, queryset=None):
        return self.request.user


@login_required(login_url='/login')
def user_feedback(request):
    user = UserModel.objects.get(username=request.user)
    company_details = Company.objects.filter(user=request.user)
    if company_details.count() > 1:
        many_companies = True
    else:
        many_companies = False
    company_name = request.session['company_name']
    if request.method == 'POST':
        form = FeedBackForm(request.POST)
        if form.is_valid():
            form.save()
            form = FeedBackForm()
            return render(
                request,
                'feed_back.html',
                {
                    'form': form,
                    'username': user.username,
                    'email': user.email,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'success': 'Thanks For your Valuable feedback',
                    'many_companies': many_companies,
                    'company_details': company_details,
                    'company_name': company_name
                }
            )

    else:
        form = FeedBackForm()
        return render(
            request,
            'feed_back.html',
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


def forget_password(request):
    if request.method == 'POST':
        form = EmailForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['user_email']
            try:
                user = UserModel.objects.get(email=email)
                try:
                    authToken = Token.objects.get(user_id=user.id)
                    return render(
                        request,
                        'forget_password.html',
                        {
                            'form': form,
                            'fail': 'Email Already Sent to ' + email
                        }
                    )
                except Token.DoesNotExist:
                    token_generation = Token.objects.create(user_id=user.id)
                    token_generation.save()
                    authToken = Token.objects.get(user_id=user.id)
                    authKey = authToken.key
                    try:
                        sg = SendGridAPIClient(settings.SENDGRID_EMAIL_API)
                        message = Mail(
                            from_email=Email(settings.FROM_EMAIL),
                            to_emails=To(email),
                            subject='Password Reset For Recipe Cost Calculator',
                            html_content='<a href="https://recipecostdemo.herokuapp.com/update-password/' + authKey + '"><input '
                                                                                                                      'type="submit" '
                                                                                                                      'value="Reset '
                                                                                                                      'Password"></a> '
                        )
                        response = sg.send(message)
                        print(response.status_code)
                        form = EmailForm()
                        return render(
                            request,
                            'forget_password.html',
                            {
                                'form': form,
                                'success': 'Password reset link sent to  ' + email
                            }
                        )
                    except Exception:
                        return render(
                            request,
                            'forget_password.html',
                            {
                                'form': form,
                                'fail': 'An Error Occurred '
                            }
                        )
            except UserModel.DoesNotExist:
                return render(
                    request,
                    'forget_password.html',
                    {
                        'form': form,
                        'fail': 'Please Enter Registered Email'
                    }
                )
        else:
            return render(
                request,
                'forget_password.html',
                {
                    'form': form,
                    'fail': 'Invalid Data'
                }
            )
    else:
        form = EmailForm()
        return render(
            request,
            'forget_password.html',
            {
                'form': form
            }
        )


def update_password(request, token):
    try:
        user_token = Token.objects.get(key=token)
        if request.method == 'POST':
            form = ForgetPassword(request.POST)
            if form.is_valid():
                password = form.cleaned_data['password']
                cpassword = form.cleaned_data['conform_password']
                if password == cpassword:
                    print(user_token)
                    print(user_token.user)
                    user = UserModel.objects.get(username=user_token.user)
                    user.set_password(password)
                    user.save()
                    user_token.delete()
                    return render(
                        request,
                        'update_forget_password.html',
                        {
                            'success': 'Password Updated',
                            'expires': False
                        }
                    )
                else:
                    form = ForgetPassword()
                    return render(
                        request,
                        'update_forget_password.html',
                        {
                            'fail': 'Password not Matched',
                            'expires': False,
                            'form': form
                        }
                    )
        else:
            form = ForgetPassword()
            return render(
                request,
                'update_forget_password.html',
                {'expires': False, 'form': form}
            )
    except Token.DoesNotExist:
        return render(
            request,
            'update_forget_password.html',
            {'expires': True}
        )


def about_us(request):
    return render(request, 'about_page.html', {'menu': 'about'})


def contact_us(request):
    return render(request, 'contact_page.html', {'menu': 'contact'})


def help_us(request):
    return render(request, 'help_page.html', {'menu': 'help'})


@login_required(login_url='/login')
def user_logout(request):
    logout(request)
    for key in request.session.keys():
        del request.session[key]
    return redirect('/')
