from django.core.validators import RegexValidator, MaxLengthValidator
from django.db import models


class Company(models.Model):
    PREFERED_UNITS_CHOICES = [
        ('metric', 'metric'),
        ('imperial', 'imperial')
    ]

    user = models.CharField(max_length=225)
    name = models.CharField(max_length=225)
    billing_email = models.EmailField(max_length=225)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                                 message="Phone number must be entered in the format: '+999999999'. Up to 15 digits "
                                         "allowed.")
    phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True)
    address_one = models.CharField(max_length=225, blank=True)
    address_two = models.CharField(max_length=225, blank=True)
    city = models.CharField(max_length=225, blank=True)
    country = models.CharField(max_length=225, blank=True)
    postal_code = models.CharField(max_length=225, blank=True)
    preferred_units = models.CharField(max_length=225, blank=True, choices=PREFERED_UNITS_CHOICES)
    use_advanced_cal = models.BooleanField(default=False, blank=True)
    billing_country = models.CharField(max_length=225, blank=True)
    currency_codes = models.CharField(max_length=225, blank=True)
    round_currency = models.CharField(max_length=225, blank=True)
    display_currency = models.CharField(max_length=225, blank=True)
    own_currency = models.CharField(max_length=225, blank=True)
    decimal_mark = models.CharField(max_length=20, blank=True,
                                    validators=[MaxLengthValidator(5, message='accept length of 5')])
    thousands_separator = models.CharField(max_length=20, blank=True,
                                           validators=[MaxLengthValidator(5, message='accept length of 5')])


class Customers(models.Model):
    user = models.CharField(max_length=225)
    company_name = models.CharField(max_length=225)
    name = models.CharField(max_length=225)
    contact_first_name = models.CharField(max_length=225, blank=True)
    contact_last_name = models.CharField(max_length=225, blank=True)
    email = models.EmailField(max_length=225, blank=True)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                                 message="Phone number must be entered in the format: '+999999999'. Up to 15 digits "
                                         "allowed.")
    phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True)


class ShippingCarriers(models.Model):
    user = models.CharField(max_length=225)
    company_name = models.CharField(max_length=225)
    name = models.CharField(max_length=225)
    contact_first_name = models.CharField(max_length=225, blank=True)
    contact_last_name = models.CharField(max_length=225, blank=True)
    email = models.EmailField(max_length=225, blank=True)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                                 message="Phone number must be entered in the format: '+999999999'. Up to 15 digits "
                                         "allowed.")
    phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True)
