from django.db import models

class ProductId(models.Model):
    idnew = models.IntegerField()    
    idold = models.IntegerField()  

    def __str__(self):
        return str(self.idnew) 

class Documento(models.Model):
    idp = models.IntegerField(null=False, default = 0)
    datos = models.JSONField()  # Usa JSONField para almacenar datos JSON
    
    def __str__(self):
        return str(self.datos)