from django.db import models
from django.contrib.postgres.fields import ArrayField


class Ingredients(models.Model):
    Category_Choices = [
        ("Food", "Food"),
        ("Labor", "Labor"),
        ("Packaging", "Packaging"),
        ("UnCategorized", "UnCategorized")
    ]

    qtyUnits_Choices = CHOICES = (
        ('-- Weight --',
         (
             ('Ounce (oz) (28.35 g)', 'Ounce (oz) (28.35 g)'),
             ('Pound (lb) (453.59 g)', 'Pound (lb) (453.59 g)'),
             ('Kilogram (Kg) (1000 g)', 'Kilogram (Kg) (1000 g)'),
             ('Tonne (T) (1000000 g)', 'Tonne (T) (1000000 g)'),
             ('Gram (g)', 'Gram (g)')
         )
         ),
        ('-- Volume --',
         (
             ('Pinch (pinch) (0.3 ml)', 'Pinch (pinch) (0.3 ml)'),
             ('US Teaspoon (tsp) (4.93 ml)', 'US Teaspoon (tsp) (4.93 ml)'),
             ('US Tablespoon (tbsp) (14.79 ml)', 'US Tablespoon (tbsp) (14.79 ml)'),
             ('Fluid-ounce (floz) (29.57 ml)', 'Fluid-ounce (floz) (29.57 ml)'),
             ('Deciliter (dL) (100 ml)', 'Deciliter (dL) (100 ml)'),
             ('US Cup (cup) (236.59 ml)', 'US Cup (cup) (236.59 ml)'),
             ('Pint (pt) (473.18 ml)', 'Pint (pt) (473.18 ml)'),
             ('Milliliter (ml)', 'Milliliter (ml)'),
             ('Quart (qt) (946.35 ml)', 'Quart (qt) (946.35 ml)'),
             ('Liter (L) (1000 ml)', 'Liter (L) (1000 ml)'),
             ('Gallon (gal) (3785.41 ml)', 'Gallon (gal) (3785.41 ml)'),
             ('Cubic Meter (kl) (1000000 ml)', 'Cubic Meter (kl) (1000000 ml)'),
             ('Each (each)', 'Each (each)')
         )
         ),
        ('-- Quantity --',
         (
             ('Dozen (dozen) (12 each)', 'Dozen (dozen) (12 each)'),
             ('Hundred (hundred) (100 each)', 'Hundred (hundred) (100 each)'),
             ('Thousand (thousand) (1000 each)', 'Thousand (thousand) (1000 each)'),
             ('Million (million) (1000000 each)', 'Million (million) (1000000 each)')
         )
         ),
        ('-- Time --',
         (
             ('Second (s)', 'Second (s)'),
             ('Minute (min) (60 s)', 'Minute (min) (60 s)'),
             ('Hour (hr) (3600 s)', 'Hour (hr) (3600 s)'),
         )
         ),
    )

    Country_Of_Origin = [
        ('Afghanistan', 'Afghanistan'), ('Canada', 'Canada'), ('United States', 'United States'),
        ('Aland Islands', 'Aland Islands'), ('Albania', 'Albania'), ('Algeria', 'Algeria'),
        ('Austria', 'Austria'), ('Andorra', 'Andorra'), ('Angola', 'Angola'), ('Anguilla', 'Anguilla'),
        ('Antarctica', 'Antarctica'), ('Antigua and Barbuda', 'Antigua and Barbuda'), ('Argentina', 'Argentina'),
        ('Armenia', 'Armenia'), ('Aruba', 'Aruba'), ('American Samoa', 'American Samoa'), ('Australia', 'Australia'),
        ('Azerbaijan', 'Azerbaijan'), ('Bahamas', 'Bahamas'), ('Bahrain', 'Bahrain'), ('Barbados', 'Barbados'),
        ('Bangladesh', 'Bangladesh'), ('Belarus', 'Belarus'), ('Belgium', 'Belgium'), ('Belize', 'Belize'),
        ('Benin', 'Benin'), ('Bermuda', 'Bermuda'), ('Bhutan', 'Bhutan'), ('Botswana', 'Botswana'),
        ('Brazil', 'Brazil'), ('British Indian Ocean Territory', 'British Indian Ocean Territory'),
        ('Bolivia, Plurinational State of', 'Bolivia, Plurinational State of'), ('Bouvet Island', 'Bouvet Island'),
        ('Bonaire, Sint Eustatius and Saba', 'Bonaire, Sint Eustatius and Saba'), ('Bulgaria', 'Bulgaria'),
        ('Burkina Faso', 'Burkina Faso'), ('Burundi', 'Burundi'), ('Brunei Darussalam', 'Brunei Darussalam'),
        ('Bosnia and Herzegovina', 'Bosnia and Herzegovina'), ('Cambodia', 'Cambodia'), ('Cameroon', 'Cameroon'),
        ('Canada', 'Canada'), ('Cape Verde', 'Cape Verde'), ('Cayman Islands', 'Cayman Islands'), ('Chad', 'Chad'),
        ('Central African Republic', 'Central African Republic'), ('Chile', 'Chile'), ('China', 'China'),
        ('Christmas Island', 'Christmas Island'), ('Cocos (Keeling) Islands', 'Cocos (Keeling) Islands'),
        ('Colombia', 'Colombia'), ('Comoros', 'Comoros'), ('Congo', 'Congo'), ('Cook Islands', 'Cook Islands'),
        ('Congo, The Democratic Republic of the', 'Congo, The Democratic Republic of the'),
        ('Costa Rica', 'Costa Rica'), ('Curaçao', 'Curaçao'), ('Cyprus', 'Cyprus'), ('Denmark', 'Denmark'),
        ('Czech Republic', 'Czech Republic'), ("Côte d'Ivoire", "Côte d'Ivoire"), ('Croatia', 'Croatia'),
        ('Cuba', 'Cuba'), ('Djibouti', 'Djibouti'), ('Dominica', 'Dominica'),
        ('Dominican Republic', 'Dominican Republic'), ('Ecuador', 'Ecuador'), ('Egypt', 'Egypt'),
        ('El Salvador', 'El Salvador'), ('Equatorial Guinea', 'Equatorial Guinea'), ('Eritrea', 'Eritrea'),
        ('Estonia', 'Estonia'), ('Ethiopia', 'Ethiopia'), ('Faroe Islands', 'Faroe Islands'), ('Fiji', 'Fiji'),
        ('Falkland Islands (Malvinas)', 'Falkland Islands (Malvinas)'), ('Finland', 'Finland'), ('France', 'France'),
        ('French Guiana', 'French Guiana'), ('French Polynesia', 'French Polynesia'), ('Gabon', 'Gabon'),
        ('French Southern Territories', 'French Southern Territories'), ('Gambia', 'Gambia'), ('Georgia', 'Georgia'),
        ('Germany', 'Germany'), ('Ghana', 'Ghana'), ('Gibraltar', 'Gibraltar'), ('Greece', 'Greece'),
        ('Greenland', 'Greenland'), ('Grenada', 'Grenada'), ('Guadeloupe', 'Guadeloupe'), ('Guam', 'Guam'),
        ('Guatemala', 'Guatemala'), ('Guernsey', 'Guernsey'), ('Guinea', 'Guinea'), ('Guinea-Bissau', 'Guinea-Bissau'),
        ('Guyana', 'Guyana'), ('Haiti', 'Haiti'), ('Honduras', 'Honduras'), ('Hong Kong', 'Hong Kong'),
        ('Hungary', 'Hungary'), ('Holy See (Vatican City State)', 'Holy See (Vatican City State)'),
        ('Heard Island and McDonald Islands', 'Heard Island and McDonald Islands'), ('Iceland', 'Iceland'),
        ('India', 'India'), ('Indonesia', 'Indonesia'), ('Iran, Islamic Republic of', 'Iran, Islamic Republic of'),
        ('Iraq', 'Iraq'), ('Ireland', 'Ireland'), ('Isle of Man', 'Isle of Man'), ('Israel', 'Israel'),
        ('Italy', 'Italy'), ('Jamaica', 'Jamaica'), ('Japan', 'Japan'), ('Jersey', 'Jersey'), ('Jordan', 'Jordan'),
        ('Kazakhstan', 'Kazakhstan'), ('Kenya', 'Kenya'), ('Kiribati', 'Kiribati'), ('Kuwait', 'Kuwait'),
        ("Korea, Democratic People's Republic of", "Korea, Democratic People's Republic of"),
        ('Kyrgyzstan', 'Kyrgyzstan'), ('Korea, Republic of', 'Korea, Republic of'), ('Latvia', 'Latvia'),
        ("Lao People's Democratic Republic", "Lao People's Democratic Republic"), ('Lebanon', 'Lebanon'),
        ('Lesotho', 'Lesotho'), ('Liberia', 'Liberia'), ('Libya', 'Libya'), ('Liechtenstein', 'Liechtenstein'),
        ('Lithuania', 'Lithuania'), ('Luxembourg', 'Luxembourg'), ('Macao', 'Macao'), ('Malawi', 'Malawi'),
        ('Macedonia, Republic of', 'Macedonia, Republic of'), ('Madagascar', 'Madagascar'), ('Malaysia', 'Malaysia'),
        ('Maldives', 'Maldives'), ('Mali', 'Mali'), ('Malta', 'Malta'), ('Marshall Islands', 'Marshall Islands'),
        ('Mexico', 'Mexico'), ('Martinique', 'Martinique'), ('Mauritania', 'Mauritania'), ('Mauritius', 'Mauritius'),
        ('Mayotte', 'Mayotte'), ('Mexico', 'Mexico'), ('Monaco', 'Monaco'), ('Mongolia', 'Mongolia'),
        ('Montenegro', 'Montenegro'), ('Moldova, Republic of', 'Moldova, Republic of'), ('Montserrat', 'Montserrat'),
        ('Micronesia, Federated States of', 'Micronesia, Federated States of'), ('Morocco', 'Morocco'),
        ('Myanmar', 'Myanmar'), ('Moldova, Republic of', 'Moldova, Republic of'), ('Namibia', 'Namibia'),
        ('Nauru', 'Nauru'), ('Nepal', 'Nepal'), ('Netherlands', 'Netherlands'), ('New Caledonia', 'New Caledonia'),
        ('New Zealand', 'New Zealand'), ('Nicaragua', 'Nicaragua'), ('Niger', 'Niger'), ('Nigeria', 'Nigeria'),
        ('Niue', 'Niue'), ('Northern Mariana Islands', 'Northern Mariana Islands'), ('Norfolk Island', 'Norfolk Island')
        , ('Norway', 'Norway'), ('Oman', 'Oman'), ('Pakistan', 'Pakistan'), ('Palau', 'Palau'), ('Panama', 'Panama'),
        ('Palestine, State of', 'Palestine, State of'), ('Papua New Guinea', 'Papua New Guinea'), ('Peru', 'Peru'),
        ('Paraguay', 'Paraguay'), ('Philippines', 'Philippines'), ('Pitcairn', 'Pitcairn'), ('Poland', 'Poland'),
        ('Portugal', 'Portugal'), ('Puerto Rico', 'Puerto Rico'), ('Qatar', 'Qatar'), ('Réunion', 'Réunion'),
        ('Romania', 'Romania'), ('Russian Federation', 'Russian Federation'), ('Rwanda', 'Rwanda'), ('Samoa', 'Samoa'),
        ('Saint Helena, Ascension and Tristan da Cunha', 'Saint Helena, Ascension and Tristan da Cunha'),
        ('Saint Lucia', 'Saint Lucia'), ('Saint Barthélemy', 'Saint Barthélemy'), ('San Marino', 'San Marino'),
        ('Saint Kitts and Nevis', 'Saint Kitts and Nevis'), ('Sao Tome and Principe', 'Sao Tome and Principe'),
        ('Saint Martin (French part)', 'Saint Martin (French part)'), ('Saudi Arabia', 'Saudi Arabia'),
        ('Serbia', 'Serbia'), ('Senegal', 'Senegal'), ('Seychelles', 'Seychelles'), ('Sierra Leone', 'Sierra Leone'),
        ('Saint Pierre and Miquelon', 'Saint Pierre and Miquelon'), ('Singapore', 'Singapore'), ('Slovakia', 'Slovakia')
        , ('Saint Vincent and the Grenadines', 'Saint Vincent and the Grenadines'), ('Slovenia', 'Slovenia'),
        ('South Africa', 'South Africa'), ('Saint Barthélemy', 'Saint Barthélemy'), ('Somalia', 'Somalia'),
        ('Solomon Islands', 'Solomon Islands'), ('Saint Kitts and Nevis', 'Saint Kitts and Nevis'),
        ('Saint Helena, Ascension and Tristan da Cunha', 'Saint Helena, Ascension and Tristan da Cunha'),
        ('South Georgia and the South Sandwich Islands', 'South Georgia and the South Sandwich Islands'),
        ('South Sudan', 'South Sudan'), ('Spain', 'Spain'), ('Sri Lanka', 'Sri Lanka'), ('Sudan', 'Sudan'),
        ('Suriname', 'Suriname'), ('Svalbard and Jan Mayen', 'Svalbard and Jan Mayen'), ('Swaziland', 'Swaziland'),
        ('Sweden', 'Sweden'), ('Switzerland', 'Switzerland'), ('Syrian Arab Republic', 'Syrian Arab Republic'),
        ('Taiwan', 'Taiwan'), ('Tajikistan', 'Tajikistan'), ('Thailand', 'Thailand'), ('Timor-Leste', 'Timor-Leste'),
        ('Tanzania, United Republic of', 'Tanzania, United Republic of'), ('Togo', 'Togo'), ('Tokelau', 'Tokelau'),
        ('Tonga', 'Tonga'), ('Trinidad and Tobago', 'Trinidad and Tobago'), ('Tunisia', 'Tunisia'), ('Turkey', 'Turkey')
        , ('Turkmenistan', 'Turkmenistan'), ('Turks and Caicos Islands', 'Turks and Caicos Islands'),
        ('Tuvalu', 'Tuvalu'), ('Uganda', 'Uganda'), ('Ukraine', 'Ukraine'), ('United Kingdom', 'United Kingdom'),
        ('United Arab Emirates', 'United Arab Emirates'), ('United States', 'United States'), ('Uruguay', 'Uruguay'),
        ('United States Minor Outlying Islands', 'United States Minor Outlying Islands'), ('Uzbekistan', 'Uzbekistan'),
        ('Vanuatu', 'Vanuatu'), ('Venezuela, Bolivarian Republic of', 'Venezuela, Bolivarian Republic of'),
        ('Viet Nam', 'Viet Nam'), ('Virgin Islands, British', 'Virgin Islands, British'),
        ('Virgin Islands, U.S.', 'Virgin Islands, U.S.'), ('Wallis and Futuna', 'Wallis and Futuna'),
        ('Western Sahara', 'Western Sahara'), ('Yemen', 'Yemen'), ('Zambia', 'Zambia'), ('Zimbabwe', 'Zimbabwe')
    ]

    username = models.CharField(max_length=225)
    company_name = models.CharField(max_length=225)
    name = models.CharField(max_length=225)
    price = models.FloatField()
    caseQuantity = models.IntegerField()
    packSize = models.IntegerField()
    qtyUnits = models.CharField(max_length=225, choices=qtyUnits_Choices)
    category = models.CharField(max_length=225, null=True, blank=True, choices=Category_Choices)
    suppliers = models.CharField(max_length=225, blank=True, null=True)
    orderCode = models.CharField(max_length=225, blank=True, null=True)
    brand = models.CharField(max_length=225, blank=True, null=True)
    countryOfOrigin = models.CharField(max_length=225, blank=True, null=True, choices=Country_Of_Origin)
    storageAreas = models.CharField(max_length=225, blank=True, null=True)
    parLevel = models.IntegerField(null=True, blank=True)
    parUnits = models.CharField(max_length=225, null=True, blank=True, choices=qtyUnits_Choices)
    nutriationData = models.CharField(max_length=225, null=True, blank=True)
    fromMeasurementData = ArrayField(models.FloatField(), null=True, blank=True)
    fromMeasurementUnits = ArrayField(models.CharField(max_length=225), null=True, blank=True)
    toMeasurementData = ArrayField(models.FloatField(), null=True, blank=True)
    toMeasurementUnits = ArrayField(models.CharField(max_length=225), null=True, blank=True)
    hasMajorAllergens = models.BooleanField(null=True, blank=True)
    majorAllergens = models.CharField(max_length=225, blank=True, null=True)
    sugarAdded = models.BooleanField(null=True, blank=True)
    usablePercentage = models.IntegerField(null=True, blank=True)
    displayUnits = models.CharField(max_length=225, null=True, blank=True)
    displayName = models.CharField(max_length=225, null=True, blank=True)
    notes = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'Ingredients_Table'


class IngredientData(models.Model):
    ing_name = models.CharField(max_length=225)
    ing_amount = models.IntegerField()
    ing_units = models.CharField(max_length=225)
    ing_description = models.CharField(max_length=225, null=True, blank=True)

    class Meta:
        db_table = 'Ingredients_data'


class RecipesModel(models.Model):
    Category_Choices = [
        ("Food", "Food"),
        ("Labor", "Labor"),
        ("Packaging", "Packaging"),
        ("UnCategorized", "UnCategorized")
    ]
    company_name = models.CharField(max_length=225)
    recipe_user = models.CharField(max_length=225)
    recipe_name = models.CharField(max_length=225)
    recipe_category = models.CharField(max_length=225, null=True, blank=True, choices=Category_Choices)
    recipe_yield_count = models.IntegerField()
    yield_units = models.CharField(max_length=225)
    other_ing_data = models.ManyToManyField(IngredientData)

    class Meta:
        db_table = 'recipe_table'
