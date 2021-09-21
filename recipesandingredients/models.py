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
             ('Tonne (T) (1000000 g)', 'Tonne (T) (1000000 g)')
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
             ('Pint (pt) (473.18 ml)', 'Pint (pt) (473.18 ml)')
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
        ('Afghanistan', 'Afghanistan'),
        ('India', 'India'),
        ('American Samoa', 'American Samoa'),
        ('Argentina', 'Argentina'),
        ('Armenia', 'Armenia'),
        ('Australia', 'Australia'),
        ('Banglades', 'Banglades'),
        ('Belgium', 'Belgium')
    ]

    username = models.CharField(max_length=225)
    name = models.CharField(max_length=225)
    price = models.IntegerField()
    caseQuantity = models.IntegerField(null=True, blank=True)
    packSize = models.IntegerField(null=True, blank=True)
    qtyUnits = models.CharField(max_length=225, null=True, blank=True, choices=qtyUnits_Choices)
    category = models.CharField(max_length=225, null=True, blank=True, choices=Category_Choices)
    suppliers = models.CharField(max_length=225, blank=True, null=True)
    orderCode = models.CharField(max_length=225, blank=True, null=True)
    brand = models.CharField(max_length=225, blank=True, null=True)
    countryOfOrigin = models.CharField(max_length=225, blank=True, null=True, choices=Country_Of_Origin)
    storageAreas = models.CharField(max_length=225, blank=True, null=True)
    parLevel = models.IntegerField(null=True, blank=True)
    parUnits = models.CharField(max_length=225, null=True, blank=True, choices=qtyUnits_Choices)
    nutriationData = models.CharField(max_length=225, null=True, blank=True)
    fromMeasurementData = ArrayField(models.IntegerField(), null=True, blank=True)
    fromMeasurementUnits = ArrayField(models.CharField(max_length=225), null=True, blank=True)
    toMeasurementData = ArrayField(models.IntegerField(), null=True, blank=True)
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

    recipe_user = models.CharField(max_length=225)
    recipe_name = models.CharField(max_length=225)
    recipe_category = models.CharField(max_length=225, null=True, blank=True,choices=Category_Choices)
    recipe_yield_count = models.IntegerField()
    yield_units = models.CharField(max_length=225)
    other_ing_data = models.ManyToManyField(IngredientData)

    class Meta:
        db_table = 'recipe_table'
