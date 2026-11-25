from django.db import models

class Product(models.Model):
    product_name = models.CharField(max_length=100)
    product_code = models.CharField(max_length=50, unique=True)
    category = models.CharField(max_length=50)
    price = models.PositiveIntegerField()
    stock_quantity = models.PositiveIntegerField()

    def __str__(self):
        return self.product_name
