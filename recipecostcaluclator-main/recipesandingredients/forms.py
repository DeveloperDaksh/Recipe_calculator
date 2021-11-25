import datetime

from django import forms
from .models import Ingredients, RecipesModel, IngredientCategories, Suppliers, StorageAreas, NutritionDetails, \
    IngredientSuppliers, ProductionPlanTemplate, ProductionPlan


class IngredientsForm(forms.ModelForm):
    required_css_class = 'required'

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        company_name = self.request.session['company_name']
        usersup = Suppliers.objects.filter(user=self.request.user, company_name=company_name)
        super(IngredientsForm, self).__init__(*args, **kwargs)
        if usersup.count() > 0:
            supp = []
            for sup in usersup:
                if sup.supplier_name == '':
                    continue
                supp.append((sup.supplier_name, sup.supplier_name))
            self.Supplier_Choice = [
                ("", "------------"),
                ("Add Supplier", "Add Supplier"),
            ]
            for sample in list(set(supp)):
                self.Supplier_Choice.append(sample)
            print(self.Supplier_Choice)
        else:
            self.Supplier_Choice = [
                ("", "------------"),
                ("Add Supplier", "Add Supplier")
            ]
        customer_categeroy_choices = [('', '-----------'), ("Add Category", "Add Category")]
        storage_choices = [('', '-----------')]
        user_categories = IngredientCategories.objects.filter(user=self.request.user,
                                                              company_name=self.request.session['company_name'],
                                                              category_type='ingredient')
        for each in user_categories:
            customer_categeroy_choices.append((each.category, each.category))
        storage_filter = StorageAreas.objects.filter(user=self.request.user.username,
                                                     company_name=self.request.session['company_name'])
        for storage in storage_filter:
            storage_choices.append((storage.name, storage.name))
        self.fields['suppliers'] = forms.ChoiceField(choices=self.Supplier_Choice, required=False, label='Supplier')
        self.fields['category'] = forms.ChoiceField(choices=customer_categeroy_choices, required=False)
        self.fields['storageAreas'] = forms.ChoiceField(choices=storage_choices, required=False, label='Storage Area')

    Alleregen_Choices = [
        ("Cerly", "Cerly"), ("Shellfish", "Shellfish"), ("Eggs", "Eggs"), ("Soy", "Soy"),
        ("Fish", "Fish"), ("Sulfites", "Sulfites"), ("Milk", "Milk"), ("Tree Nuts", "Tree Nuts"),
        ("Lupin", "Lupin"), ("Wheat", "Wheat"), ("Molluscs", "Molluscs"), ("Mustard", "Mustard"),
        ("Peanuts", "Peanuts"), ("Sesame", "Sesame")
    ]
    majorAllergens = forms.MultipleChoiceField(required=False, choices=Alleregen_Choices,
                                               widget=forms.CheckboxSelectMultiple)

    class Meta:
        model = Ingredients
        exclude = ('username', 'fromMeasurementData', 'fromMeasurementUnits', 'toMeasurementData', 'toMeasurementUnits',
                   'company_name', 'fdcId')
        fields = '__all__'


class RecipeForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        company_name = self.request.session['company_name']
        super(RecipeForm, self).__init__(*args, **kwargs)
        categories = IngredientCategories.objects.filter(user=self.request.user.username, company_name=company_name,
                                                         category_type='recipe')
        recipe_categories = [('', '--------------')]
        for each in categories:
            recipe_categories.append((each.category, each.category))
        print(recipe_categories)
        self.fields['recipe_category'] = forms.ChoiceField(choices=recipe_categories, required=False)

    yield_units = forms.CharField(label='yield units (servings,cookies,etc)', widget=forms.TextInput())

    class Meta:
        model = RecipesModel
        exclude = ('other_ing_data', 'recipe_user', 'company_name', 'preparation_instructions', 'recipe_images')
        fields = '__all__'


class SuppliersForm(forms.ModelForm):
    delivery_days_choices = [
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
        ('Saturday', 'Saturday'),
        ('Sunday', 'Sunday')
    ]
    delivery_days = forms.MultipleChoiceField(choices=delivery_days_choices, required=False,
                                              widget=forms.CheckboxSelectMultiple)

    class Meta:
        model = Suppliers
        exclude = ('user', 'company_name')
        fields = '__all__'


class UpdateSupplier(forms.ModelForm):
    class Meta:
        model = Suppliers
        exclude = ('user', 'company_name', 'delivery_days')
        fields = '__all__'


class StorageAreaForm(forms.ModelForm):
    class Meta:
        model = StorageAreas
        exclude = ('user', 'company_name')
        fields = '__all__'


class NutritionDetailsForm(forms.ModelForm):
    class Meta:
        model = NutritionDetails
        exclude = ('user', 'company_name', 'ingredient')
        fields = '__all__'


class RecipePreparationInstructions(forms.ModelForm):
    class Meta:
        model = RecipesModel
        fields = ('preparation_instructions',)


class Ingredient_SupplierForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        company_name = self.request.session['company_name']
        usersup = Suppliers.objects.filter(user=self.request.user, company_name=company_name)
        super(Ingredient_SupplierForm, self).__init__(*args, **kwargs)
        if usersup.count() > 0:
            supp = []
            for sup in usersup:
                if sup.supplier_name == '':
                    continue
                supp.append((sup.supplier_name, sup.supplier_name))
            self.Supplier_Choice = [
                ("", "------------"),
                ("Add Supplier", "Add Supplier"),
            ]
            for sample in list(set(supp)):
                self.Supplier_Choice.append(sample)
            print(self.Supplier_Choice)
        else:
            self.Supplier_Choice = [
                ("", "------------"),
                ("Add Supplier", "Add Supplier")
            ]
        self.fields['supplier'] = forms.ChoiceField(choices=self.Supplier_Choice, label='Supplier')

    class Meta:
        model = IngredientSuppliers
        exclude = ('ingredient_relation', 'preferred')
        fields = '__all__'


class UpdateIngredientSupplierForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        company_name = self.request.session['company_name']
        usersup = Suppliers.objects.filter(user=self.request.user, company_name=company_name)
        super(UpdateIngredientSupplierForm, self).__init__(*args, **kwargs)
        if usersup.count() > 0:
            supp = []
            for sup in usersup:
                if sup.supplier_name == '':
                    continue
                supp.append((sup.supplier_name, sup.supplier_name))
            self.Supplier_Choice = [
                ("", "------------"),
            ]
            for sample in list(set(supp)):
                self.Supplier_Choice.append(sample)
            print(self.Supplier_Choice)
        else:
            self.Supplier_Choice = [
                ("", "------------"),
            ]
        self.fields['supplier'] = forms.ChoiceField(choices=self.Supplier_Choice, label='Supplier')

    class Meta:
        model = IngredientSuppliers
        exclude = ('ingredient_relation', 'preferred')
        fields = '__all__'


class ProductionPlanTemplateForm(forms.ModelForm):
    class Meta:
        model = ProductionPlanTemplate
        exclude = ('user', 'company_name')
        fields = '__all__'


class ProductionPlanForm(forms.ModelForm):
    date_field = forms.DateField(initial=datetime.date.today)

    class Meta:
        model = ProductionPlan
        exclude = ('user', 'company_name', 'recipes')
        fields = '__all__'
