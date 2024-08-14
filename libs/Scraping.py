import json
from django.conf import settings
from bs4 import BeautifulSoup
from decimal import Decimal
import urllib.parse
import requests
import os

class Scraping:

    def extract_dom(url):
        try:
            encoded_url = urllib.parse.quote(url)
            api_url = settings.CODE_APISCRAPE.format(settings.TOKEN_APISCRAPE, encoded_url)
            response = requests.get(api_url)
            response.raise_for_status()  # Lanza una excepción si hay un error HTTP
            return response.text
        except requests.exceptions.RequestException as e:
            raise requests.exceptions.RequestException(f"Error al cargar la pagina: {e}")
        except Exception as e:
            raise Exception(f"Error al extraer el DOM: {e}")

    def export_to_json(data, file_name):
        try:
            if os.path.exists(file_name):
                with open(file_name, 'r', encoding='utf-8') as currfile:
                    try:
                        existing_data = json.load(currfile)
                    except json.JSONDecodeError:
                        existing_data = []
            else:
                existing_data = []

            # Asegurarse de que existing_data es una lista
            if not isinstance(existing_data, list):
                raise ValueError("El archivo JSON no contiene una lista. El formato del archivo no es compatible.")

            # Agregar los nuevos datos a la lista existente
            existing_data.append(data)

            # Escribir el contenido actualizado en el archivo
            with open(file_name, 'w', encoding='utf-8') as currfile:
                json.dump(existing_data, currfile, ensure_ascii=False, indent=4)
                
        except Exception as e:
            print('error')
            raise Exception(f"Ocurrio un error escribiendo en el archivo: {e}")
    
    def scrape_website(url):
        try:
            html = Scraping.extract_dom(url)
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

            # Extraer la descripción del producto
            description_element = soup.find('div', {'id': 'feature-bullets'})
            description = description_element.text.strip() if description_element else ''

            # Extraer la imagen del producto
            img_element = soup.find(id='landingImage')
            product_img = img_element.get('src') if img_element else ''

            # Extraer las características del producto
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
                        features[key] = value

            datos = {
                'name': name,
                'price': price,
                'description': description,
                'product_img': product_img,
                'features': features,
                'link': url
            }            
            
            return datos
        except ValueError as e:
            raise ValueError(f"Error al crear el producto: {e}")
        except Exception as e:
            raise Exception(f"Ocurrio un error extrayendo el html: {e}")

    def process_urls(name_files):
        try:
            print("processing urls file")
            
            urls = Scraping.read_urls_from_file(os.path.join(settings.BASE_DIR, settings.FILES_URL,name_files))
            linea = 0;
        
            for url in urls:
                if not url.startswith("Error"):
                    linea += 1
                    print(f"url linea {linea}")
                    data = Scraping.scrape_website(url)
                    Scraping.export_to_json(data, os.path.join(settings.BASE_DIR, settings.FILES_URL,'products.json'))
        
            
        except Exception as e:
            raise Exception(f"Ocurrio un error procesando las urls: {e}")

    def read_urls_from_file(file_name):
        try:
            print('reading file in: '+file_name)

            with open(file_name, 'r', encoding='utf-8') as currfile:
                urls = [line.strip() for line in currfile if line.strip()]
            return urls
        except Exception as e:
                raise Exception(f'Ocurrio un error leyendo el archivo txt: {e}')

        
