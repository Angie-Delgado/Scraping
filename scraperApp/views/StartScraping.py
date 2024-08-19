from django.http import HttpResponse, JsonResponse
from django.conf import settings
from django.views import View
from scraperApp.models import Productos
from libs.Scraping import Scraping
from Archivos.EstructurarDatos import EstructurarDatosEs, EstructurarDatosEn
from langdetect import detect, LangDetectException
import json
import os

class StartScraping(View):
    
    @staticmethod
    def detectar_idioma(texto):
        try:
            return detect(texto)
        except LangDetectException as e:
            return None
    
    @staticmethod
    def load_json_data(json_file_path):
        with open(json_file_path, 'r', encoding='utf-8') as json_file:
            data = json.load(json_file)       
        return data
    
    def get(self, request):
        
        try:
            
            # Scraping.process_urls('urls.txt')
            products = self.load_json_data(os.path.join(settings.BASE_DIR, 'Archivos', 'products.json'))
            text_products_json = [{'description':product['description']} for product in products]
            
            datos = []
            for text in text_products_json:
                text = text['description']
                
                if self.detectar_idioma(text) == 'es':
                    from_text = EstructurarDatosEs(text)
                else:
                    from_text = EstructurarDatosEn(text)
                    
                producto_datos = {}
                for clave, valor in from_text.caracteristicas.items():
                    producto_datos[clave] = valor
                datos.append({'texto':text})
                datos.append({'caracteristicas':producto_datos})

            # return JsonResponse({'exito':"Terminado "})
            return JsonResponse({'datos':datos})
            
        except Exception as e:
            return JsonResponse({'Error':f"Error inesperado: {e}"}, status=500)
        
    
