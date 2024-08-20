from django.db import models

class ProductId(models.Model):
    idnew = models.IntegerField()    
    idold = models.IntegerField()  

    def __str__(self):
        return str(self.idnew)