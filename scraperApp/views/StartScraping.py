from django.http import JsonResponse
from django.views import View
from scraperApp.models import ProductId, Documento
from libs.Scraping import Scraping

class StartScraping(View):
    
    def get(self, request):
        
        try:

            #obtner id productos
            product, creado = ProductId.objects.get_or_create(id=1, defaults={'idnew': 0, 'idold': 0})

            #scraping
            new_scraping = Scraping(product.idnew)
            new_id, data = new_scraping.process_urls('urls.txt')

            #Actualizar id 
            product.idold    = product.idnew
            product.idnew    = new_id
            product.save()

            idold = product.idold 

            for item in data:
                idold +=1
                documento = Documento(idp = idold,datos=item)
                documento.save()

            return JsonResponse({'exito':"Terminado "})
            
        except Exception as e:
            return JsonResponse({'Error':f"Error inesperado: {e}"}, status=500)
        
    
