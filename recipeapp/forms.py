from django import forms
from django.contrib.auth.forms import UserCreationForm
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
