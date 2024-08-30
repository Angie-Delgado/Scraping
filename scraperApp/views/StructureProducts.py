from django.http import JsonResponse
from django.conf import settings
from django.views import View
from scraperApp.models import ProductId, Documento
from libs.EstructurarDatos import EstructurarDatosEs, EstructurarDatosEn
from libs.Utils import Utils
from langdetect import detect, LangDetectException
import os

class StructureProducts(View):
    
    def __init__(self):
        try:
            # Obtener única fila
            self.productId = ProductId.objects.get(pk=1)
            if not self.productId:
                raise Exception("No se encontro ningun producto en la base de datos.")

            # Cargar los datos del archivo JSON
            self.products = Documento.objects.filter(idp__gt=self.productId.idold, idp__lte=self.productId.idnew)
            
        
        except Exception as e:
            self.products = []
            raise Exception(f"Error inesperado: {e}")
            
    
    @staticmethod
    def detectar_idioma(texto):
        try:
            return detect(texto)
        except LangDetectException as e:
            return None           
   

    def get_final_structure(self):
        todos = []

        try:
            for item in self.products:
                product = item.datos
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
                    'size': product['detail'].get('Dimensiones del producto', product['detail'].get('Product Dimensions', '')),
                    'weight': product['extFeature'].get('peso',product['extFeature'].get('weight',product['detail'].get('Peso del articulo',product['detail'].get('Item Weight', '')))),
                    'velocity': product['extFeature'].get('velocidad',product['extFeature'].get('velocity',product['detail'].get('Procesador',product['detail'].get('Processor', '')))),
                    'RAM': product['features'].get('Tamano de la memoria RAM instalada', product['features'].get('Ram Memory Installed Size', product['detail'].get('RAM',''))),
                    'storage': product['features'].get('Tamano del disco duro', product['features'].get('Hard Disk Size', '')),
                    'pantalla': product['features'].get('Tamano de pantalla', product['features'].get('Screen Size', '')),
                    'sistema': product['features'].get('Sistema operativo', product['features'].get('Operating System', ''))
                }

                todos.append(datos)
                
            return todos
    
        except KeyError as e:
            raise Exception(f"Error de clave: {e}")
        except Exception as e:
            raise Exception(f"Error inesperado: {e}")


    def add_structure(self):
        try:
            for product in self.products:
                text = product.datos['description']
            
                if self.detectar_idioma(text) == 'es':
                    from_text = EstructurarDatosEs(text)
                else:
                    from_text = EstructurarDatosEn(text)
                
                producto_datos = {}
                for clave, valor in from_text.caracteristicas.items():
                    producto_datos[clave] = valor

                # Aquí se actualiza self.products al modificar cada producto
                product.datos['extFeature'] = producto_datos
                product.save()
                
        except Exception as e:
            raise Exception(f"Error inesperado: {e}")
        

    def get(self, request):
        
        try:

            self.add_structure()
            datos = self.get_final_structure()

            Utils.save_to_csv(datos, os.path.join(settings.BASE_DIR, settings.FILES_URL,'finalProducts.csv'))
            
            return JsonResponse({'datos':datos})
            
        except Exception as e:
            return JsonResponse({'Error':f"Error inesperado: {e}"}, status=500)
        
    
