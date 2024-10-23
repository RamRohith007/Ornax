from django.db import models
from django.db.models import Model

# Create your models here.
class Product(models.Model):
    product_id = models.IntegerField(unique=True)
    product_name = models.CharField(max_length=100)
    product_brand = models.CharField(max_length=50)
    product_mfg_year = models.DateField()
    product_image_url = models.URLField(max_length=500)
    product_url = models.URLField(max_length=600,default="http://ornax.com/")
    product_stock = models.IntegerField()
    product_price = models.IntegerField()
    product_description = models.CharField(max_length=300)

    def __str__(self):
        return f"{self.product_id} | {self.product_name}"

    
