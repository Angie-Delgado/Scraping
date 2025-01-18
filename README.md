# Aplicación de Scraping para obtener las características de productos de AMAZON

## Descripción

Esta aplicación de Python realiza scraping en páginas de Amazon, enfocándose en extraer información sobre computadoras de diferentes marcas. Utiliza la biblioteca **BeautifulSoup** para analizar y extraer datos específicos y almacena los resultados en una base de datos **MongoDB** en formato JSON. 

El listado de URLs que se analizarán debe proporcionarse en un archivo `.txt`.

---

## Requisitos

Antes de ejecutar la aplicación, asegúrate de tener los siguientes componentes instalados y configurados:

### Dependencias

1. **Python 3.8+**
2. Bibliotecas de Python:
   - `beautifulsoup4`
   - `Django`
   - `djongo`
   - `langdetect`
   - `pymongo`
   - `requests`
   - `spacy`
   - `langdetect`
3. **MongoDB** instalado y configurado (o una instancia en la nube).

### Instalación de dependencias

Ejecuta el siguiente comando para instalar las dependencias necesarias:

```sh
    pip install -r requirements.txt
```
**Clona el repositorio**:
```sh
    git clone <https://github.com/Angie-Delgado/Scraping/tree/master>
    cd scraper
```
## Uso

1. **Ejecuta el servidor Django**:
    ```bash
    python manage.py runserver
    ```

2. **Accede a la aplicación**:
    Abre el servidor web y ve a `http://127.0.0.1:8000/`.

## Funcionamiento

### Carga de URLs:
La aplicación lee el archivo `urls.txt` y carga todas las URLs que se deben procesar.

### Registro de URLs cargadas:
La aplicación actualiza el listado de las URLs procesadas en el archivo `urlsagregadas.txt`. Este archivo no se debe editar.

### Scraping de datos:
Para cada URL, la aplicación extrae los siguientes datos y los alamacena en el archivo `finalProducts.csv`:

- id: Identificador único del producto.
- title: Título descriptivo del producto.
- description: Descripción detallada del producto.
- delivery_time: Tiempo estimado de entrega.
- category: Categoría del producto.
- price: Precio del producto.
- link: Enlace al producto.
- image: URL de la imagen del producto.
- color: Color del producto.
- brand: Marca del producto.
- model: Modelo del producto.
- size: Dimensiones físicas del producto.
- weight: Peso del producto.
- velocity: Velocidad del procesador (en caso de productos electrónicos).
- RAM: Memoria RAM del producto (en caso de productos electrónicos).
- storage: Capacidad de almacenamiento del producto (en caso de productos electrónicos).
- pantalla: Tamaño y características de la pantalla del producto (en caso de productos electrónicos).
- sistema: Sistema operativo o plataforma del producto (en caso de productos electrónicos).

### Observaciones:
- Las columnas como velocity, RAM, storage, pantalla, y sistema están presentes solo para productos electrónicos.
- La columna delivery_time podría estar vacía si el dato no está disponible en la fuente.
- Si algún dato no está presente, aparecerá como vacío en el archivo .csv.

Este archivo facilita el análisis y la gestión de los datos de productos para su posterior uso en reportes o aplicaciones.

## Notas importantes
- Restricciones de Amazon:
El scraping de Amazon puede estar sujeto a restricciones y términos de uso. Utiliza esta herramienta de manera responsable.

- Códigos de respuesta HTTP:
Si alguna URL no devuelve datos válidos, se registrará un error en la consola.

- Manejo de grandes volúmenes de URLs:
Si planeas procesar muchas URLs, considera agregar retrasos entre las solicitudes para evitar ser bloqueado por Amazon.

## Licencia
Este proyecto está licenciado bajo la Licencia GNU Affero General Public License v3.0.