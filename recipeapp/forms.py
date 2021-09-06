import pytz
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext_lazy as _
from .models import UserModel


class UserForm(UserCreationForm):
    class Meta:
        model = UserModel
        fields = ('username', 'email', 'first_name', 'last_name')

    def save(self, commit=True):  # overrides method save
        user = super().save(commit=False)
        user.is_staff = False
        user.is_superuser = False
        if commit:
            user.save()
        return user


class LoginForm(forms.Form):
    username = forms.CharField(max_length=200, widget=forms.TextInput(
        attrs={'placeholder': 'Username'}))
    password = forms.CharField(max_length=200, widget=forms.PasswordInput(
        attrs={'placeholder': 'Password'}))


class RegistrationForm(forms.Form):
    first_name = forms.CharField(max_length=225, widget=forms.TextInput(
        attrs={'placeholder': 'FirstName'}))
    last_name = forms.CharField(max_length=225, widget=forms.TextInput(
        attrs={'placeholder': 'LastName'}))
    username = forms.CharField(max_length=225, widget=forms.TextInput(
        attrs={'placeholder': 'Username'}))
    password = forms.CharField(max_length=225, widget=forms.PasswordInput(
        attrs={'placeholder': 'Password'}))
    email = forms.EmailField(max_length=225, widget=forms.EmailInput(
        attrs={'placeholder': 'Email'}
    ))


class UpdateEmailForm(forms.ModelForm):
    email = forms.EmailField(max_length=225, widget=forms.EmailInput(
        attrs={'placeholder': 'Email'}
    ))

    class Meta:
        model = UserModel
        fields = ('email',)


class UpdateContactInfoForm(forms.ModelForm):
    first_name = forms.CharField(max_length=225, widget=forms.TextInput(
        attrs={'placeholder': 'FirstName'}))
    last_name = forms.CharField(max_length=225, widget=forms.TextInput(
        attrs={'placeholder': 'LastName'}))

    class Meta:
        model = UserModel
        fields = ('first_name', 'last_name')


class ForgetPasswordForm(forms.Form):
    current_password = forms.CharField(max_length=225, widget=forms.PasswordInput(
        attrs={'placeholder': 'Enter Current Password'}))
    new_password = forms.CharField(max_length=225, widget=forms.PasswordInput(
        attrs={'placeholder': 'Enter New Password'}))
    confirm_password = forms.CharField(max_length=225, widget=forms.PasswordInput(
        attrs={'placeholder': 'Confirm  New Password'}))


class UserSettingsForm(forms.Form):
    TIMEZONE_CHOICES = (('', '---------'),) + tuple(map(lambda tz: (tz, tz), pytz.common_timezones))

    timezone = forms.ChoiceField(
        choices=TIMEZONE_CHOICES,
        required=False,
        label=_('Timezone')
    )

    class Meta:
        model = UserModel
        fields = ('timezone',)
