from django.http import HttpResponse, JsonResponse
from django.views import View
from scraperApp.models import Productos
from libs.Scraping import Scraping
import json

class StartScraping(View):
    
    def get(self, request):
        
        try:
            
            Scraping.process_urls('urls.txt')

            return JsonResponse({'exito':"Terminado "})
            
        except Exception as e:
            return JsonResponse({'Error':f"Error inesperado: {e}"}, status=500)
        
    
