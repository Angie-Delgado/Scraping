from django.conf import settings
from bs4 import BeautifulSoup
from libs.Utils import Utils
import urllib.parse
import requests
import os

class Scraping:
    def __init__(self,nid=None):
        self.id = nid if nid else 0

    @staticmethod
    def extract_dom(url):
        try:
            encoded_url = urllib.parse.quote(url)
            api_url = settings.CODE_APISCRAPE.format(settings.TOKEN_APISCRAPE, encoded_url)
            response = requests.get(api_url)
            response.raise_for_status()  # Lanza una excepci�n si hay un error HTTP
            return response.text
        except requests.exceptions.RequestException as e:
            raise requests.exceptions.RequestException(f"Error al cargar la pagina: {e}")
        except Exception as e:
            raise Exception(f"Error al extraer el DOM: {e}")
        
    def scrape_website(self, url):
        try:
            html = self.extract_dom(url)
            soup = BeautifulSoup(html, 'html.parser')
            
            # Extraer el nombre del producto
            name_element = soup.find(id='productTitle')
            name = name_element.text.strip() if name_element else ''

            # Extraer el precio
            price_element = soup.find('span', {'class': 'a-price-symbol'})
            price = price_element.text.strip() if price_element else ''

            price_element = soup.find('span', {'class': 'a-price-whole'})
            price += price_element.text.strip() if price_element else ''
            
            price_element = soup.find('span', {'class': 'a-price-fraction'})
            price += price_element.text.strip() if price_element else '00'

            # Extraer la descripci�n del producto
            description_element = soup.find('div', {'id': 'feature-bullets'})
            description = description_element.text.strip() if description_element else ''
            description = description.replace('\n','')

            # Extraer la imagen del producto
            img_element = soup.find(id='landingImage')
            product_img = img_element.get('src') if img_element else ''

            # Extraer las caracteristicas del producto
            features = {}
            overview_elements = soup.find('div', {'data-feature-name': 'productOverview'})
            if not overview_elements:
                overview_elements = soup.find('div', {'data-a-expander-name': 'productOverview'})

            if overview_elements: 
                features_elements = overview_elements.find_all('tr')
                for feature in features_elements:
                    key_element = feature.find('td', {'class': 'a-keyvalue-label'})
                    value_element = feature.find('td', {'class': 'a-keyvalue-value'})

                    if not (key_element and value_element):
                        key_element = feature.find('td', {'class': 'a-span3'})
                        value_element = feature.find('td', {'class': 'a-span9'})

                    if (key_element and value_element):
                        key = key_element.find('span').text.strip()
                        value = value_element.find('span').text.strip()
                        features[key] = value.replace('\n','')

            # Extraer las caracteristicas adicionales del producto
            detail = {}
          
            detail_elements = soup.find_all('table', {'class': 'prodDetTable'})
            
            for tabla in detail_elements:
                rows = tabla.find_all('tr')
                for row in rows:
                    key_element = row.find('th')
                    value_element = row.find('td')                    

                    if (key_element and value_element):
                        key = key_element.text.strip()
                        value = value_element.text.strip()
                        detail[key] = value.replace('\n','')
                        
            datos = {
                'id':           self.id,
                'name':         name,
                'price':        price,
                'description':  description,
                'product_img':  product_img,
                'features':     features,
                'detail':       detail,
                'link':         url
            }
            
            return datos
        except ValueError as e:
            raise ValueError(f"Error al crear el producto: {e}")
        except Exception as e:
            raise Exception(f"Ocurrio un error extrayendo el html: {e}")

    def process_urls(self,name_files):
        try:
            print("processing urls file")
            print('reading file in: '+os.path.join(settings.BASE_DIR, settings.FILES_URL,name_files))

            urls = Utils.get_list_from_txt(os.path.join(settings.BASE_DIR, settings.FILES_URL,name_files))
            alldata = []
            for url in urls:
                if not url.startswith("Error"):
                    self.id +=1
                    print(f"url linea {self.id}")
                    data = self.scrape_website(url)
                    alldata.append(data)
                    #Utils.push_json_file(data, os.path.join(settings.BASE_DIR, settings.FILES_URL,'products.json'))
            
            return self.id, alldata
        except Exception as e:
            raise Exception(f"Ocurrio un error procesando las urls: {e}")

        
