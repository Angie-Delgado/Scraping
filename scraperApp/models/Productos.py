from django.db import models

class Productos(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    offer_price = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    description = models.CharField(max_length=255,null=True)
    product_img = models.URLField()
    

    def __str__(self):
        return self.name
