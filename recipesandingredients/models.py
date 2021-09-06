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
             ('19', 'Ounce (oz) (28.35 g)'),
             ('18', 'Pound (lb) (453.59 g)'),
             ('9', 'Kilogram (Kg) (1000 g)'),
             ('6', 'Tonne (T) (1000000 g)')
         )
         ),
        ('-- Volume --',
         (
             ('25', 'Pinch (pinch) (0.3 ml)'),
             ('22', 'US Teaspoon (tsp) (4.93 ml)'),
             ('21', 'US Tablespoon (tbsp) (14.79 ml)'),
             ('17', 'Fluid-ounce (floz) (29.57 ml)'),
             ('11', 'Deciliter (dL) (100 ml)'),
             ('20', 'US Cup (cup) (236.59 ml)'),
             ('16', 'Pint (pt) (473.18 ml)')
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
    fromMeasurement = ArrayField(ArrayField(models.CharField(max_length=225)), null=True, blank=True)
    toMeasurement = ArrayField(ArrayField(models.CharField(max_length=225)), null=True, blank=True)
    hasMajorAllergens = models.BooleanField(null=True, blank=True)
    majorAllergens = models.CharField(max_length=225, blank=True, null=True)
    sugarAdded = models.BooleanField(null=True, blank=True)
    usablePercentage = models.IntegerField(null=True, blank=True)
    displayUnits = models.CharField(max_length=225, null=True, blank=True)
    displayName = models.CharField(max_length=225,null=True, blank=True)
    notes = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'Ingredients_Table'
