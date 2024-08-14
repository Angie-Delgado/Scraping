from django.http import JsonResponse
from django.views import View
from scraperApp.models import Productos as ProductosModel

class ProductosView(View):
    def prueba(request):
        datos = {
            'nombre': 'John Doe',
            'edad': 30,
            'ciudad': 'New York'
        }
        return JsonResponse(datos)

    def obtenerProductos(request):
        products = ProductosModel.objects.all().values('name', 'price', 'url')
        products_list = list(products)  # Convertir el QuerySet a una lista
        return JsonResponse(products_list, safe=False)

    def get(self,request):
        return  self.obtenerProductos()

