from django import forms
from .models import Ingredients


class IngredientsForm(forms.ModelForm):
    required_css_class = 'required'

    def __init__(self, *args, **kwargs):
        print(kwargs)
        print(kwargs.get('request').user)
        self.request = kwargs.pop('request', None)
        usersup = Ingredients.objects.filter(username=self.request.user)
        super(IngredientsForm, self).__init__(*args, **kwargs)
        if usersup.count() > 0:
            supp = []
            for sup in usersup:
                supp.append((sup.suppliers, sup.suppliers))
            self.Supplier_Choice = [
                ("Add Supplier", "Add Supplier"),
            ]
            for sample in list(set(supp)):
                self.Supplier_Choice.append(sample)
            print(self.Supplier_Choice)
        else:
            self.Supplier_Choice = [
                ("--------", "------------"),
                ("Add Supplier", "Add Supplier")
            ]
        self.fields['suppliers'] = forms.ChoiceField(choices=self.Supplier_Choice, required=False)

    Alleregen_Choices = [
        ("Cerly", "Cerly"),
        ("Eggs", "Eggs"),
        ("Fish", "Fish"),
        ("Milk", "Milk")
    ]
    majorAllergens = forms.MultipleChoiceField(required=False, choices=Alleregen_Choices,
                                               widget=forms.CheckboxSelectMultiple)

    class Meta:
        model = Ingredients
        exclude = ('username', 'fromMeasurement', 'toMeasurement')
        fields = '__all__'
