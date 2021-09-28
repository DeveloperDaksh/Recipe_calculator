from django import forms
from .models import Ingredients, RecipesModel


class IngredientsForm(forms.ModelForm):
    required_css_class = 'required'

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        usersup = Ingredients.objects.filter(username=self.request.user)
        super(IngredientsForm, self).__init__(*args, **kwargs)
        if usersup.count() > 0:
            supp = []
            for sup in usersup:
                if sup.suppliers == '':
                    continue
                supp.append((sup.suppliers, sup.suppliers))
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
        self.fields['suppliers'] = forms.ChoiceField(choices=self.Supplier_Choice, required=False)

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
                   'company_name')
        fields = '__all__'


class RecipeForm(forms.ModelForm):
    yield_units = forms.CharField(label='yield units (servings,cookies,etc)', widget=forms.TextInput())

    class Meta:
        model = RecipesModel
        exclude = ('other_ing_data', 'recipe_user', 'company_name')
        fields = '__all__'
