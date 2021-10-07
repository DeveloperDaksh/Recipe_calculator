from django import forms
from .models import Company, Customers, ShippingCarriers


class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company

        fields = (
            'name', 'billing_email', 'phone_number', 'address_one', 'address_two', 'city', 'country', 'postal_code')


class CompanySettings(forms.ModelForm):
    use_advanced_cal = forms.BooleanField(label='Use advanced margin calculator by default (instead of basic)',
                                          required=False)

    class Meta:
        model = Company
        fields = ('preferred_units', 'use_advanced_cal')


class CurrencyDisplay(forms.ModelForm):
    CURRENCY_CODE_CHOICES = [
        ('United States Dollar ($)', 'United States Dollar ($)'), ('Australian Dollar ($)', 'Australian Dollar ($)'),
        ('Euro (€)', 'Euro (€'), ('British Pound (£)', 'British Pound (£)'), ('Japanese Yen (¥)', 'Japanese Yen (¥)'),
        ('Canadian Dollar ($)', 'Canadian Dollar ($)'), ('Belarusian Ruble (Br)', 'Belarusian Ruble (Br)'),
        ('United Arab Emirates Dirham (د.إ)', 'United Arab Emirates Dirham (د.إ)'),
        ('Afghan Afghani (؋)', 'Afghan Afghani (؋)'), ('Albanian Lek (L)', 'Albanian Lek (L)'),
        ('Armenian Dram (դր.)', 'Armenian Dram (դր.)'), ('Angolan Kwanza (Kz)', 'Angolan Kwanza (Kz)'),
        ('Netherlands Antillean Gulden (ƒ)', 'Netherlands Antillean Gulden (ƒ)'),
        ('Aruban Florin (ƒ)', 'Aruban Florin (ƒ)'), ('Azerbaijani Manat (₼)', 'Azerbaijani Manat (₼)'),
        ('Argentine Peso ($)', 'Argentine Peso ($)'), ('Barbadian Dollar ($)', 'Barbadian Dollar ($)'),
        ('Bosnia and Herzegovina Convertible Mark (КМ)', 'Bosnia and Herzegovina Convertible Mark (КМ)'),
        ('Bangladeshi Taka (৳)', 'Bangladeshi Taka (৳)'), ('Bulgarian Lev (лв.)', 'Bulgarian Lev (лв.)'),
        ('Bahraini Dinar (ب.د)', 'Bahraini Dinar (ب.د)'), ('Burundian Franc (Fr)', 'Burundian Franc (Fr)'),
        ('Bermudian Dollar ($)', 'Bermudian Dollar ($)'), ('Brunei Dollar ($)', 'Brunei Dollar ($)'),
        ('Bolivian Boliviano (Bs.)', 'Bolivian Boliviano (Bs.)'), ('Brazilian Real (R$)', 'Brazilian Real (R$)'),
        ('Bahamian Dollar ($)', 'Bahamian Dollar ($)'), ('Bhutanese Ngultrum (Nu.)', 'Bhutanese Ngultrum (Nu.)'),
        ('Botswana Pula (P)', 'Botswana Pula (P)'), ('Belarusian Ruble (Br)', 'Belarusian Ruble (Br)'),
        ('Belize Dollar ($)', 'Belize Dollar ($)'), ('Congolese Franc (Fr)', 'Congolese Franc (Fr)'),
        ('Swiss Franc (CHF)', 'Swiss Franc (CHF)'), ('Unidad de Fomento (UF)', 'Unidad de Fomento (UF)'),
        ('Chilean Peso ($)', 'Chilean Peso ($)'), ('Chinese Renminbi Yuan (¥)', 'Chinese Renminbi Yuan (¥)'),
        ('Colombian Peso ($)', 'Colombian Peso ($)'), ('Costa Rican Colón (₡)', 'Costa Rican Colón (₡)'),
        ('Cuban Convertible Peso ($)', 'Cuban Convertible Peso ($)'), ('Cuban Peso ($)', 'Cuban Peso ($)'),
        ('Cape Verdean Escudo ($)', 'Cape Verdean Escudo ($)'), ('Czech Koruna (Kč)', 'Czech Koruna (Kč)'),
        ('Djiboutian Franc (Fdj)', 'Djiboutian Franc (Fdj)'), ('Danish Krone (kr.)', 'Danish Krone (kr.)'),
        ('Dominican Peso ($)', 'Dominican Peso ($)'), ('Algerian Dinar (د.ج)', 'Algerian Dinar (د.ج)'),
        ('Egyptian Pound (ج.م)', 'Egyptian Pound (ج.م)'), ('Eritrean Nakfa (Nfk)', 'Eritrean Nakfa (Nfk)'),
        ('Ethiopian Birr (Br)', 'Ethiopian Birr (Br)'), ('Fijian Dollar ($)', 'Fijian Dollar ($)'),
        ('Falkland Pound (£)', 'Falkland Pound (£)'), ('Georgian Lari (ლ)', 'Georgian Lari (ლ)'),
        ('Ghanaian Cedi (₵)', 'Ghanaian Cedi (₵)'), ('Gibraltar Pound (£)', 'Gibraltar Pound (£)'),
        ('Gambian Dalasi (D)', 'Gambian Dalasi (D)'), ('Guinean Franc (Fr)', 'Guinean Franc (Fr)'),
        ('Guatemalan Quetzal (Q)', 'Guatemalan Quetzal (Q)'), ('Guyanese Dollar ($)', 'Guyanese Dollar ($)'),
        ('Hong Kong Dollar ($)', 'Hong Kong Dollar ($)'), ('Honduran Lempira (L)', 'Honduran Lempira (L)'),
        ('Croatian Kuna (kn)', 'Croatian Kuna (kn)'), ('Haitian Gourde (G)', 'Haitian Gourde (G)'),
        ('Hungarian Forint (Ft)', 'Hungarian Forint (Ft)'), ('Indonesian Rupiah (Rp)', 'Indonesian Rupiah (Rp)'),
        ('Israeli New Sheqel (₪)', 'Israeli New Sheqel (₪)'), ('Indian Rupee (₹)', 'Indian Rupee (₹)'),
        ('Iraqi Dinar (ع.د)', 'Iraqi Dinar (ع.د)'), ('Iranian Rial (﷼)', 'Iranian Rial (﷼)'),
        ('Icelandic Króna (kr)', 'Icelandic Króna (kr)'), ('Jamaican Dollar ($)', 'Jamaican Dollar ($)'),
        ('Jordanian Dinar (د.ا)', 'Jordanian Dinar (د.ا)'), ('Kenyan Shilling (KSh)', 'Kenyan Shilling (KSh)'),
        ('Kyrgyzstani Som (som)', 'Kyrgyzstani Som (som)'), ('Cambodian Riel (៛)', 'Cambodian Riel (៛)'),
        ('Comorian Franc (Fr)', 'Comorian Franc (Fr)'), ('North Korean Won (₩)', 'North Korean Won (₩)'),
        ('South Korean Won (₩)', 'South Korean Won (₩)'), ('Kuwaiti Dinar (د.ك)', 'Kuwaiti Dinar (د.ك)'),
        ('Cayman Islands Dollar ($)', 'Cayman Islands Dollar ($)'), ('Kazakhstani Tenge (₸)', 'Kazakhstani Tenge (₸)'),
        ('Lao Kip (₭)', 'Lao Kip (₭)'), ('Lebanese Pound (ل.ل)', 'Lebanese Pound (ل.ل)'),
        ('Sri Lankan Rupee (₨)', 'Sri Lankan Rupee (₨)'), ('Liberian Dollar ($)', 'Liberian Dollar ($)'),
        ('Lesotho Loti (L)', 'Lesotho Loti (L)'), ('Libyan Dinar (ل.د)', 'Libyan Dinar (ل.د)'),
        ('Moroccan Dirham (د.م.)', 'Moroccan Dirham (د.م.)'), ('Moldovan Leu (L)', 'Moldovan Leu (L)'),
        ('Malagasy Ariary (Ar)', 'Malagasy Ariary (Ar)'), ('Macedonian Denar (ден)', 'Macedonian Denar (ден)'),
        ('Myanmar Kyat (K)', 'Myanmar Kyat (K)'), ('Mongolian Tögrög (₮)', 'Mongolian Tögrög (₮)'),
        ('Macanese Pataca (P)', 'Macanese Pataca (P)'), ('Mauritanian Ouguiya (UM)', 'Mauritanian Ouguiya (UM)'),
        ('Mauritian Rupee (₨)', 'Mauritian Rupee (₨)'), ('Maldivian Rufiyaa (MVR)', 'Maldivian Rufiyaa (MVR)'),
        ('Malawian Kwacha (MK)', 'Malawian Kwacha (MK)'), ('Mexican Peso ($)', 'Mexican Peso ($)'),
        ('Malaysian Ringgit (RM)', 'Malaysian Ringgit (RM)'), ('Mozambican Metical (MTn)', 'Mozambican Metical (MTn)'),
        ('Namibian Dollar ($)', 'Namibian Dollar ($)'), ('Nigerian Naira (₦)', 'Nigerian Naira (₦)'),
        ('Nicaraguan Córdoba (C$)', 'Nicaraguan Córdoba (C$)'), ('Norwegian Krone (kr)', 'Norwegian Krone (kr)'),
        ('Nepalese Rupee (₨)', 'Nepalese Rupee (₨)'), ('New Zealand Dollar ($)', 'New Zealand Dollar ($)'),
        ('Omani Rial (ر.ع.)', 'Omani Rial (ر.ع.)'), ('Panamanian Balboa (B/.)', 'Panamanian Balboa (B/.)'),
        ('Peruvian Sol (S/)', 'Peruvian Sol (S/)'), ('Papua New Guinean Kina (K)', 'Papua New Guinean Kina (K)'),
        ('Philippine Peso (₱)', 'Philippine Peso (₱)'), ('Pakistani Rupee (₨)', 'Pakistani Rupee (₨)'),
        ('Polish Złoty (zł)', 'Polish Złoty (zł)'), ('Paraguayan Guaraní (₲)', 'Paraguayan Guaraní (₲)'),
        ('Qatari Riyal (ر.ق)', 'Qatari Riyal (ر.ق)'), ('Romanian Leu (Lei)', 'Romanian Leu (Lei)'),
        ('Serbian Dinar (РСД)', 'Serbian Dinar (РСД)'), ('Russian Ruble (₽)', 'Russian Ruble (₽)'),
        ('Rwandan Franc (FRw)', 'Rwandan Franc (FRw)'), ('Saudi Riyal (ر.س)', 'Saudi Riyal (ر.س)'),
        ('Solomon Islands Dollar ($)', 'Solomon Islands Dollar ($)'), ('Swazi Lilangeni (E)', 'Swazi Lilangeni (E)'),
        ('South Sudanese Pound (£)', 'South Sudanese Pound (£)'), ('Syrian Pound (£S)', 'Syrian Pound (£S)'),
        ('Surinamese Dollar ($)', 'Surinamese Dollar ($)'), ('Salvadoran Colón (₡)', 'Salvadoran Colón (₡)'),
        ('São Tomé and Príncipe Dobra (Db)', 'São Tomé and Príncipe Dobra (Db)'), ('Thai Baht (฿)', 'Thai Baht (฿)'),
        ('Seychellois Rupee (₨)', 'Seychellois Rupee (₨)'), ('Somali Shilling (Sh)', 'Somali Shilling (Sh)'),
        ('Sudanese Pound (£)', 'Sudanese Pound (£)'), ('Swedish Krona (kr)', 'Swedish Krona (kr)'),
        ('Singapore Dollar ($)', 'Singapore Dollar ($)'), ('Saint Helenian Pound (£)', 'Saint Helenian Pound (£)'),
        ('Slovak Koruna (Sk)', 'Slovak Koruna (Sk)'), ('Sierra Leonean Leone (Le)', 'Sierra Leonean Leone (Le)'),
        ('Tajikistani Somoni (ЅМ)', 'Tajikistani Somoni (ЅМ)'), ('Turkmenistani Manat (T)', 'Turkmenistani Manat (T)'),
        ('Tunisian Dinar (د.ت)', 'Tunisian Dinar (د.ت)'), ('Tongan Paʻanga (T$)', 'Tongan Paʻanga (T$)'),
        ('Turkish Lira (₺)', 'Turkish Lira (₺)'), ('Trinidad and Tobago Dollar ($)', 'Trinidad and Tobago Dollar ($)'),
        ('New Taiwan Dollar ($)', 'New Taiwan Dollar ($)'), ('Tanzanian Shilling (Sh)', 'Tanzanian Shilling (Sh)'),
        ('Ukrainian Hryvnia (₴)', 'Ukrainian Hryvnia (₴)'), ('Ugandan Shilling (USh)', 'Ugandan Shilling (USh)'),
        ('Uruguayan Peso ($)', 'Uruguayan Peso ($)'), ("Uzbekistan Som (so'm)", "Uzbekistan Som (so'm)"),
        ('Venezuelan Bolívar Soberano (Bs)', 'Venezuelan Bolívar Soberano (Bs)'),
        ('Samoan Tala (T)', 'Samoan Tala (T)'), ('Silver (Troy Ounce) (oz t)', 'Silver (Troy Ounce) (oz t)'),
        ('Vanuatu Vatu (Vt)', 'Vanuatu Vatu (Vt)'), ('Gold (Troy Ounce) (oz t)', 'Gold (Troy Ounce) (oz t)'),
        ('Central African Cfa Franc (Fr)', 'Central African Cfa Franc (Fr)'),
        ('Vietnamese Đồng (₫)', 'Vietnamese Đồng (₫)'), ('European Composite Unit ()', 'European Composite Unit ()'),
        ('European Monetary Unit ()', 'European Monetary Unit ()'), ('Palladium (oz t)', 'Palladium (oz t)'),
        ('European Unit of Account 9 ()', 'European Unit of Account 9 ()'), ('Cfp Franc (Fr)', 'Cfp Franc (Fr)'),
        ('European Unit of Account 17 ()', 'European Unit of Account 17 ()'), ('Platinum (oz t)', 'Platinum (oz t)'),
        ('East Caribbean Dollar ($)', 'East Caribbean Dollar ($)'), ('Yemeni Rial (﷼)', 'Yemeni Rial (﷼)'),
        ('Special Drawing Rights (SDR)', 'Special Drawing Rights (SDR)'), ('Yemeni Rial (﷼)', 'Yemeni Rial (﷼)'),
        ('West African Cfa Franc (Fr)', 'West African Cfa Franc (Fr)'), ('Zambian Kwacha (ZK)', 'Zambian Kwacha (ZK)'),
        ('South African Rand (R)', 'South African Rand (R)'), ('Zambian Kwacha (K)', 'Zambian Kwacha (K)'),
        ('Codes specifically reserved for testing purposes ()', 'Codes specifically reserved for testing purposes ()'),
        ('Bitcoin Cash (₿)', 'Bitcoin Cash (₿)'), ('Bitcoin (₿)', 'Bitcoin (₿)'), ('UIC Franc ()', 'UIC Franc ()'),
        ('Guernsey Pound (£)', 'Guernsey Pound (£)'), ('Jersey Pound (£)', 'Jersey Pound (£)'),
        ('Isle of Man Pound (£)', 'Isle of Man Pound (£)'), ('British Penny ()', 'British Penny ()'),
        ('Chinese Renminbi Yuan Offshore (¥)', 'Chinese Renminbi Yuan Offshore (¥)'),
        ('Estonian Kroon (KR)', 'Estonian Kroon (KR)'), ('Ghanaian Cedi (₵)', 'Ghanaian Cedi (₵)'),
        ('Lithuanian Litas (Lt)', 'Lithuanian Litas (Lt)'), ('Latvian Lats (Ls)', 'Latvian Lats (Ls)'),
        ('Mauritanian Ouguiya (UM)', 'Mauritanian Ouguiya (UM)'), ('Maltese Lira (₤)', 'Maltese Lira (₤)'),
        ('Turkmenistani Manat (m)', 'Turkmenistani Manat (m)'), ('Japanese Yen (¥)', 'Japanese Yen (¥)'),
        ('Zimbabwean Dollar ($)', 'Zimbabwean Dollar ($)'), ('Venezuelan Bolívar (Bs.F)', 'Venezuelan Bolívar (Bs.F)')
    ]

    currency_codes = forms.ChoiceField(choices=CURRENCY_CODE_CHOICES, required=False,
                                       label='Choose a currency code for display purposes...')
    own_currency = forms.CharField(label='...or enter your own', required=False)
    ROUND_CHOICES = [
        ('Yes', 'Yes (e.g. 285)'),
        ('No', 'No(e.g. 285.29)')
    ]
    DISPLAY_CHOICES = [
        ('before', '...before the number (e.g. $100.00)'),
        ('after', '...after the number (e.g. 100.00$)')
    ]
    round_currency = forms.ChoiceField(choices=ROUND_CHOICES, widget=forms.RadioSelect(), required=False,
                                       initial={'round_currency': 'No'}, label='Round currency to whole numbers')
    display_currency = forms.ChoiceField(choices=DISPLAY_CHOICES, widget=forms.RadioSelect(), required=False,
                                         initial={'display_currency': 'before'}, label='Display currency symbol...')
    decimal_mark = forms.CharField(required=False, label='Decimal mark (e.g. 100.00 vs 100,00)')
    thousands_separator = forms.CharField(required=False, label='Thousands separator (e.g. 1,000,000 vs 1.000.000)')

    class Meta:
        model = Company
        fields = ('currency_codes', 'own_currency', 'round_currency', 'display_currency', 'decimal_mark',
                  'thousands_separator')


class BillingCountry(forms.ModelForm):
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

    billing_country = forms.ChoiceField(choices=Country_Of_Origin, label='Country', required=False)

    class Meta:
        model = Company
        fields = ('billing_country',)


class DeleteForm(forms.Form):
    password = forms.CharField(max_length=225, widget=forms.PasswordInput(attrs={'placeholder': ' Enter Password'}),
                               label='You must provide your password to perform this action.')


class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customers
        exclude = ('user', 'company_name')
        fields = '__all__'


class ShippingCarrierForm(forms.ModelForm):
    class Meta:
        model = ShippingCarriers
        exclude = ('user', 'company_name')
        fields = '__all__'
