from django.http import JsonResponse
from django.conf import settings
from django.views import View
import os

class ShowProducts(View):  
       
    
    def get(self, request):
        
        try:

            products = os.path.join(settings.BASE_DIR, 'Archivos', 'products.json')
            
            return JsonResponse(products)
            
        except Exception as e:
            return JsonResponse({'Error':f"Error inesperado: {e}"}, status=500)
        
    
