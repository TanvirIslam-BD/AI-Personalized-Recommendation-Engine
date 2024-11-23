from django.db import models

class Product(models.Model):
    product_id = models.IntegerField(unique=True)
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=50)

class UserRating(models.Model):
    user_id = models.IntegerField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    rating = models.FloatField()
