from django.http import JsonResponse
from django.views import View
from scraperApp.models import ProductId
from libs.Scraping import Scraping

class StartScraping(View):
    
    def get(self, request):
        
        try:

            #obtner id productos
            product = ProductId.objects.first()

            #scraping
            new_scraping = Scraping(product.idnew)
            new_id = new_scraping.process_urls('urls.txt')

            #Actualizar id 
            product.idold    = product.idnew
            product.idnew       = new_id
            product.save()

            return JsonResponse({'exito':"Terminado "})
            
        except Exception as e:
            return JsonResponse({'Error':f"Error inesperado: {e}"}, status=500)
        
    
