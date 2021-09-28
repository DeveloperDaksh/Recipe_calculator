import pytz
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext_lazy as _

from .models import UserModel
from .models import FeedBack


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


class FeedBackForm(forms.ModelForm):
    feeling_choice = (
        ("I'm feeling happy", "I'm feeling happy"),
        ("I'm feeling sad", "I'm feeling sad"),
        ("I'm feeling frustrated", "I'm feeling frustrated"),
        ("I'm feeling confused", "I'm feeling confused"),
        ("I'm feeling happy", "I'm feeling happy"),
        ("I'm feeling intrigued", "I'm feeling intrigued"),
    )
    feeling = forms.ChoiceField(choices=feeling_choice, label=_('How are you feeling'))

    class Meta:
        model = FeedBack
        fields = ['feeling', 'suggestion']


class ForgetPassword(forms.Form):
    password = forms.CharField(max_length=225, widget=forms.PasswordInput(attrs={'placeholder': 'Enter New Password'}),
                               label='Password')
    conform_password = forms.CharField(max_length=225,
                                       widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password'}),
                                       label='Confirm Password')


class EmailForm(forms.Form):
    user_email = forms.EmailField(max_length=225, widget=forms.EmailInput(attrs={'placeholder': 'Enter Email'}),
                                  label='Enter Registered Email')
