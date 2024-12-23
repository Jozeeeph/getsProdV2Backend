from django.db import models
from django.core.validators import MinValueValidator


# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=50)
    price = models.FloatField(validators=[MinValueValidator(0.0)])
    image = models.ImageField(upload_to='images/')

    def __str__(self):
        return self.name
    