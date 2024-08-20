from django.http import HttpResponse, JsonResponse
from django.conf import settings
from django.views import View
from scraperApp.models import ProductId
from libs.EstructurarDatos import EstructurarDatosEs, EstructurarDatosEn
from libs.Utils import Utils
from langdetect import detect, LangDetectException
import json
import os

class StructureProducts(View):
    
    def __init__(self):
        try:
            # Obtener única fila
            productId = ProductId.objects.first()
            if not productId:
                raise ValueError("No se encontro ningun producto en la base de datos.")

            # Cargar los datos del archivo JSON
            products = Utils.load_json_data(os.path.join(settings.BASE_DIR, 'Archivos', 'products.json'))
            
            # Filtrar productos 
            self.products = [product for product in products if product['id'] >= productId.idold]
        
        except Exception as e:
            self.products = []
            raise ValueError(f"Error inesperado: {e}")
            
    
    @staticmethod
    def detectar_idioma(texto):
        try:
            return detect(texto)
        except LangDetectException as e:
            return None           
   

    def get_final_structure(self):
        todos = []

        try:
            for product in self.products:
                datos = {
                    'id': product['id'],
                    'title': product['name'],
                    'description': product['description'],
                    'delivery_time': '',
                    'category': 'Electronics',
                    'price': product['price'],
                    'link': product['link'],
                    'image': product['product_img'],
                    'color': product['features'].get('Color', ''),
                    'brand': product['features'].get('Marca', product['features'].get('Brand', '')),
                    'model': product['features'].get('Modelo de CPU', product['features'].get('CPU Model', '')),
                    'size': product['modules'].get('Dimensiones', product['modules'].get('Dimensions', '')),
                    'weight': product['extFeatres'].get('peso',product['extFeatres'].get('weight',product['modules'].get('Peso', product['modules'].get('Weight', '')))),
                    'velocity': product['extFeatres'].get('velocidad',product['extFeatres'].get('velocity',product['modules'].get('Frecuencia de actualizacion', product['modules'].get('Refresh Rate', '')))),
                    'RAM': product['features'].get('Tamano de la memoria RAM instalada', product['features'].get('Ram Memory Installed Size', '')),
                    'storage': product['features'].get('Tamano del disco duro', product['features'].get('Hard Disk Size', '')),
                    'pantalla': product['features'].get('Tamano de pantalla', product['features'].get('Screen Size', '')),
                    'sistema': product['features'].get('Sistema operativo', product['features'].get('Operating System', ''))
                }

                todos.append(datos)
                
            return todos
    
        except KeyError as e:
            raise valueError(f"Error de clave: {e}")
        except Exception as e:
            raise valueError(f"Error inesperado: {e}")


    def add_structure(self):
        try:
            for product in self.products:
                text = product['description']
            
                if self.detectar_idioma(text) == 'es':
                    from_text = EstructurarDatosEs(text)
                else:
                    from_text = EstructurarDatosEn(text)
                
                producto_datos = {}
                for clave, valor in from_text.caracteristicas.items():
                    producto_datos[clave] = valor

                # Aquí se actualiza self.products al modificar cada producto
                product['extFeature'] = producto_datos
                
        except Exception as e:
            raise ValueError(f"Error inesperado: {e}")


    def get(self, request):
        
        try:

            self.add_structure()
            datos = self.get_final_structure()

            Utils.export_to_json(datos, os.path.join(settings.BASE_DIR, settings.FILES_URL,'finalProducts.json'))
            
            
            return JsonResponse({'datos':datos})
            
        except Exception as e:
            return JsonResponse({'Error':f"Error inesperado: {e}"}, status=500)
        
    
